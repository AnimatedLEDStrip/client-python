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
from typing import AnyStr

from animatedledstrip.utils import check_data_type


class Section(object):
    """Stores information about a section of the LED strip"""

    def __init__(self):
        self.name: str = ''
        self.start_pixel: int = -1
        self.end_pixel: int = -1
        self.physical_start: int = -1
        self.num_leds: int = 0

    def json(self) -> str:
        """Create a JSON representation of this instance"""
        if self.check_data_types() is False:
            # If something has a bad data type (and STRICT_TYPE_CHECKING is False), return an empty string
            return ''
        else:
            # Otherwise, create the JSON representation and return it
            return ''.join(['SECT:{',
                            ','.join([
                                '"name":"{}"'.format(self.name),
                                '"startPixel":{}'.format(self.start_pixel),
                                '"endPixel":{}'.format(self.end_pixel)]),
                            '}'])

    @classmethod
    def from_json(cls, input_str: AnyStr) -> 'Section':
        """Create a Section instance from a json representation"""
        # Parse the JSON
        input_json = json.loads(input_str[5:])

        # Create a new StripInfo instance
        new_instance = cls()

        new_instance.name = input_json.get('name', new_instance.name)
        new_instance.start_pixel = input_json.get('startPixel', new_instance.start_pixel)
        new_instance.end_pixel = input_json.get('endPixel', new_instance.end_pixel)
        new_instance.physical_start = input_json.get('physicalStart', new_instance.physical_start)
        new_instance.num_leds = input_json.get('numLEDs', new_instance.num_leds)

        # Double check that everything has the right data type
        new_instance.check_data_types()

        return new_instance

    def check_data_types(self) -> bool:
        """Check that all parameter types are correct"""
        good_types = True

        good_types = good_types and check_data_type('name', self.name, str)
        good_types = good_types and check_data_type('start_pixel', self.start_pixel, int)
        good_types = good_types and check_data_type('end_pixel', self.end_pixel, int)
        good_types = good_types and check_data_type('physical_start', self.physical_start, int)
        good_types = good_types and check_data_type('num_leds', self.num_leds, int)

        return good_types
