from led_client import AnimationSender


sender = AnimationSender("10.0.0.55", 6)


def receive(data: bytes):
    print(str(data) + '\n')


sender.receiveCallback = receive

sender.start()

while True:
    sender.send_data('CMD :' + input())
