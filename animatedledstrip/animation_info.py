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

from .param_usage import ParamUsage
from .utils import check_data_type


class AnimationInfo(object):
    """Stores information about an animation the server can run"""

    def __init__(self):
        self.name: str = ''
        self.abbr: str = ''
        self.description: str = ''
        self.signature_file: str = ''
        self.repetitive: bool = False
        self.minimum_colors: int = 0
        self.unlimited_colors: bool = False
        self.center: 'ParamUsage' = ParamUsage.NOTUSED
        self.delay: 'ParamUsage' = ParamUsage.NOTUSED
        self.direction: 'ParamUsage' = ParamUsage.NOTUSED
        self.distance: 'ParamUsage' = ParamUsage.NOTUSED
        self.spacing: 'ParamUsage' = ParamUsage.NOTUSED
        self.delay_default: int = 50
        self.distance_default: int = -1
        self.spacing_default: int = 3

    @classmethod
    def from_json(cls, input_str: AnyStr) -> 'AnimationInfo':
        """Create an AnimationInfo instance from a JSON representation"""
        # Parse the JSON
        input_json = json.loads(input_str[5:])

        # Create a new AnimationInfo instance
        new_instance = cls()

        # Get each property from the JSON, reverting to defaults if it can't be found
        new_instance.name = input_json.get('name', new_instance.name)
        new_instance.abbr = input_json.get('abbr', new_instance.abbr)
        new_instance.description = input_json.get('description', new_instance.description)
        new_instance.signature_file = input_json.get('signatureFile', new_instance.signature_file)
        new_instance.repetitive = input_json.get('repetitive', new_instance.repetitive)
        new_instance.minimum_colors = input_json.get('minimumColors', new_instance.minimum_colors)
        new_instance.unlimited_colors = input_json.get('unlimitedColors', new_instance.unlimited_colors)
        new_instance.center = ParamUsage[input_json.get('center', new_instance.center.name)]
        new_instance.delay = ParamUsage[input_json.get('delay', new_instance.delay.name)]
        new_instance.direction = ParamUsage[input_json.get('direction', new_instance.direction.name)]
        new_instance.distance = ParamUsage[input_json.get('distance', new_instance.distance.name)]
        new_instance.spacing = ParamUsage[input_json.get('spacing', new_instance.spacing.name)]
        new_instance.delay_default = input_json.get('delayDefault', new_instance.delay_default)
        new_instance.distance_default = input_json.get('distanceDefault', new_instance.distance_default)
        new_instance.spacing_default = input_json.get('spacingDefault', new_instance.spacing_default)

        # Double check that everything has the right data type
        new_instance.check_data_types()

        return new_instance

    def check_data_types(self) -> bool:
        """Check that all parameter types are correct"""
        good_types = True

        good_types = good_types and check_data_type('name', self.name, str)
        good_types = good_types and check_data_type('abbr', self.abbr, str)
        good_types = good_types and check_data_type('description', self.description, str)
        good_types = good_types and check_data_type('signature_file', self.signature_file, str)
        good_types = good_types and check_data_type('repetitive', self.repetitive, bool)
        good_types = good_types and check_data_type('minimum_colors', self.minimum_colors, int)
        good_types = good_types and check_data_type('unlimited_colors', self.unlimited_colors, bool)
        good_types = good_types and check_data_type('center', self.center, ParamUsage)
        good_types = good_types and check_data_type('delay', self.delay, ParamUsage)
        good_types = good_types and check_data_type('direction', self.direction, ParamUsage)
        good_types = good_types and check_data_type('distance', self.distance, ParamUsage)
        good_types = good_types and check_data_type('spacing', self.spacing, ParamUsage)
        good_types = good_types and check_data_type('delay_default', self.delay_default, int)
        good_types = good_types and check_data_type('distance_default', self.distance_default, int)
        good_types = good_types and check_data_type('spacing_default', self.spacing_default, int)

        return good_types
