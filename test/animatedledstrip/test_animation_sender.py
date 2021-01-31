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

from animatedledstrip import AnimationSender
from animatedledstrip.animation_to_run_params import AnimationToRunParams


def test_constructor():
    sender = AnimationSender('10.0.0.254', 5)

    assert sender.address == '10.0.0.254'
    assert sender.port == 5
    assert sender.connected is False
    # noinspection PyProtectedMember
    assert sender._recv_thread is None
    assert sender.running_animations == {}
    assert sender.strip_info is None
    assert sender.supported_animations == []
    assert sender.on_receive_callback is None
    assert sender.on_new_animation_info_callback is None
    assert sender.on_new_current_strip_color_callback is None
    assert sender.on_new_end_animation_callback is None
    assert sender.on_new_message_callback is None
    assert sender.on_new_running_animation_params_callback is None
    assert sender.on_new_section_callback is None
    assert sender.on_new_strip_info_callback is None


def test_send_animation():
    data = AnimationToRunParams()
    sender = AnimationSender('10.0.0.254', 5)
    with mock.patch.object(sender, 'connection') as mock_socket:
        sender.send(data)
        assert mock_socket.sendall.called
        assert mock_socket.called_with(data)


def test_parse_data_running_animation_params():
    sender = AnimationSender('10.0.0.254', 5)

    with mock.patch.object(sender, 'connection') as mock_socket:
        with mock.patch.object(sender, 'on_new_running_animation_params_callback') as mock_callback:
            mock_socket.recv.return_value = bytes('{"type":"AnimationToRunParams",'
                                                  '"animation":"9kd`O8l*I*Nqn-)Dw71GD-xmY3-lmnjcJT7kMBS5Cba(g+r+@wY:W)8yBR=4%<9kyB6_9R2aNa;OU=hkdgl)y*au2u]lXyy&g",'
                                                  '"colors":[{"type":"ColorContainer","colors":[]},{"type":"PreparedColorContainer","colors":[],"originalColors":[]},{"type":"ColorContainer","colors":[0,1,15843857,13946345,9074689,2562712,1027499,9244430,8893055,16073827,14784411,13222205,66706,10031368,11252361,632676,11157697,10051847,5960558,4342536,5890090,5609224,13912345,16246967,1637565,8752417,2856813,8861040,8164616,13280036,14718872,528433,4625582,498958,8080174,5119595,13445645,5023714,15039110,8485341,7096991,3698225,9231731,10216078,10217872,8268689,2046631,2069256,16030237,5221855,9528467,8815970,6533208,10843263,5067777,4060438,10687535,9275585,9544718,10381711,1902397,11198771,2315335,5731048,12368367,4466783,13824556,12687108,12158936,14026502,13597282,13286090,12458072,922676,15353097,15223635,5561265,14177159,15708639,8187309,6333942,15765776,217633,15130521,6974357,773354,6578783,7349853,10655468,1088090,3242856,15839618,13308174]},{"type":"PreparedColorContainer","colors":[],"originalColors":[]},{"type":"PreparedColorContainer","colors":[0,1,11719442],"originalColors":[]}],'
                                                  '"id":"/@A<wq0?lRF=7ZdJ%4VgVne9",'
                                                  '"section":"/Oj;2&J`tD>fHvHVKY9rR3iVWFYCPh`&hAlKRl/4keTmEiu1",'
                                                  '"runCount":-1469019058,'
                                                  '"direction":"FORWARD",'
                                                  '"intParams":{"T,F_GzRCXLn>[.j":-1812210955,"zWP%q=xzCk2i+[IYs&GFibPT6+Z@gH/uL7(Aq*O<.VY%N!m4<IpO@IyHqOB48p":-2056817743},"doubleParams":{"9xvDP-eW??a3mc*W(uhvg&x@OLj9IE;363MHo<W^=+%+nT79^ BQU`1`ySqPrpf9%yPshKcBh5K!)>Vm9:, DSA.":8.249069344234898E307,"t8":-1.578395092499425E308,"hRuDDs?I>UL4`<Xwwx":-1.5274687377156308E308,"s6+Zd(Hdt%6w/tpPg<XV)s.oeb;exhFN4bn`OHC[;hw[5X4l?j)7%%s[_E_%R1M!/s:5MrT>U)8lgKgFyN+e`=+n47":-9.554323788272268E307},"stringParams":{"5NnA%8MK F<SHZm7[yv(rH4Sr28_arLQe]v@n^SEwHd*GXdISQl.Fo?hAiXVX*":"[B>&mBuu-QS1un^Lc*Hgp,I*of7l)*","(Q(kzTGjum[Tx.nNWBCY+aT2z2;2G6I-jVhQ-C_2>xlhQhrdJzZs96&LA!GCE@>y12dkTL_X&":":(ijdzsznr@t=twT3N)LQ8Vq)<[@My%ce5NxVN2t>o(3Y7WOrD1XKYU)MIOJTAMOJ&P8fv.O[:7d","N?J&;UW+L>vDIp6!kj;N)dThU(L/z":".!5LDN85+Ca0<WM4,kL=2",",7t7Rf2JTP<fJGAchY=lR4!V:JmImZE^4OdhwQpCW[y[pz":"vKSbRW9UU2*T M*jmm@7q(w4s?<7U<c1-n<hku ?oxd7VrU1C5EL`SB]pFpYV]"},"locationParams":{"JO`LfQjf":{"x":3.509781464796749E8,"y":1.2430629070562382E9,"z":-1.328318108295171E9,"coordinates":"3.509781464796749E8, 1.2430629070562382E9, -1.328318108295171E9"},"z6k4Y!9sSQA*OtD:Oy":{"x":2.3013269865412906E7,"y":1.4453891262245123E9,"z":2.0742815763795311E9,"coordinates":"2.3013269865412906E7, 1.4453891262245123E9, 2.0742815763795311E9"}},"distanceParams":{"fDFHV.P4e+B+(NNSVJ84I_8QsG*":{"type":"PercentDistance","x":-7.418475505422992E8,"y":-1.9826226634997616E9,"z":1.1803587457015536E9,"coordinates":"-7.418475505422992E8, -1.9826226634997616E9, 1.1803587457015536E9","maxDistance":1.1803587457015536E9},"jDo^u @Z?yE.Rp]>zvC[De^Lq0;<6ZQR/OU;Z[KM!(.Wb,in[kKFpSOf_fuWkVZ4e%L4M":{"type":"PercentDistance","x":1.1264941573376575E9,"y":-3.581055887112018E8,"z":1.3694952878726428E9,"coordinates":"1.1264941573376575E9, -3.581055887112018E8, 1.3694952878726428E9","maxDistance":1.3694952878726428E9}},"rotationParams":{},"equationParams":{}};;;', 'utf-8')

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
        with mock.patch.object(sender, 'on_new_animation_info_callback') as mock_callback:
            mock_socket.recv.return_value = bytes('AINF:{"name":"Multi Pixel Run","abbr":"MPR",'
                                                  '"description":"Similar to [Pixel Run](Pixel-Run) but with multiple '
                                                  'LEDs at a specified spacing.","signatureFile":"multi_pixel_run.png",'
                                                  '"repetitive":true,"minimumColors":1,"unlimitedColors":false,'
                                                  '"center":"NOTUSED","delay":"USED","direction":"USED",'
                                                  '"distance":"NOTUSED","spacing":"USED","delayDefault":100,'
                                                  '"distanceDefault":-1,"spacingDefault":3};;;', 'utf-8')

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
                                                  '"distanceDefault":10,"spacingDefault":30};;;', 'utf-8')

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


