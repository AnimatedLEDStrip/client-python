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

from .utils import check_data_type


class Command(object):
    """A command to send to the server"""

    def __init__(self):
        self.command = ''

    def json(self) -> str:
        """Create a JSON representation of this instance"""
        if self.check_data_types() is False:
            # If something has a bad data type (and STRICT_TYPE_CHECKING is False), return an empty string
            return ''
        else:
            # Otherwise, create the JSON representation and return it
            return ''.join(['CMD :{',
                            '"command":"{}"'.format(self.command),
                            '}'])

    def check_data_types(self) -> bool:
        """Check that all parameter types are correct"""
        return check_data_type('message', self.command, str)
