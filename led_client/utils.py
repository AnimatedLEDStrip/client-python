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
from typing import TypeVar, Any, Optional

from . import global_vars


def nullable_str(value: Optional[Any]) -> str:
    """Convert values to a string while converting None to 'null'"""
    if value is None:
        return 'null'
    else:
        return str(value)


def check_data_type(name: str, param: Any, correct_type: TypeVar, allow_none: bool = False) -> bool:
    """Check that a parameter has the correct data type

    If it does not, then when STRICT_TYPE_CHECKING is:
        True  -> throw a TypeError
        False -> print a log message and return False"""

    # Check the type of param
    # If None is an acceptable value, check for that too
    if not isinstance(param, correct_type) and not (allow_none and param is None):
        # Type was incorrect, prepare message
        msg = 'Bad data type for {name}: {bad_type} ' \
              '(should be {cor_type}{none_allowed})'.format(name=name,
                                                            bad_type=str(type(param)),
                                                            cor_type=str(correct_type),
                                                            none_allowed=" or None" if allow_none else "")

        if global_vars.STRICT_TYPE_CHECKING:
            # Type was incorrect and STRICT_TYPE_CHECKING is True, raise TypeError with message
            raise TypeError(msg)
        else:
            # Type was incorrect and STRICT_TYPE_CHECKING is False, print log message and return False
            logging.error(msg)
            return False

    # Type was correct, return True
    return True