def test_parse_data_command(caplog):
    sender = AnimationSender('10.0.0.254', 5)

    with mock.patch.object(sender, 'connection') as mock_socket:
        mock_socket.recv.return_value = bytes('CMD :{"command":"test_command"};;;', 'utf-8')

        sender.parse_data()

        log_messages = {(log.msg, log.levelname) for log in caplog.records}

        assert log_messages == {('Receiving Command is not supported by client', 'WARNING')}


def test_parse_data_end_animation():
    sender = AnimationSender('10.0.0.254', 5)

    with mock.patch.object(sender, 'connection') as mock_socket:
        with mock.patch.object(sender, 'on_new_end_animation_callback') as mock_callback:
            mock_socket.recv.return_value = bytes('DATA:{"animation":"Meteor","baseDelay":10,"center":120,'
                                                  '"colors":[{"colors":[16711680]}],"continuous":null,'
                                                  '"delayMod":1.0,"direction":"FORWARD","distance":240,'
                                                  '"id":"52782797","section":"","spacing":3};;;', 'utf-8')

            sender.parse_data()

            assert '52782797' in sender.running_animations.keys()

            mock_socket.recv.return_value = bytes('END :{"id":"52782797"};;;', 'utf-8')

            sender.parse_data()

            assert '52782797' not in sender.running_animations.keys()

            assert mock_callback.called


def test_parse_data_message():
    sender = AnimationSender('10.0.0.254', 5)

    with mock.patch.object(sender, 'connection') as mock_socket:
        with mock.patch.object(sender, 'on_new_message_callback') as mock_callback:
            mock_socket.recv.return_value = bytes('MSG :{"message":"a message"};;;',
                                                  'utf-8')

            sender.parse_data()

            assert mock_callback.called
            assert mock_callback.called_with('a message')


def test_parse_data_section():
    sender = AnimationSender('10.0.0.254', 5)

    with mock.patch.object(sender, 'connection') as mock_socket:
        with mock.patch.object(sender, 'on_new_section_callback') as mock_callback:
            mock_socket.recv.return_value = bytes('SECT:{"physicalStart":0,"numLEDs":240,"name":"section",'
                                                  '"startPixel":0,"endPixel":239};;;',
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
        with mock.patch.object(sender, 'on_new_strip_info_callback') as mock_callback:
            mock_socket.recv.return_value = bytes('SINF:{"numLEDs":240,"pin":12,"imageDebugging":false,'
                                                  '"fileName":"test.csv","rendersBeforeSave":1000,"threadCount":100};;;',
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
                                                  '"fileName":null,"rendersBeforeSave":null,"threadCount":20};;;',
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
    sender = AnimationSender('10.0.0.254', 5)

    with mock.patch.object(sender, 'connection') as mock_socket:
        mock_socket.recv.return_value = bytes('BAD :{};;;', 'utf-8')

        sender.parse_data()

        log_messages = {(log.msg, log.levelname) for log in caplog.records}

        assert log_messages == {('Unrecognized data type: BAD ', 'WARNING')}
