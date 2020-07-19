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
from typing import Optional, Dict, AnyStr, Callable, Any, List

from .animation_data import AnimationData
from .animation_info import AnimationInfo
from .end_animation import EndAnimation
from .global_vars import *


class AnimationSender(object):
    """Handles communications with the server"""

    address: str
    port: int
    connection: 'socket.socket' = socket.socket()
    connected: bool = False
    recv_thread: Optional['Thread'] = None
    running_animations: Dict[str, 'AnimationData'] = {}
    supported_animations: List['AnimationInfo'] = []

    newAnimationDataCallback: Optional[Callable[['AnimationData'], Any]] = None
    newAnimationInfoCallback: Optional[Callable[['AnimationInfo'], Any]] = None
    newEndAnimationCallback: Optional[Callable[['EndAnimation'], Any]] = None

    def __init__(self, ip_address: str, port_num: int):
        self.address: str = ip_address
        self.port: int = port_num

    def start(self) -> 'AnimationSender':
        """Connect to the server"""
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

        # If the separate thread for receiving animations was started, join it with the main thread.
        # The loop should stop because the connection is closed and connected is False,
        #  allowing it to return
        if self.recv_thread is not None:
            self.recv_thread.join()

        return self

    def send_animation(self, animation_json: AnyStr) -> 'AnimationSender':
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
            input_bytes = self.connection.recv(4096)

            # Split up data (multiple may have come in the same message -
            #  they are split up with triple semicolons)
            for input_str in input_bytes.split(DELIMITER):
                if input_str.startswith(ANIMATION_DATA_PREFIX):
                    # Create the AnimationData instance
                    data = AnimationData.from_json(input_str)

                    # Add new animation to the running_animations dict
                    self.running_animations[data.id] = data

                    # Call callback
                    if self.newAnimationDataCallback:
                        self.newAnimationDataCallback(data)

                elif input_str.startswith(ANIMATION_INFO_PREFIX):
                    # Create the AnimationInfo instance
                    info = AnimationInfo.from_json(input_str)

                    # Add new supported animation to the supported_animations list
                    self.supported_animations.append(info)

                    # Call callback
                    if self.newAnimationInfoCallback:
                        self.newAnimationInfoCallback(info)

                elif input_str.startswith(END_ANIMATION_PREFIX):
                    # Create the EndAnimation instance
                    data = EndAnimation.from_json(input_str)

                    # Remove animation if it's in the dict
                    del self.running_animations[data.id]

                    # Call callback
                    if self.newEndAnimationCallback:
                        self.newEndAnimationCallback(data)

                elif input_str.startswith(SECTION_PREFIX):
                    pass  # TODO

                elif input_str.startswith(STRIP_INFO_PREFIX):
                    pass  # TODO

                else:
                    logging.warning('Unrecognized data type: {}'.format(input_str[:4]))

        except socket.timeout:
            pass
        except OSError:
            pass
