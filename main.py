import os
import spotipy
from spotipy.oauth2 import SpotifyClientCredentials
from util.credential_manager import credential_input, credential_loader
from util.MyAES import encryptText, decryptText, generateKey, loadKey
from util.MyHash import hashText

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
            else:
                cls()
                client_id, client_secret = credential_input()
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