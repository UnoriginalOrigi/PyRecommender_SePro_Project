# Secure Programming Final Project

This is a project for the course Secure Programming in Tampere University. In this code a securely implemented music recommendation system is provided. The code has been tested with Python 3.8 and Python 3.9 on Windows and Windows Subsystems for Linux (WSL 2.0). To make use of the code please install the requirements by running:

```
pip install -r requirements.txt
```

To run the code run the command:

```
python3 main.py
```

Breakdown of the project files and directories:
```
main.py -- core execution of the project, core functionality is written here.
/util -- folder containing utilities for credential input, loading as well as secure storage and communication
    |- credential_manager.py -- code for inputing and saving new credential data as well as loading prior credentials 
    |- MyAES.py -- utilities for key generation/loading, encryption and decryption with AES-256-CBC.
    |- MyHash.py -- utilities for creating hashes with SHA-256.
```

Below will be the list of OWASP vulnerabilities, which have been addressed in the code as well as a description of the test ran on the final code:

