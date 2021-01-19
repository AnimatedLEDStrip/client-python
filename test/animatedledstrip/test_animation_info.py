from unittest import mock

from animatedledstrip import AnimationInfo


def test_constructor():
    info = AnimationInfo()

    assert info.name == ''
    assert info.abbr == ''
    assert info.description == ''
    assert info.signature_file == ''
    assert info.repetitive is False
    assert info.minimum_colors == 0
    assert info.unlimited_colors is False
    # assert info.center is ParamUsage.NOTUSED
    # assert info.delay is ParamUsage.NOTUSED
    # assert info.direction is ParamUsage.NOTUSED
    # assert info.distance is ParamUsage.NOTUSED
    # assert info.spacing is ParamUsage.NOTUSED
    assert info.delay_default == 50
    assert info.distance_default == -1
    assert info.spacing_default == 3


def test_name(caplog):
    info = AnimationInfo()

    info.name = 'Sparkle'
    assert info.check_data_types() is True

    info.name = 3
    with mock.patch('animatedledstrip.global_vars.STRICT_TYPE_CHECKING', False):
        assert info.check_data_types() is False
        log_messages = {(log.msg, log.levelname) for log in caplog.records}
        assert log_messages == {("Bad data type for name: <class 'int'> (should be <class 'str'>)", 'ERROR')}

    try:
        info.check_data_types()
        raise AssertionError
    except TypeError:
        pass


def test_abbr(caplog):
    info = AnimationInfo()

    info.abbr = 'SPK'
    assert info.check_data_types() is True

    info.abbr = 3
    with mock.patch('animatedledstrip.global_vars.STRICT_TYPE_CHECKING', False):
        assert info.check_data_types() is False
        log_messages = {(log.msg, log.levelname) for log in caplog.records}
        assert log_messages == {("Bad data type for abbr: <class 'int'> (should be <class 'str'>)", 'ERROR')}

    try:
        info.check_data_types()
        raise AssertionError
    except TypeError:
        pass


def test_description(caplog):
    info = AnimationInfo()

    info.description = 'A description'
    assert info.check_data_types() is True

    info.description = 3
    with mock.patch('animatedledstrip.global_vars.STRICT_TYPE_CHECKING', False):
        assert info.check_data_types() is False
        log_messages = {(log.msg, log.levelname) for log in caplog.records}
        assert log_messages == {("Bad data type for description: <class 'int'> (should be <class 'str'>)", 'ERROR')}

    try:
        info.check_data_types()
        raise AssertionError
    except TypeError:
        pass


def test_signature_file(caplog):
    info = AnimationInfo()

    info.signature_file = 'file.png'
    assert info.check_data_types() is True

    info.signature_file = 3
    with mock.patch('animatedledstrip.global_vars.STRICT_TYPE_CHECKING', False):
        assert info.check_data_types() is False
        log_messages = {(log.msg, log.levelname) for log in caplog.records}
        assert log_messages == {("Bad data type for signature_file: <class 'int'> (should be <class 'str'>)", 'ERROR')}

    try:
        info.check_data_types()
        raise AssertionError
    except TypeError:
        pass


def test_repetitive(caplog):
    info = AnimationInfo()

    info.repetitive = False
    assert info.check_data_types() is True

    info.repetitive = 3
    with mock.patch('animatedledstrip.global_vars.STRICT_TYPE_CHECKING', False):
        assert info.check_data_types() is False
        log_messages = {(log.msg, log.levelname) for log in caplog.records}
        assert log_messages == {("Bad data type for repetitive: <class 'int'> (should be <class 'bool'>)", 'ERROR')}

    try:
        info.check_data_types()
        raise AssertionError
    except TypeError:
        pass


def test_minimum_colors(caplog):
    info = AnimationInfo()

    info.minimum_colors = 5
    assert info.check_data_types() is True

    info.minimum_colors = 5.0
    with mock.patch('animatedledstrip.global_vars.STRICT_TYPE_CHECKING', False):
        assert info.check_data_types() is False
        log_messages = {(log.msg, log.levelname) for log in caplog.records}
        assert log_messages == {
            ("Bad data type for minimum_colors: <class 'float'> (should be <class 'int'>)", 'ERROR')
        }

    try:
        info.check_data_types()
        raise AssertionError
    except TypeError:
        pass


def test_unlimited_colors(caplog):
    info = AnimationInfo()

    info.unlimited_colors = False
    assert info.check_data_types() is True

    info.unlimited_colors = 5.0
    with mock.patch('animatedledstrip.global_vars.STRICT_TYPE_CHECKING', False):
        assert info.check_data_types() is False
        log_messages = {(log.msg, log.levelname) for log in caplog.records}
        assert log_messages == {
            ("Bad data type for unlimited_colors: <class 'float'> (should be <class 'bool'>)", 'ERROR')
        }

    try:
        info.check_data_types()
        raise AssertionError
    except TypeError:
        pass


