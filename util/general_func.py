import os

INPUT_SIZE = 64

def cls(): #command line clearing, purely aesthetic
    os.system('cls' if os.name=='nt' else 'clear')

def clean_up(): #Deletion of .cache file
    if(os.path.exists(".cache")):
        os.remove(".cache")

def action_input(): #General action check to find valid integer input
    try:
        action = int(input())
    except (ValueError, EOFError):
        cls()
        print("Error 1: Input is not a valid integer")
        action = -1
    return action

def related_artists_search(sp, search_query): #related artist lookup using Spotify API
    search_query = "artist:"+search_query
    results = sp.search(q=search_query, limit=1)
    for idx, track in enumerate(results['tracks']['items']):
        related_artists = sp.artist_related_artists(track['album']['artists'][0]['id'])
    return related_artists
