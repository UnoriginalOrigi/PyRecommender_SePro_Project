import os
import spotipy
from spotipy.oauth2 import SpotifyClientCredentials
from util.MyAES import generateKey, loadKey
from util.MyHash import hashText
from util.credential_manager import credential_input, credential_loader

"""
Error Codes:
1. Expected integer, received invalid input
2. Input is incorrect length, possible overflow
3. Invalid characters provided
"""

def cls(): #command line clearing, purely estetic
    os.system('cls' if os.name=='nt' else 'clear')

def clean_up():
    if(os.path.exists(".cache")):
        os.remove(".cache")

def action_input():
    try:
        action = int(input())
    except (ValueError, EOFError):
        cls()
        print("Error 1: Input is not a valid integer")
        action = -1

    return action

def related_artists_search(sp, search_query):
    search_query = "artist:"+search_query
    results = sp.search(q=search_query, limit=1)
    for idx, track in enumerate(results['tracks']['items']):
        related_artists = sp.artist_related_artists(track['album']['artists'][0]['id'])
    return related_artists

def main():
    print("Welcome to the Spotify Recommender Prototype!")
    clean_up()
    if not os.path.exists("key.json"):
        params = generateKey()
    else: 
        params = loadKey()
    while(True):
        print("Choose your action:\n1. Login\n0. Quit")
        action = action_input()
        if action == 0:
            cls()
            print("Program end!")
            clean_up()
            break
        elif action == 1:
            if os.path.exists("client_info.txt") and not os.path.exists(".cache"):
                while True:
                    print("Saved credentials found, use saved credentials? [y]/n")
                    input_action = input().lower()
                    if input_action == "":
                        input_action = "y"
                    if input_action == 'y':
                        cls()
                        print("Using saved credentials")
                        client_id, client_secret = credential_loader(params=params)
                        break
                    elif input_action == 'n':
                        cls()
                        client_id, client_secret = credential_input(params=params)
                        break
                    else:
                        print("Invalid input")
            elif os.path.exists("client_info.txt") and not os.path.exists(".cache"):
                cls()
                client_id, client_secret = credential_input(params=params)
            try:
                auth_manager = SpotifyClientCredentials(client_id=client_id,client_secret=client_secret)
                auth_manager.get_access_token(as_dict=False) #test to see if login was successful
                sp = spotipy.Spotify(auth_manager=auth_manager)
                print("Login Successful.")
                while True:
                    print("1 - Search, 2 - Recommend similar artists")
                    action = input()
                    if action == "1":
                        search_query = input("Enter search query: ")
                        results = sp.search(q=search_query, limit=10)
                        for idx, track in enumerate(results['tracks']['items']):
                            print(idx+1, track['name'])
                        action = input("Another search? ([y]/n) ")
                        if action == "":
                            action = "y"
                        if action == "y":
                            cls()
                        elif action == "n":
                            cls()
                            break
                        else:
                            print("Invalid input")    
                    elif action == "2":
                        search_query = input("Enter an Artist: ")
                        related_artists = related_artists_search(sp, search_query)
                        for idx, artist in enumerate(related_artists['artists']):
                            print(idx+1, artist['name'])
                        action = input("Another search? ([y]/n) ")
                        if action == "":
                            action = "y"
                        if action == "y":
                            cls()
                        elif action == "n":
                            cls()
                            break
                        else:
                            print("Invalid input") 
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
        clean_up()