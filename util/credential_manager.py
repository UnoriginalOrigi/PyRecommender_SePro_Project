from util.MyAES import encryptText, decryptText
import re
from getpass import getpass
import spotipy
from spotipy.oauth2 import SpotifyClientCredentials

#input validation constants
EXPECTED_INPUT_LENGTH = 32
BASE62_INVALID_SYMBOLS = "[^A-Za-z0-9]"

def credential_input(): #Adding credentials and input validation
    try:
        print("Input your Client ID token:")
        client_id_input = input()
        if len(client_id_input) != EXPECTED_INPUT_LENGTH:
            raise OverflowError
        if re.findall(BASE62_INVALID_SYMBOLS,client_id_input):
            raise ValueError
        print("Input your Client Secret token:")
        client_secret_input = getpass()
        if len(client_secret_input) != EXPECTED_INPUT_LENGTH:
            raise OverflowError
        if re.findall(BASE62_INVALID_SYMBOLS,client_secret_input):
            raise ValueError
        client_id = client_id_input
        client_secret = client_secret_input
    except OverflowError: #Input validation
        print("Error 2: Input is not correct length")
        client_id = "-1"
        client_secret = "-1"
    except ValueError: #Input validation
        print("Error 3: Invalid Base62 characters detected")
        client_id = "-1"
        client_secret = "-1"
    except TypeError: #Input validation
        print ("Error 4: Input is invalid format")
        client_id = "-1"
        client_secret = "-1"
    
    return client_id, client_secret

def credential_loader(params): #Loads previously saved encrypted credentials
    with open("client_info.txt","r") as f:
        client_id = f.readline()
        client_id = client_id.strip()
        client_secret = f.readline()
        client_secret = client_secret.strip()
        client_secret = decryptText(client_secret, params=params)
    return client_id, client_secret

def login_attempt(client_id,client_secret, params): #Attempt to login to Spotify API with provided client_id and client_secret 
    auth_manager = SpotifyClientCredentials(client_id=client_id,client_secret=client_secret)
    auth_manager.get_access_token(as_dict=False) #test to see if login was successful
    sp = spotipy.Spotify(auth_manager=auth_manager)
    client_secret_enc = encryptText(data = client_secret, params=params)
    with open("client_info.txt","w") as f:
        f.write("{}\n{}".format(client_id,client_secret_enc))

    return sp