def test_center(caplog):
    info = AnimationInfo()

    # info.center = ParamUsage.NOTUSED
    assert info.check_data_types() is True

    info.center = 5.0
    with mock.patch('animatedledstrip.global_vars.STRICT_TYPE_CHECKING', False):
        assert info.check_data_types() is False
        log_messages = {(log.msg, log.levelname) for log in caplog.records}
        assert log_messages == {("Bad data type for center: <class 'float'> (should be <enum 'ParamUsage'>)", 'ERROR')}

    try:
        info.check_data_types()
        raise AssertionError
    except TypeError:
        pass


def test_delay(caplog):
    info = AnimationInfo()

    # info.delay = ParamUsage.NOTUSED
    assert info.check_data_types() is True

    info.delay = 5.0
    with mock.patch('animatedledstrip.global_vars.STRICT_TYPE_CHECKING', False):
        assert info.check_data_types() is False
        log_messages = {(log.msg, log.levelname) for log in caplog.records}
        assert log_messages == {("Bad data type for delay: <class 'float'> (should be <enum 'ParamUsage'>)", 'ERROR')}

    try:
        info.check_data_types()
        raise AssertionError
    except TypeError:
        pass


def test_direction(caplog):
    info = AnimationInfo()

    # info.direction = ParamUsage.NOTUSED
    assert info.check_data_types() is True

    info.direction = 5.0
    with mock.patch('animatedledstrip.global_vars.STRICT_TYPE_CHECKING', False):
        assert info.check_data_types() is False
        log_messages = {(log.msg, log.levelname) for log in caplog.records}
        assert log_messages == {
            ("Bad data type for direction: <class 'float'> (should be <enum 'ParamUsage'>)", 'ERROR')
        }

    try:
        info.check_data_types()
        raise AssertionError
    except TypeError:
        pass


def test_distance(caplog):
    info = AnimationInfo()

    # info.distance = ParamUsage.NOTUSED
    assert info.check_data_types() is True

    info.distance = 5.0
    with mock.patch('animatedledstrip.global_vars.STRICT_TYPE_CHECKING', False):
        assert info.check_data_types() is False
        log_messages = {(log.msg, log.levelname) for log in caplog.records}
        assert log_messages == {
            ("Bad data type for distance: <class 'float'> (should be <enum 'ParamUsage'>)", 'ERROR')
        }

    try:
        info.check_data_types()
        raise AssertionError
    except TypeError:
        pass


def test_spacing(caplog):
    info = AnimationInfo()

    # info.spacing = ParamUsage.NOTUSED
    assert info.check_data_types() is True

    info.spacing = 5.0
    with mock.patch('animatedledstrip.global_vars.STRICT_TYPE_CHECKING', False):
        assert info.check_data_types() is False
        log_messages = {(log.msg, log.levelname) for log in caplog.records}
        assert log_messages == {("Bad data type for spacing: <class 'float'> (should be <enum 'ParamUsage'>)", 'ERROR')}

    try:
        info.check_data_types()
        raise AssertionError
    except TypeError:
        pass


def test_delay_default(caplog):
    info = AnimationInfo()

    info.delay_default = 5
    assert info.check_data_types() is True

    info.delay_default = 5.0
    with mock.patch('animatedledstrip.global_vars.STRICT_TYPE_CHECKING', False):
        assert info.check_data_types() is False
        log_messages = {(log.msg, log.levelname) for log in caplog.records}
        assert log_messages == {("Bad data type for delay_default: <class 'float'> (should be <class 'int'>)", 'ERROR')}

    try:
        info.check_data_types()
        raise AssertionError
    except TypeError:
        pass


def test_distance_default(caplog):
    info = AnimationInfo()

    info.distance_default = 5
    assert info.check_data_types() is True

    info.distance_default = 5.0
    with mock.patch('animatedledstrip.global_vars.STRICT_TYPE_CHECKING', False):
        assert info.check_data_types() is False
        log_messages = {(log.msg, log.levelname) for log in caplog.records}
        assert log_messages == {
            ("Bad data type for distance_default: <class 'float'> (should be <class 'int'>)", 'ERROR')
        }

    try:
        info.check_data_types()
        raise AssertionError
    except TypeError:
        pass


def test_spacing_default(caplog):
    info = AnimationInfo()

    info.spacing_default = 5
    assert info.check_data_types() is True

    info.spacing_default = 5.0
    with mock.patch('animatedledstrip.global_vars.STRICT_TYPE_CHECKING', False):
        assert info.check_data_types() is False
        log_messages = {(log.msg, log.levelname) for log in caplog.records}
        assert log_messages == {
            ("Bad data type for spacing_default: <class 'float'> (should be <class 'int'>)", 'ERROR')
        }

    try:
        info.check_data_types()
        raise AssertionError
    except TypeError:
        pass
