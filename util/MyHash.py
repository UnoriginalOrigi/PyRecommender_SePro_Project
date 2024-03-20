import hashlib
import base64 as b64

def hashText(paraText):
    #prepare the hashing tool and get text from file
    hasher = hashlib.sha256()
    hasher.update(paraText)

    #get the digest of the text
    hash = hasher.digest()
    hash = b64.b64encode(hash)
    return hash

