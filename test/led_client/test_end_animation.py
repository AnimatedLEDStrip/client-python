from led_client.end_animation import EndAnimation


def test_end_animation_json():
    end = EndAnimation()
    end.id = '123456'

    json = end.json()

    assert json == 'END :{"id":"123456"}'
