from unittest import mock

from led_client.utils import nullable_str, check_data_type


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
