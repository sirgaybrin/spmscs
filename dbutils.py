#!/usr/bin/env python
# coding: utf-8

# In[1]:


import base64
import os
from cryptography.hazmat.backends import default_backend
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives.kdf.pbkdf2 import PBKDF2HMAC
from shutil import copyfile
from shutil import  move
import time
import random
import string


# In[2]:


from cryptography.fernet import Fernet


# In[3]:


def keyderive(passw):
    password_provided = passw
    password = password_provided.encode() # Convert to type bytes
    salt = b'salt_' # CHANGE THIS - recommend using a key from os.urandom(16), must be of type bytes
    kdf = PBKDF2HMAC(
        algorithm=hashes.SHA256(),
        length=32,
        salt=salt,
        iterations=100000,
        backend=default_backend()
    )
    key = base64.urlsafe_b64encode(kdf.derive(password))
    return key


# In[4]:


def decrypt_file(file, key):
    fer = Fernet(key)

    with open(file, 'rb') as f:
        decrypted_file = fer.decrypt(f.read())

    with open("files.db", 'wb') as f:
        f.write(decrypted_file)


# In[5]:


def encrypt_file(file, key, name):
    fer = Fernet(key)
    
    with open(file, 'rb') as f:
        encrypted_file = fer.encrypt(f.read())
    with open(name, 'wb') as f:
        f.write(encrypted_file)


# In[6]:


def fetch_db(password):
    key = keyderive(password)
    try:
        copyfile("/tmp/outputs/"+sorted(os.listdir("/tmp/outputs"))[0], "./encrypteddb")
    except:
        f = open("files.db", "wb")
        f.close()
        encrypt_file("files.db", key, "encrypteddb")
        push_db(password)
    decrypt_file("encrypteddb", key)
    os.remove("encrypteddb")


# In[10]:


def push_db(password):
    key = keyderive(password)
    try:
        filename = sorted(os.listdir("/tmp/outputs"))[0]
    except:
        filename = str(time.time()) + ''.join(random.SystemRandom().choice(string.ascii_uppercase + string.ascii_lowercase + string.digits) for _ in range(10))
    encrypt_file("files.db", key, filename)
    move(filename, "/tmp/outputs/"+filename)
    os.remove("files.db")
    #os.remove(filename)


# In[ ]:




