#   Copyright (c) 2019-2020 AnimatedLEDStrip
#
#   Permission is hereby granted, free of charge, to any person obtaining a copy
#   of this software and associated documentation files (the "Software"), to deal
#   in the Software without restriction, including without limitation the rights
#   to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
#   copies of the Software, and to permit persons to whom the Software is
#   furnished to do so, subject to the following conditions:
#
#   The above copyright notice and this permission notice shall be included in
#   all copies or substantial portions of the Software.
#
#   THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
#   IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
#   FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
#   AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
#   LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
#   OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN
#   THE SOFTWARE.

import logging
import socket
from threading import Thread
from typing import Any, AnyStr, Callable, Dict, List, Optional

from .animation_data import AnimationData
from .animation_info import AnimationInfo
from .end_animation import EndAnimation
from .global_vars import *
from .message import Message
from .section import Section
from .strip_info import StripInfo


class AnimationSender(object):
    """Handles communications with the server"""

    def __init__(self, ip_address: str, port_num: int):
        self.address: str = ip_address
        self.port: int = port_num
        self.connection: 'socket.socket' = socket.socket()
        self.connected: bool = False
        self.started: bool = False
        self.recv_thread: Optional['Thread'] = None

        self.running_animations: Dict[str, 'AnimationData'] = {}
        self.sections: Dict[str, 'Section'] = {}
        self.supported_animations: List['AnimationInfo'] = []
        self.strip_info: Optional['StripInfo'] = None

        self.on_connect_callback: Optional[Callable[[str, int], Any]] = None
        self.on_disconnect_callback: Optional[Callable[[str, int], Any]] = None
        self.on_unable_to_connect_callback: Optional[Callable[[str, int], Any]] = None

        self.on_receive_callback: Optional[Callable[[bytes], Any]] = None
        self.on_new_animation_data_callback: Optional[Callable[['AnimationData'], Any]] = None
        self.on_new_animation_info_callback: Optional[Callable[['AnimationInfo'], Any]] = None
        self.on_new_end_animation_callback: Optional[Callable[['EndAnimation'], Any]] = None
        self.on_new_message_callback: Optional[Callable[['Message'], Any]] = None
        self.on_new_section_callback: Optional[Callable[['Section'], Any]] = None
        self.on_new_strip_info_callback: Optional[Callable[['StripInfo'], Any]] = None

        self.partial_data: bytes = b''

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
        self.connection = socket.create_connection((self.address, self.port), timeout=2.0)

        # Connection has been made, so set connected = True
        self.connected = True

        # Create and start a separate thread for receiving animations
        self.recv_thread = Thread(target=self.recv_data, daemon=True)
        self.recv_thread.start()

        return self

    def end(self) -> 'AnimationSender':
        """Disconnect from the server"""
        # Disconnect from the server
        self.connection.close()

        # Connection has been closed, so set connected = False
        self.connected = False

        self.strip_info = None

        # If the separate thread for receiving animations was started, join it with the main thread.
        # The loop should stop because the connection is closed and connected is False,
        #  allowing it to return
        if self.recv_thread is not None:
            self.recv_thread.join()

        return self

    def send_data(self, animation_json: AnyStr) -> 'AnimationSender':
        """Send a new animation to the server"""
        json_bytes = bytearray(animation_json, 'utf-8')
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
            complete_input: bytes = self.partial_data + all_input
            self.partial_data = b''

            # Split up data (multiple may have come in the same message -
            #  they are split up with triple semicolons)
            input_list = complete_input.split(DELIMITER)

            # If last input is partial, save for later when the rest comes
            if not complete_input.endswith(DELIMITER):
                self.partial_data = input_list[-1]
                input_list = input_list[:-1]

            # Process inputs
            for split_input in input_list:
                if len(split_input) == 0:
                    continue

                if self.on_receive_callback:
                    self.on_receive_callback(split_input)

                if split_input.startswith(ANIMATION_DATA_PREFIX):
                    # Create the AnimationData instance
                    data = AnimationData.from_json(split_input)

                    # Add new animation to the running_animations dict
                    self.running_animations[data.id] = data

                    # Call callback
                    if self.on_new_animation_data_callback:
                        self.on_new_animation_data_callback(data)

                elif split_input.startswith(ANIMATION_INFO_PREFIX):
                    # Create the AnimationInfo instance
                    info = AnimationInfo.from_json(split_input)

                    # Add new supported animation to the supported_animations list
                    self.supported_animations.append(info)

                    # Call callback
                    if self.on_new_animation_info_callback:
                        self.on_new_animation_info_callback(info)

                elif split_input.startswith(COMMAND_PREFIX):
                    logging.warning("Receiving Command is not supported by client")

                elif split_input.startswith(END_ANIMATION_PREFIX):
                    # Create the EndAnimation instance
                    data = EndAnimation.from_json(split_input)

                    # Remove animation if it's in the dict
                    del self.running_animations[data.id]

                    # Call callback
                    if self.on_new_end_animation_callback:
                        self.on_new_end_animation_callback(data)

                elif split_input.startswith(MESSAGE_PREFIX):
                    # Create the Message instance
                    msg = Message.from_json(split_input)

                    # Call callback
                    if self.on_new_message_callback:
                        self.on_new_message_callback(msg)

                elif split_input.startswith(SECTION_PREFIX):
                    # Create the Section instance
                    sect = Section.from_json(split_input)

                    # Add new section to the sections dict
                    self.sections[sect.name] = sect

                    # Call callback
                    if self.on_new_section_callback:
                        self.on_new_section_callback(sect)

                elif split_input.startswith(STRIP_INFO_PREFIX):
                    # Create the StripInfo instance
                    info = StripInfo.from_json(split_input)

                    self.strip_info = info

                    # Call callback
                    if self.on_new_strip_info_callback:
                        self.on_new_strip_info_callback(info)

                else:
                    logging.warning('Unrecognized data type: {}'.format(str(split_input[:4], 'utf-8')))

        except socket.timeout:
            pass
        except OSError:
            pass
