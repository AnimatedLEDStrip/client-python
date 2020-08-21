from animatedledstrip import AnimationSender


sender = AnimationSender("10.44.167.23", 6)


def receive(data: bytes):
    print(str(data) + '\n')


sender.on_receive_callback = receive

sender.start()

while True:
    sender.send_data('CMD :' + input())
