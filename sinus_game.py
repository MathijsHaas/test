''' hier moet een soort van socket communicatie gaan plaatsvinden met de processing file. Deze file gedraagt zich als de client waar de sinus processing file zich als server gedraagd. zodra de "server" een start signaal krijgt als de spy_knobs goed staan, gaat het sinus spel van start. zodra het spel is afgerond krijgt deze file een antwoord en is het dus klaar om door te gaan.'''
import multiprocessing

game_won = multiprocessing.Value('i', 0)


def main():
    host = '127.0.0.1'  # localhost
    port = 5000  # has to be the same as in the sine_test.pde

    s = socket.socket()
    s.connect((host, port))

    message = "start"
    s.send(message.encode('utf-8'))
    data = s.recv(1024).decode('utf-8')
    game_won.value = 1  # recv waits until there is an anwser for the server. because there is a reply, it means the game finished.
    print("sinus game won")
    s.close()


if __name__ == '__main__':
    main()
