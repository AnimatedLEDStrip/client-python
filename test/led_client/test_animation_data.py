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

from led_client import *


def test_constructor():
    data = AnimationData()

    assert data.animation == 'Color'
    assert data.center == -1
    assert data.continuous is None
    assert data.delay == -1
    assert data.delay_mod == 1.0
    assert data.direction is Direction.FORWARD
    assert data.distance == -1
    assert data.id == ''
    assert data.section == ''
    assert data.spacing == -1


def test_animation():
    data = AnimationData()

    data.animation = 'Sparkle'
    assert data.check_data_types() is True

    data.animation = 3
    with mock.patch('led_client.global_vars.STRICT_TYPE_CHECKING', False):
        assert data.check_data_types() is False

    try:
        data.check_data_types()
        raise AssertionError
    except TypeError:
        pass


def test_center():
    data = AnimationData()

    data.center = 5
    assert data.check_data_types() is True

    data.center = Direction.FORWARD
    with mock.patch('led_client.global_vars.STRICT_TYPE_CHECKING', False):
        assert data.check_data_types() is False

    try:
        data.check_data_types()
        raise AssertionError
    except TypeError:
        pass


def test_continuous():
    data = AnimationData()

    data.continuous = True
    assert data.check_data_types() is True

    data.continuous = None
    assert data.check_data_types() is True

    data.continuous = 5
    with mock.patch('led_client.global_vars.STRICT_TYPE_CHECKING', False):
        assert data.check_data_types() is False

    try:
        data.check_data_types()
        raise AssertionError
    except TypeError:
        pass


def test_delay():
    data = AnimationData()

    data.delay = 10
    assert data.check_data_types() is True

    data.delay = Direction.BACKWARD
    with mock.patch('led_client.global_vars.STRICT_TYPE_CHECKING', False):
        assert data.check_data_types() is False

    try:
        data.check_data_types()
        raise AssertionError
    except TypeError:
        pass


def test_delay_mod():
    data = AnimationData()

    data.delay_mod = 0.5
    assert data.check_data_types() is True

    data.delay_mod = 3
    with mock.patch('led_client.global_vars.STRICT_TYPE_CHECKING', False):
        assert data.check_data_types() is False

    try:
        data.check_data_types()
        raise AssertionError
    except TypeError:
        pass


def test_direction():
    data = AnimationData()

    data.direction = Direction.BACKWARD
    assert data.check_data_types() is True

    data.direction = 1
    with mock.patch('led_client.global_vars.STRICT_TYPE_CHECKING', False):
        assert data.check_data_types() is False

    try:
        data.check_data_types()
        raise AssertionError
    except TypeError:
        pass


def test_distance():
    data = AnimationData()

    data.distance = 5
    assert data.check_data_types() is True

    data.distance = 5.0
    with mock.patch('led_client.global_vars.STRICT_TYPE_CHECKING', False):
        assert data.check_data_types() is False

    try:
        data.check_data_types()
        raise AssertionError
    except TypeError:
        pass


def test_id():
    data = AnimationData()

    data.id = 'TEST'
    assert data.check_data_types() is True

    data.id = 5
    with mock.patch('led_client.global_vars.STRICT_TYPE_CHECKING', False):
        assert data.check_data_types() is False

    try:
        data.check_data_types()
        raise AssertionError
    except TypeError:
        pass


def test_section():
    data = AnimationData()

    data.section = 'SECT'
    assert data.check_data_types() is True

    data.section = 5
    with mock.patch('led_client.global_vars.STRICT_TYPE_CHECKING', False):
        assert data.check_data_types() is False

    try:
        data.check_data_types()
        raise AssertionError
    except TypeError:
        pass


def test_spacing():
    data = AnimationData()

    data.spacing = 10
    assert data.check_data_types() is True

    data.spacing = 3.0
    with mock.patch('led_client.global_vars.STRICT_TYPE_CHECKING', False):
        assert data.check_data_types() is False

    try:
        data.check_data_types()
        raise AssertionError
    except TypeError:
        pass


def test_json():
    data = AnimationData()

    data.animation = 'Meteor'
    data.center = 50
    data.continuous = False
    data.delay = 10
    data.delay_mod = 1.5
    data.direction = Direction.BACKWARD
    data.distance = 45
    data.id = 'TEST'
    data.section = 'SECT'
    data.spacing = 5

    cc = ColorContainer()
    cc.add_color(0xFF)
    cc.add_color(0xFF00)
    cc2 = ColorContainer()
    cc2.add_color(0xFF0000)
    data.add_color(cc)
    data.add_color(cc2)

    assert data.json() == 'DATA:{"animation":"Meteor","colors":[{"colors":[255,65280]},{"colors":[' \
                          '16711680]}],"center":50,"continuous":False,"delay":10,"delayMod":1.5,' \
                          '"direction":"BACKWARD","distance":45,"id":"TEST","section":"SECT",' \
                          '"spacing":5}'


def test_json_no_cc():
    data = AnimationData()

    data.animation = 'Meteor'
    data.center = 50
    data.continuous = False
    data.delay = 10
    data.delay_mod = 1.5
    data.direction = Direction.BACKWARD
    data.distance = 45
    data.id = 'TEST'
    data.section = 'SECT'
    data.spacing = 5

    assert data.json() == 'DATA:{"animation":"Meteor","colors":[],"center":50,"continuous":False,' \
                          '"delay":10,"delayMod":1.5,"direction":"BACKWARD","distance":45,' \
                          '"id":"TEST","section":"SECT","spacing":5}'


def test_json_bad_type():
    data = AnimationData()
    data.spacing = 1.5

    with mock.patch('led_client.global_vars.STRICT_TYPE_CHECKING', False):
        assert data.json() == ''

    try:
        data.json()
        raise AssertionError
    except TypeError:
        pass


def test_add_bad_color():
    try:
        # noinspection PyTypeChecker
        AnimationData().add_color(-1)
        raise AssertionError
    except TypeError:
        pass


def test_colors_json():
    assert AnimationData().colors_json() == ''
    data = AnimationData().add_color(ColorContainer().add_color(0xFF)).add_color(ColorContainer().add_color(0x0F))
    assert data.colors_json() == '{"colors":[255]},{"colors":[15]}'


def test_from_json():
    json_data = 'DATA:{"animation":"Meteor","colors":[{"colors":[255]}],"center":50,"continuous":false,' \
                '"baseDelay":10,"delayMod":1.5,"direction":"BACKWARD","distance":45,' \
                '"id":"TEST","section":"SECT","spacing":5}'

    data = AnimationData.from_json(json_data)
    assert data.animation == 'Meteor'
    assert data.colors == [ColorContainer().add_color(255)]
    assert data.center == 50
    assert data.continuous is False
    assert data.delay == 10
    assert data.delay_mod == 1.5
    assert data.direction is Direction.BACKWARD
    assert data.distance == 45
    assert data.id == 'TEST'
    assert data.section == 'SECT'
    assert data.spacing == 5

    assert data.json() == 'DATA:{"animation":"Meteor","colors":[{"colors":[255]}],"center":50,"continuous":False,' \
                          '"delay":10,"delayMod":1.5,"direction":"BACKWARD","distance":45,' \
                          '"id":"TEST","section":"SECT","spacing":5}'
