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

def credential_input():
    try:
        print("Input your client id token:")
        client_id_input = input()
        if len(client_id_input) > MAXIMUM_INPUT_LENGTH:
            raise OverflowError
        print("Input your client secret token:")
        client_secret_input = input()
        if len(client_secret_input) > MAXIMUM_INPUT_LENGTH:
            raise OverflowError
        with open("client_info.txt","w") as f:
            f.write(client_id_input)
            f.write("\n")
            f.write(client_secret_input)
        client_id = client_id_input
        client_secret = client_secret_input
    except OverflowError:
        print("Error 2: Input higher than maximum possible length")
        client_id = "-1"
        client_secret = "-1"
    
    return client_id, client_secret

def credential_loader():
    with open("client_info.txt","r") as f:
        client_id = f.readline()
        client_id = client_id.strip()
        client_secret = f.readline()
        client_secret = client_secret.strip()
    return client_id, client_secret

def main():
    print("Welcome to the Spotify Recommender Prototype!")
    while(True):
        action = action_input()
        if action == 0:
            print("Program end!")
            break
        elif action == 1:
            if os.path.exists("client_info.txt"):
                while True:
                    print("Saved credentials found, use saved credentials? y/n")
                    input_action = input().lower()
                    if input_action == 'y':
                        cls()
                        print("Using saved credentials")
                        client_id, client_secret = credential_loader()
                        break
                    elif input_action == 'n':
                        cls()
                        client_id, client_secret = credential_input()
                        break
                    else:
                        print("Invalid input")
            try:
                sp = spotipy.Spotify(auth_manager=SpotifyClientCredentials(client_id=client_id,client_secret=client_secret))
                search_query = input("Login successful, enter search query: ")
                results = sp.search(q=search_query, limit=20)
                for idx, track in enumerate(results['tracks']['items']):
                    print(idx+1, track['name'])
            except spotipy.oauth2.SpotifyOauthError:
                print("Invalid Credentials Given, failed to connect")
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