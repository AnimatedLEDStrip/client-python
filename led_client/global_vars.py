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


# Should incorrect data types cause a TypeError (True)
#  or a log message (False)
STRICT_TYPE_CHECKING: bool = True

DELIMITER: bytes = bytes(';;;', 'utf-8')

ANIMATION_DATA_PREFIX: bytes = bytes('DATA:', 'utf-8')
ANIMATION_INFO_PREFIX: bytes = bytes('AINF:', 'utf-8')
END_ANIMATION_PREFIX: bytes = bytes('END :', 'utf-8')
SECTION_PREFIX: bytes = bytes('SECT:', 'utf-8')
STRIP_INFO_PREFIX: bytes = bytes('SINF:', 'utf-8')
