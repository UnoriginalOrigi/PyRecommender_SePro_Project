import os
import spotipy
from spotipy.oauth2 import SpotifyClientCredentials

MAXIMUM_INPUT_LENGTH = 512

"""
Error Codes:
1. Expected integer, received invalid input
2. Input is too long, possible overflow
3.

"""

def cls(): #command line clearing, purely estetic
    os.system('cls' if os.name=='nt' else 'clear')

def action_input():
    print("Choose your action:\n1. Login\n0. Quit")
    try:
        action = int(input())
    except (ValueError, EOFError):
        cls()
        print("Error 1: Input is not a valid integer")
        action = -1

    return action

def main():
    print("Welcome to the Spotify Recommender Prototype!")

    while(True):
        action = action_input()
        if action == 0:
            print("Program end!")
            break
        elif action == 1:
            print("Input your client id token")
            try:
                client_id_input = input()
                if len(client_id_input) > MAXIMUM_INPUT_LENGTH:
                    raise OverflowError
                print("Input your client secret token")
                client_secret_input = input()
                if len(client_secret_input) > MAXIMUM_INPUT_LENGTH:
                    raise OverflowError
                with open("client_info.txt","w") as f:
                    f.write(client_id_input)
                    f.write("\n")
                    f.write(client_secret_input)
            except OverflowError:
                print("Error 2: Input higher than maximum possible length")

        elif action == -1:
            print("Error encountered")
        else:
            cls()
            print("Input out of range")

if __name__ == "__main__":
    cls()
    try:
        main()
    except KeyboardInterrupt:
        print("Keyboard interrupt detected, force closing program!")