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

from .utils import check_data_type


class EndAnimation(object):
    """Represents the ending of an animation"""

    def __init__(self):
        self.id = ''

    def json(self) -> str:
        self.check_data_types()

        return 'END :{"id":"' + self.id + '"}'

    @classmethod
    def from_json(cls, input_str: AnyStr) -> 'EndAnimation':
        """Create an EndAnimation instance from a JSON representation"""
        # Parse the JSON
        input_json = json.loads(input_str[5:])

        # Create a new EndAnimation instance
        new_instance = cls()

        # Get property from the JSON, reverting to default if it can't be found
        new_instance.id = input_json.get('id', new_instance.id)

        # Double check that parameter has the right data type
        new_instance.check_data_types()

        return new_instance

    def check_data_types(self) -> bool:
        """Check that parameter type is correct"""
        return check_data_type('id', self.id, str)
