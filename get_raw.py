from animatedledstrip import AnimationSender, Command
from animatedledstrip.json_encoder import ALSJsonEncoder

ip = input('Enter IP address: ')
port = int(input('Enter port: '))

sender = AnimationSender(ip, port)
encoder = ALSJsonEncoder()


def receive(data: bytes):
    print(str(data) + '\n')


sender.on_receive_callback = receive

sender.start()

while True:
    cmd = input('Enter command: ')
    if cmd != '':
        sender.send(Command(cmd))
