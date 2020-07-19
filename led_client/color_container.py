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

from led_client.utils import check_data_type


class ColorContainer(object):
    """Stores an array of colors"""

    def __init__(self):
        self.colors = []

    def __eq__(self, other) -> bool:
        return isinstance(other, ColorContainer) and self.colors == other.colors

    def add_color(self, color: int) -> 'ColorContainer':
        """Add a color to the ColorContainer's list of colors"""
        # Make sure that the color is the right data type
        if check_data_type('color', color, int):
            self.colors.append(color)

        # Return this instance so method calls can be chained
        return self

    def json(self) -> str:
        """Create a JSON representation of this instance"""
        return ''.join(['{"colors":[',
                        ','.join([str(color) for color in self.colors]),
                        ']}'])

    @classmethod
    def from_json(cls, input_json) -> 'ColorContainer':
        """Create a ColorContainer instance from a JSON representation"""
        # Create a new ColorContainer instance
        new_instance = cls()

        # Iterate through each color in the array
        for c in input_json.get('colors', []):
            # Make sure that the color is the right data type
            if check_data_type('color', c, int):
                new_instance.add_color(c)

        return new_instance
