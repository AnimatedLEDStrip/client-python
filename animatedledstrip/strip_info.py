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

import json
from typing import AnyStr, Optional

from .utils import check_data_type


class StripInfo(object):
    """Stores information about a LED strip"""

    def __init__(self):
        self.num_leds: int = 0
        self.pin: Optional[int] = None
        self.image_debugging: bool = False
        self.file_name: Optional[str] = None
        self.renders_before_save: Optional[int] = None
        self.thread_count: int = 100

    @classmethod
    def from_json(cls, input_str: AnyStr) -> 'StripInfo':
        """Create an StripInfo instance from a JSON representation"""
        # Parse the JSON
        input_json = json.loads(input_str[5:])

        # Create a new StripInfo instance
        new_instance = cls()

        # Get each property from the JSON, reverting to defaults if it can't be found
        new_instance.num_leds = input_json.get('numLEDs', new_instance.num_leds)
        new_instance.pin = input_json.get('pin', new_instance.pin)
        new_instance.image_debugging = input_json.get('imageDebugging', new_instance.image_debugging)
        new_instance.file_name = input_json.get('fileName', new_instance.file_name)
        new_instance.renders_before_save = input_json.get('rendersBeforeSave', new_instance.renders_before_save)
        new_instance.thread_count = input_json.get('threadCount', new_instance.thread_count)

        # Double check that everything has the right data type
        new_instance.check_data_types()

        return new_instance

    def check_data_types(self) -> bool:
        """Check that all parameter types are correct"""
        good_types = True

        good_types = good_types and check_data_type('num_leds', self.num_leds, int)
        good_types = good_types and check_data_type('pin', self.pin, int, allow_none=True)
        good_types = good_types and check_data_type('image_debugging', self.image_debugging, bool)
        good_types = good_types and check_data_type('file_name', self.file_name, str, allow_none=True)
        good_types = good_types and check_data_type('renders_before_save', self.renders_before_save, int, allow_none=True)
        good_types = good_types and check_data_type('thread_count', self.thread_count, int)

        return good_types
