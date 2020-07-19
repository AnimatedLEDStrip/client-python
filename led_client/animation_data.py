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
from typing import List, Optional, AnyStr

from .color_container import ColorContainer
from .direction import *
from .utils import check_data_type, nullable_str


class AnimationData(object):
    """Stores data about an animation"""

    def __init__(self):
        self.animation: str = 'Color'
        self.colors: List['ColorContainer'] = []
        self.center: int = -1
        self.continuous: Optional[bool] = None
        self.delay: int = -1
        self.delay_mod: float = 1.0
        self.direction: 'Direction' = Direction.FORWARD
        self.distance: int = -1
        self.id: str = ''
        self.section: str = ''
        self.spacing: int = -1

    def add_color(self, color: 'ColorContainer') -> 'AnimationData':
        """Add a new ColorContainer to colors"""
        # Make sure that the color is the right data type
        if check_data_type('color', color, ColorContainer) is True:
            self.colors.append(color)

        # Return this instance so method calls can be chained
        return self

    def colors_json(self) -> str:
        """Create a JSON representation of colors"""
        return ','.join([color.json() for color in self.colors])

    def json(self) -> str:
        """Create a JSON representation of this instance"""
        if self.check_data_types() is False:
            # If something has a bad data type (and STRICT_TYPE_CHECKING is False), return an empty string
            return ''
        else:
            # Otherwise, create the JSON representation and return it
            return ''.join(['DATA:{',
                            ','.join([
                                '"animation":"{}"'.format(self.animation),
                                '"colors":[{}]'.format(self.colors_json()),
                                '"center":{}'.format(str(self.center)),
                                '"continuous":{}'.format(nullable_str(self.continuous)),
                                '"delay":{}'.format(str(self.delay)),
                                '"delayMod":{}'.format(str(self.delay_mod)),
                                '"direction":"{}"'.format(self.direction.name),
                                '"distance":{}'.format(str(self.distance)),
                                '"id":"{}"'.format(self.id),
                                '"section":"{}"'.format(self.section),
                                '"spacing":{}'.format(str(self.spacing))]),
                            '}'])

    @classmethod
    def from_json(cls, input_str: AnyStr) -> 'AnimationData':
        """Create an AnimationData instance from a JSON representation"""
        # Parse the JSON
        input_json = json.loads(input_str[5:])

        # Create a new AnimationData instance
        new_instance = cls()

        # Get each property from the JSON, reverting to defaults if it can't be found
        new_instance.animation = input_json.get('animation', new_instance.animation)
        new_instance.colors = [ColorContainer.from_json(cc_arr) for cc_arr in input_json.get('colors', [])]
        new_instance.center = input_json.get('center', new_instance.center)
        new_instance.continuous = input_json.get('continuous', new_instance.continuous)
        new_instance.delay = input_json.get('baseDelay', new_instance.delay)
        new_instance.delay_mod = input_json.get('delayMod', new_instance.delay_mod)
        new_instance.direction = Direction[input_json.get('direction', new_instance.direction)]
        new_instance.distance = input_json.get('distance', new_instance.distance)
        new_instance.id = input_json.get('id', new_instance.id)
        new_instance.section = input_json.get('section', new_instance.section)
        new_instance.spacing = input_json.get('spacing', new_instance.spacing)

        # Double check that everything has the right data type
        new_instance.check_data_types()

        return new_instance

    def check_data_types(self) -> bool:
        """Check that all parameter types are correct"""
        good_types = True

        good_types = good_types and check_data_type('animation', self.animation, str)
        for color_container in self.colors:
            good_types = good_types and check_data_type('color', color_container, ColorContainer)
        good_types = good_types and check_data_type('center', self.center, int)
        good_types = good_types and check_data_type('continuous', self.continuous, bool, allow_none=True)
        good_types = good_types and check_data_type('delay', self.delay, int)
        good_types = good_types and check_data_type('delay_mod', self.delay_mod, float)
        good_types = good_types and check_data_type('direction', self.direction, Direction)
        good_types = good_types and check_data_type('distance', self.distance, int)
        good_types = good_types and check_data_type('id', self.id, str)
        good_types = good_types and check_data_type('section', self.section, str)
        good_types = good_types and check_data_type('spacing', self.spacing, int)

        return good_types
