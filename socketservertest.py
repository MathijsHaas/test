import socket
import time


def main():
    host = '127.0.0.1'
    port = 5006

    s = socket.socket()
    s.bind((host, port))

    s.listen(1)
    c, addr = s.accept()
    print ("connection from: " + str(addr))

    while True:
        data = c.recv(1024).decode('utf-8')
        if not data:
            break
        if data == "start":
            print("1")
            time.sleep(1)
            print("2")
            time.sleep(1)
            print("3")
            c.send(data.encode('utf-8'))
        else:
            print ("from connected user: " + data)
            data = data.upper()
            print("sending: " + data)
            c.send(data.encode('utf-8'))
    c.close()


if __name__ == '__main__':
    main()
