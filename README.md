# Secure Programming (SEPRO) Final Project (PyRecommender)

This is a project for the course COMP.SEC.300 Secure Programming in Tampere University. In this code a securely implemented music recommendation system is provided. The code has been tested with Python 3.8 and Python 3.9 on Windows and Windows Subsystems for Linux (WSL 2.0). To make use of the code please install the requirements by running:

```
pip install -r requirements.txt
```

To run the code run the command:

```
python3 main.py
```

To login to the system you must have access to the Spotify account and obtain a valid client ID and client secret from the developer dashboard as explained in https://developer.spotify.com/.

Breakdown of the project files and directories:
```
main.py -- core execution of the project.
/util -- folder containing utilities for credential input, loading as well as secure storage and communication.
    |- credential_manager.py -- code for inputting and saving new credential data as well as loading prior credentials.
    |- MyAES.py -- utilities for key generation/loading, encryption and decryption with AES-256-CBC.
    |- general_func.py -- interchangeable functions for both CLI and Tkinter implementations.
CLI_implemenatation.py -- CLI implementation of PyRecommender.
tkinter_implementation.py -- Tkinter implementation of PyRecommender.
```

Below will be the list of OWASP vulnerabilities, which have been addressed in the code as well as a description of the test ran on the final code:

```
Vulnerable and Outdated Components -- The code is constructed using Python 3.9 as well as the newest available updates of the requirements.

Identification and Authentication Failures -- Invalid credentials are ignored after testing them, only specific symbols and lengths are allowed into the input fields.

Security Misconfiguration -- the public client ID is available for others to see, but the secret parameter is encrypted with AES-256-CBC. It is assumed the secret key is never shared with the server and the connection is made securely through HTTPS/TLS.

Cryptographic Failures -- Strong symmetric encryption is used with connections made online being trusted to be sent securely through HTTPS/TLS.

Buffer Overflow (off-by-one, memory leakage) -- Built-in security in Python. Additionally, the code checks input sizes as well as inputted symbols to avoid going over specified lengths.
```
