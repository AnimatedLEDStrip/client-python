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

from unittest import mock

from animatedledstrip.utils import check_data_type, nullable_str


def test_nullable_str_non_null():
    assert nullable_str(5) == "5"
    assert nullable_str(False) == "False"


def test_nullable_string_null():
    assert nullable_str(None) == "null"


@mock.patch('led_client.global_vars.STRICT_TYPE_CHECKING', False)
def test_check_data_type_lenient_checking(caplog):
    assert check_data_type("test", "x", int) is False

    log_messages = {(log.msg, log.levelname) for log in caplog.records}
    assert log_messages == {("Bad data type for test: <class 'str'> (should be <class 'int'>)", 'ERROR')}


@mock.patch('led_client.global_vars.STRICT_TYPE_CHECKING', False)
def test_check_data_type_lenient_checking_allow_none(caplog):
    assert check_data_type("test", "x", int, allow_none=True) is False

    log_messages = {(log.msg, log.levelname) for log in caplog.records}
    print(caplog.records)

    assert log_messages == {("Bad data type for test: <class 'str'> (should be <class 'int'> or None)", 'ERROR')}


def test_check_data_type_strict_checking():
    try:
        check_data_type("test", "x", int)
        raise AssertionError
    except TypeError:
        pass
