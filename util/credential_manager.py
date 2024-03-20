from util.MyAES import encryptText, decryptText
import re

EXPECTED_INPUT_LENGTH = 32
BASE62_INVALID_SYMBOLS = "[^A-Za-z0-9]"

def credential_input():
    try:
        print("Input your client id token:")
        client_id_input = input()
        if len(client_id_input) != EXPECTED_INPUT_LENGTH:
            raise OverflowError
        if re.findall(BASE62_INVALID_SYMBOLS,client_id_input):
            raise ValueError
        print("Input your client secret token:")
        client_secret_input = input()
        if len(client_secret_input) != EXPECTED_INPUT_LENGTH:
            raise OverflowError
        with open("client_info.txt","w") as f:
            f.write("{}\n{}".format(client_id_input,client_secret_input))
        client_id = client_id_input
        client_secret = client_secret_input
    except OverflowError:
        print("Error 2: Input is not correct length")
        client_id = "-1"
        client_secret = "-1"
    except ValueError:
        print("Error 3: Invalid Base62 characters detected")
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