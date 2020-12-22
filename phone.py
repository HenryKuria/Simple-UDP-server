#!/usr/bin/python3
import socket


class ESocket:
    def __init__(self, phone, host, port, sock=None):
        self.phone = phone
        self.host = host
        self.port = port

        if sock is None:
            self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        else:
            self.sock = sock

    def start(self):
        self.sock.bind((self.host, self.port))

        self.sock.listen(1)

        print("Simple UDP Connection")
        print("Waiting for connection")
        client, addr = self.sock.accept()
        print("{} connected".format(str(addr)))

        while True:
            data = client.recv(1024)

            if data.decode() == 'q':
                client.close()
                break
            else:
                print("Reply: {}".format(data.decode()))
                msg = self.send()

                if msg == 'q':
                    client.send(msg.encode())
                    client.close()
                    break

                client.send(msg.encode())

    def connect(self, host, port):
        try:
            self.sock.connect((host, port))
        except ConnectionRefusedError:
            print("Sorry. Server is down!")
        else:
            print("Edge Connections")
            msg = self.send()
            while msg:
                if msg == 'q':
                    self.sock.send(msg.encode())
                    break
                else:
                    self.sock.send(msg.encode())

                    data = self.sock.recv(1024)
                    print("Reply: {}".format(data.decode()))

                    if data.decode() == 'q':
                        break

                    msg = self.send()

    def send(self):
        msg = input("Send .> ")
        if msg == "":
            print("Empty")
            msg = "#"

        return msg


class Phone:
    def __init__(self, name, host, port):
        self.name = name
        self.sock = ESocket(name, host, port)

    def connect(self, phone):
        host = phone.sock.host
        port = phone.sock.port

        self.sock.connect(host, port)

    def start(self):
        self.sock.start()


if __name__ == '__main__':
    phone = Phone('phone', '192.168.43.51', 8000)  # change the addresses to suit you
    phone2 = Phone('phone2', '192.168.43.51', 8200) # change the addresses to suit you

    print("Simple UDP")
    print("# Start   -- 1")
    print("# Connect -- 2")
    choice = int(input(">. "))

    if choice == 1:
        phone.start()
    elif choice == 2:
        phone = input("Phone: ")

        if phone == "phone2":
            phone.connect(phone2)
