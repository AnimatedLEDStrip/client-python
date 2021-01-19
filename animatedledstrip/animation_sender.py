#  Copyright (c) 2018-2021 AnimatedLEDStrip
#
#  Permission is hereby granted, free of charge, to any person obtaining a copy
#  of this software and associated documentation files (the "Software"), to deal
#  in the Software without restriction, including without limitation the rights
#  to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
#  copies of the Software, and to permit persons to whom the Software is
#  furnished to do so, subject to the following conditions:
#
#  The above copyright notice and this permission notice shall be included in
#  all copies or substantial portions of the Software.
#
#  THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
#  IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
#  FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
#  AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
#  LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
#  OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN
#  THE SOFTWARE.

import logging
import socket
from threading import Thread
from typing import Any, AnyStr, Callable, Dict, List, Optional

from .animation_info import AnimationInfo
from .animation_to_run_params import AnimationToRunParams
from .command import Command
from .current_strip_color import CurrentStripColor
from .end_animation import EndAnimation
from .global_vars import *
from .json_decoder import ALSJsonDecoder
from .message import Message
from .running_animation_params import RunningAnimationParams
from .section import Section
from .strip_info import StripInfo


class AnimationSender(object):
    """Handles communications with the server"""

    def __init__(self, ip_address: str, port_num: int):
        self.address: str = ip_address
        self.port: int = port_num
        self.connection: 'socket.socket' = socket.socket()

        self.started: bool = False
        self.connected: bool = False

        self.running_animations: Dict[str, 'RunningAnimationParams'] = {}
        self.sections: Dict[str, 'Section'] = {}
        self.supported_animations: List['AnimationInfo'] = []
        self.strip_info: Optional['StripInfo'] = None

        self.on_connect_callback: Optional[Callable[[str, int], Any]] = None
        self.on_disconnect_callback: Optional[Callable[[str, int], Any]] = None
        self.on_unable_to_connect_callback: Optional[Callable[[str, int], Any]] = None

        self.on_receive_callback: Optional[Callable[[bytes], Any]] = None
        self.on_new_animation_info_callback: Optional[Callable[['AnimationInfo'], Any]] = None
        self.on_new_current_strip_color_callback: Optional[Callable[['CurrentStripColor'], Any]] = None
        self.on_new_end_animation_callback: Optional[Callable[['EndAnimation'], Any]] = None
        self.on_new_message_callback: Optional[Callable[['Message'], Any]] = None
        self.on_new_running_animation_params_callback: Optional[Callable[['RunningAnimationParams'], Any]] = None
        self.on_new_section_callback: Optional[Callable[['Section'], Any]] = None
        self.on_new_strip_info_callback: Optional[Callable[['StripInfo'], Any]] = None

        self._recv_thread: Optional['Thread'] = None
        self._partial_data: bytes = b''

        self.decoder = ALSJsonDecoder()

    def start(self) -> 'AnimationSender':
        """Connect to the server"""
        if self.started:
            return self

        self.running_animations.clear()
        self.sections.clear()
        self.supported_animations.clear()
        self.strip_info = None

        self.started = True

        # Attempt to connect to the server
        try:
            self.connection = socket.create_connection((self.address, self.port), timeout=2.0)
        except socket.timeout:
            if self.on_unable_to_connect_callback:
                self.on_unable_to_connect_callback(self.address, self.port)
            self.started = False
            self.connected = False
            return self

        # Connection has been made, so set connected = True
        self.connected = True

        if self.on_connect_callback:
            self.on_connect_callback(self.address, self.port)

        # Create and start a separate thread for receiving animations
        self._recv_thread = Thread(target=self.recv_data, daemon=True)
        self._recv_thread.start()

        return self

    def end(self) -> 'AnimationSender':
        """Disconnect from the server"""
        self.started = False
        self.connected = False

        # Disconnect from the server
        self.connection.close()

        # If the separate thread for receiving animations was started, join it with the main thread.
        # The loop should stop because the connection is closed and connected is False,
        #  allowing it to return
        if self._recv_thread is not None:
            self._recv_thread.join()

        return self

    def send_data(self, animation_json: AnyStr) -> 'AnimationSender':
        """Send a new animation to the server"""
        json_bytes = bytearray(animation_json + ";;;", 'utf-8')
        self.connection.sendall(json_bytes)

        return self

    def recv_data(self):
        """Loop that runs in a separate thread to receive data from the server"""
        while self.connected:
            self.parse_data()

    def parse_data(self):
        try:
            all_input: bytes = self.connection.recv(4096)

            # Handle any partial data from previous communications
            complete_input: bytes = self._partial_data + all_input
            self._partial_data = b''

            # Split up data (multiple may have come in the same message -
            #  they are split up with triple semicolons)
            input_list = complete_input.split(DELIMITER)

            # If last input is partial, save for later when the rest comes
            if not complete_input.endswith(DELIMITER):
                self._partial_data = input_list[-1]
                input_list = input_list[:-1]

            # Process inputs
            for split_input in input_list:

                if len(split_input) == 0:
                    continue

                if self.on_receive_callback:
                    self.on_receive_callback(split_input)

                data = self.decoder.decode(str(split_input, 'utf-8'))

                if isinstance(data, AnimationInfo):
                    # Add new supported animation to the supported_animations list
                    self.supported_animations.append(data)

                    # Call callback
                    if self.on_new_animation_info_callback:
                        self.on_new_animation_info_callback(data)

                elif isinstance(data, AnimationToRunParams):
                    logging.warning("Receiving AnimationToRunParams is not supported by client")

                elif isinstance(data, Command):
                    logging.warning("Receiving Command is not supported by client")

                elif isinstance(data, CurrentStripColor):
                    if self.on_new_current_strip_color_callback:
                        self.on_new_current_strip_color_callback(data)

                elif isinstance(data, EndAnimation):
                    # Call callback
                    if self.on_new_end_animation_callback:
                        self.on_new_end_animation_callback(data)

                    # Remove animation if it's in the dict
                    del self.running_animations[data.anim_id]

                elif isinstance(data, Message):
                    # Call callback
                    if self.on_new_message_callback:
                        self.on_new_message_callback(data)

                elif isinstance(data, RunningAnimationParams):
                    # Call callback
                    if self.on_new_running_animation_params_callback:
                        self.on_new_running_animation_params_callback(data)

                    # Add new animation to the running_animations dict
                    self.running_animations[data.anim_id] = data

                elif isinstance(data, Section):
                    # Call callback
                    if self.on_new_section_callback:
                        self.on_new_section_callback(data)

                    # Add new section to the sections dict
                    self.sections[data.name] = data

                elif isinstance(data, StripInfo):
                    self.strip_info = data

                    # Call callback
                    if self.on_new_strip_info_callback:
                        self.on_new_strip_info_callback(data)

                else:
                    logging.warning('Unrecognized data type: {}'.format(str(split_input[:4], 'utf-8')))

        except socket.timeout:
            pass
        except OSError:
            pass
