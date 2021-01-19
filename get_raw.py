from animatedledstrip import AnimationSender, Command
from animatedledstrip.json_encoder import ALSJsonEncoder

sender = AnimationSender("10.0.0.91", 6)
encoder = ALSJsonEncoder()


def receive(data: bytes):
    print(str(data) + '\n')


sender.on_receive_callback = receive

sender.start()

while True:
    sender.send_data(encoder.encode(Command(input())))
