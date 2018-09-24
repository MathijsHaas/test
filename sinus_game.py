''' hier moet een soort van socket communicatie gaan plaatsvinden met de processing file. Deze file gedraagt zich als de client waar de sinus processing file zich als server gedraagd. zodra de "server" een start signaal krijgt als de spy_knobs goed staan, gaat het sinus spel van start. zodra het spel is afgerond krijgt deze file een antwoord en is het dus klaar om door te gaan.'''
import multiprocessing
import socket
import time

game_won = multiprocessing.Value('i', 0)


def main():
    host = '127.0.0.1'
    port = 10005

    s = socket.socket()
    s.connect((host, port))

    print ("socket connection made and waiting for response")
    message = "start"
    s.send(message.encode('utf-8'))
    data = s.recv(1024)
    data = data.decode('utf-8')
    if data == "done":
        print("received from Sinus processing script: " + data)
        game_won.value = 1
        print ("Sinus game_won.value: ", game_won.value)
    time.sleep(10)  # give blackbox the time to catch up
    s.close()


if __name__ == '__main__':
    main()
