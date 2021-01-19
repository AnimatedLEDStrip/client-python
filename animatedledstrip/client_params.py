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

from typing import Dict


class ClientParams:
    """Communicates parameters for this connection with the server"""

    def __init__(self,
                 send_defined_animation_info_on_connection: bool = True,
                 send_running_animation_info_on_connection: bool = True,
                 send_section_info_on_connection: bool = True,
                 send_strip_info_on_connection: bool = True,
                 send_animation_start: str = 'IMMEDIATE',
                 send_animation_end: str = 'IMMEDIATE',
                 send_section_creation: str = 'IMMEDIATE',
                 send_logs: bool = False,
                 buffered_message_interval: int = 500):
        self.send_defined_animation_info_on_connection: bool = send_defined_animation_info_on_connection
        self.send_running_animation_info_on_connection: bool = send_running_animation_info_on_connection
        self.send_section_info_on_connection: bool = send_section_info_on_connection
        self.send_strip_info_on_connection: bool = send_strip_info_on_connection
        self.send_animation_start: MessageFrequency = send_animation_start
        self.send_animation_end: MessageFrequency = send_animation_end
        self.send_section_creation: MessageFrequency = send_section_creation
        self.send_logs: bool = send_logs
        self.buffered_message_interval: int = buffered_message_interval

    def json_dict(self) -> Dict:
        return {
            "type": "ClientParams",
            "sendDefinedAnimationInfoOnConnection": self.send_defined_animation_info_on_connection,
            "sendRunningAnimationInfoOnConnection": self.send_running_animation_info_on_connection,
            "sendSectionInfoOnConnection": self.send_section_info_on_connection,
            "sendStripInfoOnConnection": self.send_strip_info_on_connection,
            "sendAnimationStart": self.send_animation_start,
            "sendAnimationEnd": self.send_animation_end,
            "sendSectionCreation": self.send_section_creation,
            "sendLogs": self.send_logs,
            "bufferedMessageInterval": self.buffered_message_interval,
        }
