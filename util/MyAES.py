from Crypto.Cipher import AES
import Crypto.Util.Padding  as Padding
from Crypto.Random import get_random_bytes
from base64 import b64encode, b64decode
import json

BLOCK_SIZE = 16
LEN_BYTES = 32

def generateKey():
    #generating key and saving it to file
    key = get_random_bytes(LEN_BYTES)
    params = json.dumps({'key': b64encode(key).decode('utf-8')})
    with open("key.json", 'w') as file_o:
        json.dump(params, file_o)
    return json.loads(params)

def loadKey():
    try:
        with open("key.json","r") as file_i:
            params = json.load(file_i)
        return json.loads(params)
    except FileNotFoundError:
        print("File corrupted or could not be read.")
        return -1

def encryptText(data, params):
    data = Padding.pad(bytes(data,"utf-8"), BLOCK_SIZE)
    cipher = AES.new(b64decode(params["key"].encode('utf-8')), AES.MODE_CBC)
    ct = cipher.encrypt(data)
    ct = "".join((b64encode(cipher.iv).decode('utf-8'),b64encode(ct).decode('utf-8'))) #encoding ciphertext to BASE64
    return ct

def decryptText(data, params):
    iv,ct = data[:24],data[24:]
    try:
        cipher = AES.new(b64decode(params["key"].encode('utf-8')), AES.MODE_CBC, iv=b64decode(iv.encode('utf-8')))
        ct = b64decode(ct.encode('utf-8'))#decoding ciphertext from BASE64
        pt = cipher.decrypt(ct)
        pt = Padding.unpad(pt, BLOCK_SIZE).decode('utf-8')
    except ValueError:
        print("Invalid values for key or IV")
        pt = ""
    return pt