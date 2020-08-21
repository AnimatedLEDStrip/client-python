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
import socket
from unittest import mock

from animatedledstrip import AnimationSender, AnimationData, Direction, ParamUsage


def test_constructor():
    sender = AnimationSender('10.0.0.254', 5)

    assert sender.address == '10.0.0.254'
    assert sender.port == 5
    assert sender.connected is False
    assert sender.recv_thread is None
    assert sender.running_animations == {}
    assert sender.strip_info is None
    assert sender.supported_animations == []
    assert sender.on_receive_callback is None
    assert sender.on_new_animation_data_callback is None
    assert sender.on_new_animation_info_callback is None
    assert sender.on_new_end_animation_callback is None
    assert sender.on_new_section_callback is None
    assert sender.on_new_strip_info_callback is None


def test_send_animation():
    data = AnimationData().json()
    sender = AnimationSender('10.0.0.254', 5)
    with mock.patch.object(sender, 'connection') as mock_socket:
        sender.send_data(data)
        assert mock_socket.sendall.called
        assert mock_socket.called_with(data)


def test_parse_data_animation_data():
    sender = AnimationSender('10.0.0.254', 5)

    with mock.patch.object(sender, 'connection') as mock_socket:
        with mock.patch.object(sender, 'newAnimationDataCallback') as mock_callback:
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


def test_parse_data_animation_info():
    sender = AnimationSender('10.0.0.254', 5)

    with mock.patch.object(sender, 'connection') as mock_socket:
        with mock.patch.object(sender, 'newAnimationInfoCallback') as mock_callback:
            mock_socket.recv.return_value = bytes('AINF:{"name":"Multi Pixel Run","abbr":"MPR",'
                                                  '"description":"Similar to [Pixel Run](Pixel-Run) but with multiple '
                                                  'LEDs at a specified spacing.","signatureFile":"multi_pixel_run.png",'
                                                  '"repetitive":true,"minimumColors":1,"unlimitedColors":false,'
                                                  '"center":"NOTUSED","delay":"USED","direction":"USED",'
                                                  '"distance":"NOTUSED","spacing":"USED","delayDefault":100,'
                                                  '"distanceDefault":-1,"spacingDefault":3}', 'utf-8')

            sender.parse_data()

            assert len(sender.supported_animations) == 1

            info = sender.supported_animations[0]

            assert info.name == 'Multi Pixel Run'
            assert info.abbr == 'MPR'
            assert info.description == 'Similar to [Pixel Run](Pixel-Run) but with multiple LEDs ' \
                                       'at a specified spacing.'
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

            mock_socket.recv.return_value = bytes('AINF:{"name":"Multi Pixel Run","abbr":"MPR",'
                                                  '"description":"Similar to [Pixel Run](Pixel-Run) but with multiple '
                                                  'LEDs at a specified spacing.","signatureFile":"multi_pixel_run.png",'
                                                  '"repetitive":false,"minimumColors":1,"unlimitedColors":true,'
                                                  '"center":"USED","delay":"USED","direction":"USED",'
                                                  '"distance":"USED","spacing":"USED","delayDefault":1000,'
                                                  '"distanceDefault":10,"spacingDefault":30}', 'utf-8')

            sender.parse_data()

            assert len(sender.supported_animations) == 2

            info2 = sender.supported_animations[1]

            assert info2.name == 'Multi Pixel Run'
            assert info2.abbr == 'MPR'
            assert info2.description == 'Similar to [Pixel Run](Pixel-Run) but with multiple LEDs ' \
                                        'at a specified spacing.'
            assert info2.signature_file == 'multi_pixel_run.png'
            assert info2.repetitive is False
            assert info2.minimum_colors == 1
            assert info2.unlimited_colors is True
            assert info2.center is ParamUsage.USED
            assert info2.delay is ParamUsage.USED
            assert info2.direction is ParamUsage.USED
            assert info2.distance is ParamUsage.USED
            assert info2.spacing is ParamUsage.USED
            assert info2.delay_default == 1000
            assert info2.distance_default == 10
            assert info2.spacing_default == 30

            assert mock_callback.called
            assert mock_callback.called_with(info2)


def test_parse_data_end_animation():
    sender = AnimationSender('10.0.0.254', 5)

    with mock.patch.object(sender, 'connection') as mock_socket:
        with mock.patch.object(sender, 'newEndAnimationCallback') as mock_callback:
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


def test_parse_data_section():
    sender = AnimationSender('10.0.0.254', 5)

    with mock.patch.object(sender, 'connection') as mock_socket:
        with mock.patch.object(sender, 'newSectionCallback') as mock_callback:
            mock_socket.recv.return_value = bytes('SECT:{"physicalStart":0,"numLEDs":240,"name":"section",'
                                                  '"startPixel":0,"endPixel":239}',
                                                  'utf-8')

            sender.parse_data()

            assert 'section' in sender.sections

            sect = sender.sections['section']

            assert sect.name == 'section'
            assert sect.start_pixel == 0
            assert sect.end_pixel == 239
            assert sect.physical_start == 0
            assert sect.num_leds == 240

            assert mock_callback.called
            assert mock_callback.called_with(sect)


def test_parse_data_strip_info():
    sender = AnimationSender('10.0.0.254', 5)

    with mock.patch.object(sender, 'connection') as mock_socket:
        with mock.patch.object(sender, 'newStripInfoCallback') as mock_callback:
            mock_socket.recv.return_value = bytes('SINF:{"numLEDs":240,"pin":12,"imageDebugging":false,'
                                                  '"fileName":"test.csv","rendersBeforeSave":1000,"threadCount":100}',
                                                  'utf-8')

            sender.parse_data()

            assert sender.strip_info is not None

            info = sender.strip_info

            assert info.num_leds == 240
            assert info.pin == 12
            assert info.image_debugging is False
            assert info.file_name == 'test.csv'
            assert info.renders_before_save == 1000
            assert info.thread_count == 100

            assert mock_callback.called
            assert mock_callback.called_with(info)

            mock_socket.recv.return_value = bytes('SINF:{"numLEDs":20,"pin":null,"imageDebugging":true,'
                                                  '"fileName":null,"rendersBeforeSave":null,"threadCount":20}',
                                                  'utf-8')

            sender.parse_data()

            assert sender.strip_info is not None

            info2 = sender.strip_info

            assert info2.num_leds == 20
            assert info2.pin is None
            assert info2.image_debugging is True
            assert info2.file_name is None
            assert info2.renders_before_save is None
            assert info2.thread_count == 20

            assert mock_callback.called
            assert mock_callback.called_with(info2)


def test_parse_data_bad_data_type(caplog):
    pass
