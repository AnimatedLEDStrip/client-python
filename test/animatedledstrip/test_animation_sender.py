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

from animatedledstrip import AnimationSender, AnimationData, Direction, ParamUsage


def test_constructor():
    sender = AnimationSender('10.0.0.254', 5)

    assert sender.address == '10.0.0.254'
    assert sender.port == 5


@mock.patch.object(AnimationSender, 'connection')
def test_send_animation(mock_socket):
    data = AnimationData().json()
    AnimationSender('10.0.0.254', 5).send_data(data)
    assert mock_socket.sendall.called
    assert mock_socket.called_with(data)


@mock.patch.object(AnimationSender, 'newAnimationDataCallback')
@mock.patch.object(AnimationSender, 'connection')
def test_parse_data_animation_data(mock_socket, mock_callback):
    sender = AnimationSender('10.0.0.254', 5)

    mock_socket.recv.return_value = bytes('DATA:{"animation":"Meteor","baseDelay":10,"center":120,'
                                          '"colors":[{"colors":[16711680]}],"continuous":null,'
                                          '"delayMod":1.0,"direction":"FORWARD","distance":240,'
                                          '"id":"52782797","section":"","spacing":3}', 'utf-8')

    sender.parse_data()

    assert '52782797' in sender.running_animations.keys()

    anim = sender.running_animations['52782797']

    assert anim.animation == 'Meteor'
    assert anim.center == 120
    assert len(anim.colors) == 1
    assert anim.colors[0].colors == [0xff0000]
    assert anim.continuous is None
    assert anim.delay == 10
    assert anim.delay_mod == 1.0
    assert anim.direction is Direction.FORWARD
    assert anim.distance == 240
    assert anim.id == '52782797'
    assert anim.section == ''
    assert anim.spacing == 3

    assert mock_callback.called
    assert mock_callback.called_with(anim)


@mock.patch.object(AnimationSender, 'newAnimationInfoCallback')
@mock.patch.object(AnimationSender, 'connection')
def test_parse_data_animation_info(mock_socket, mock_callback):
    sender = AnimationSender('10.0.0.254', 5)

    mock_socket.recv.return_value = bytes('AINF:{"name":"Multi Pixel Run","abbr":"MPR",'
                                          '"description":"Similar to [Pixel Run](Pixel-Run) but with multiple LEDs '
                                          'at a specified spacing.","signatureFile":"multi_pixel_run.png",'
                                          '"repetitive":true,"minimumColors":1,"unlimitedColors":false,'
                                          '"center":"NOTUSED","delay":"USED","direction":"USED",'
                                          '"distance":"NOTUSED","spacing":"USED","delayDefault":100,'
                                          '"distanceDefault":-1,"spacingDefault":3}', 'utf-8')

    sender.parse_data()

    assert len(sender.supported_animations) == 1

    info = sender.supported_animations[0]

    assert info.name == 'Multi Pixel Run'
    assert info.abbr == 'MPR'
    assert info.description == 'Similar to [Pixel Run](Pixel-Run) but with multiple LEDs at a specified spacing.'
    assert info.signature_file == 'multi_pixel_run.png'
    assert info.repetitive is True
    assert info.minimum_colors == 1
    assert info.unlimited_colors is False
    assert info.center is ParamUsage.NOTUSED
    assert info.delay is ParamUsage.USED
    assert info.direction is ParamUsage.USED
    assert info.distance is ParamUsage.NOTUSED
    assert info.spacing is ParamUsage.USED
    assert info.delay_default == 100
    assert info.distance_default == -1
    assert info.spacing_default == 3

    assert mock_callback.called
    assert mock_callback.called_with(info)


@mock.patch.object(AnimationSender, 'newEndAnimationCallback')
@mock.patch.object(AnimationSender, 'connection')
def test_parse_data_end_animation(mock_socket, mock_callback):
    sender = AnimationSender('10.0.0.254', 5)

    mock_socket.recv.return_value = bytes('DATA:{"animation":"Meteor","baseDelay":10,"center":120,'
                                          '"colors":[{"colors":[16711680]}],"continuous":null,'
                                          '"delayMod":1.0,"direction":"FORWARD","distance":240,'
                                          '"id":"52782797","section":"","spacing":3}', 'utf-8')

    sender.parse_data()

    assert '52782797' in sender.running_animations.keys()

    mock_socket.recv.return_value = bytes('END :{"id":"52782797"}', 'utf-8')

    sender.parse_data()

    assert '52782797' not in sender.running_animations.keys()

    assert mock_callback.called


def test_parse_data_bad_data_type(caplog):
    pass
