import os
import spotipy
from spotipy.oauth2 import SpotifyClientCredentials
from util.MyAES import generateKey, loadKey
from util.credential_manager import credential_input, credential_loader, login_attempt
from util.general_func import clean_up, cls, action_input, related_artists_search, INPUT_SIZE
import re

def CLI_program():
    print("Welcome to the Spotify Recommender CLI!")
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
                        if client_secret == "":
                            print("Saved credentials corrupted. Removing file.")
                            if(os.path.exists("client_info.txt")):
                                os.remove("client_info.txt")
                            break
                        else:
                            break
                    elif input_action == 'n':
                        cls()
                        client_id, client_secret = credential_input(params=params)
                        break
                    else:
                        print("Invalid input")
            if not os.path.exists("client_info.txt") and not os.path.exists(".cache"):
                client_id, client_secret = credential_input(params=params)
            try:
                sp = login_attempt(client_id, client_secret)
                while True:
                    print("1 - Song/Artist search, 2 - Recommend similar artists")
                    action = input()
                    if action == "1":
                        while True:
                            search_query = input("Enter search query: ")
                            if len(search_query) > INPUT_SIZE:
                                search_query = ""
                                print("Input too long. Input size <=",INPUT_SIZE)
                            elif len(search_query) == 0:
                                print("No Input given")
                            else:
                                break
                        results = sp.search(q=search_query, limit=10)
                        for idx, track in enumerate(results['tracks']['items']):
                            print(idx+1, track['name'], "-", track['artists'][0]['name'])
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
                        while True:
                            search_query = input("Enter an Artist: ")
                            if len(search_query) > INPUT_SIZE:
                                search_query = ""
                                print("Input too long. Input size <=",INPUT_SIZE)
                            elif len(search_query) == 0:
                                print("No Input given")
                            else:
                                break
                        related_artists = related_artists_search(sp, search_query)
                        future_lookup = []
                        for idx, artist in enumerate(related_artists['artists']):
                            print(idx+1, artist['name'])
                            future_lookup.append(artist['name'])
                        while True:
                            action = input("Lookup songs from a related artist? ([y]/n) ").lower()
                            if action == "":
                                action = "y"
                            if action == "y":
                                id_search = input("Type in the ID of the artist: ")
                                if not re.findall("[^0-9]",id_search) and int(id_search) <= 20:
                                    id_search = "artist:"+future_lookup[int(id_search)-1]
                                    results = sp.search(q=id_search, limit=10)
                                    for idx, track in enumerate(results['tracks']['items']):
                                        print(idx+1, track['name'], "-", track['artists'][0]['name'])
                                else:
                                    print("Invalid input")
                                action = input("Another? ([y]/n) ").lower()
                                if action == "":
                                    action = "y"
                                if action == "y":
                                    cls()
                                    for i in range(0,len(future_lookup)):
                                        print(i+1, future_lookup[i])
                                elif action == "n":
                                    cls()
                                    break
                                else:
                                    print("Invalid input") 

                            elif action == "n":
                                cls()
                                break
                            else:
                                print("Invalid input") 
                        
                        action = input("Another Search? ([y]/n) ").lower()
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