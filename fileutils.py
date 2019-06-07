
# coding: utf-8

# In[66]:

import sqlite3
import pickle
from shutil import copyfile
import os
import subprocess
import time
import random
import string


# In[2]:

def get_list():
    conn = sqlite3.connect('files.db')
    c = conn.cursor()
    query = "SELECT filename FROM file2key"
    c.execute(query)
    l = c.fetchall()
    conn.close()
    filelist = []
    for x in l:
        print(x[0])
        filelist.append(x[0])
    return filelist


# In[75]:

def pull_file(filename):
    conn = sqlite3.connect('files.db')
    c = conn.cursor()
    query = "SELECT key, piecelistname FROM file2key WHERE filename = '" + filename + "';"
    #print(query)
    c.execute(query)
    l = c.fetchall()
    conn.close()
    success = 0
    for x in l:
        success = 1
        key = x[0]
        piecelist = x[1]
        copyfile("/tmp/outputs/" + piecelist, 
                 "./" + piecelist)
        #print(piecelist)
        with open(piecelist, "rb") as f:
            pieces = pickle.load(f)
        #print(pieces)
        command = "cat "
        for piece in pieces:
            command += "/tmp/outputs/" + piece + " "
        
        command += " | ./hpenc -k " + key + " -d " + " | tar xvaf -"
        #print(command)
        os.system(command)
        os.remove("./" + piecelist)
    if success:
        print("Successful")
    else:
        print("Not Successful")


# In[54]:

def delete_file(filename):
    conn = sqlite3.connect('files.db')
    c = conn.cursor()
    query = "SELECT key, piecelistname FROM file2key WHERE filename = '" + filename + "';"
    #print(query)
    c.execute(query)
    l = c.fetchall()
    query = "DELETE  FROM file2key WHERE filename = '" + filename + "';"
    c.execute(query)
    conn.commit()
    conn.close()
    for x in l:
        key = x[0]
        piecelist = x[1]
        copyfile("/tmp/outputs/" + piecelist, 
                 "./" + piecelist)
        #print(piecelist)
        with open(piecelist, "rb") as f:
            pieces = pickle.load(f)
        #print(pieces)
        for piece in pieces:
            os.remove("/tmp/outputs/"+piece)
        os.remove("/tmp/outputs/"+piecelist)
        os.remove("./" + piecelist)


# In[68]:

def push_file(filename):
    conn = sqlite3.connect('files.db')
    c = conn.cursor()

    a = subprocess.check_output("./hpenc psk",  shell=True)
    key = a.split()[-1]
    #print(key.decode("utf-8"))
    #filename = sys.argv[1]
    os.system("mkdir output")
    command = "tar cvf - " + filename + " | ./hpenc -b 16M -k " + key.decode("utf-8")  +" | split -b 2M - output/"
    os.system(command)
    l = []
    origfilename = filename.split("/")[-1]
    for x in sorted(os.listdir("output")):
        filename = str(time.time()) + ''.join(random.SystemRandom().choice(string.ascii_uppercase + string.ascii_lowercase + string.digits) for _ in range(10))
        #print(x, filename)
        os.system("mv output/" + x + " /tmp/outputs/" +  filename)
        l.append(filename)

    piecelistname = str(time.time()) + ''.join(random.SystemRandom().choice(string.ascii_uppercase + string.ascii_lowercase + string.digits) for _ in range(10))
    piecelist = open("./output/" + piecelistname, 'wb')
    pickle.dump(l, piecelist)
    piecelist.close()
    copyfile("./output/" + piecelistname, "/tmp/outputs/"+piecelistname)

    try:
        query = "INSERT INTO file2key VALUES('" + origfilename + "', '" + key.decode("utf-8") +  "', '" +  piecelistname + "')"
        #print(query)
        c.execute(query)
    except sqlite3.IntegrityError:
        print("Erroe")
    except Exception:
        try:    
            c.execute('''CREATE TABLE file2key
                 (filename text PRIMARY KEY, key text, piecelistname text)''')
        except:
            pass

        query = "INSERT INTO file2key VALUES('" + origfilename + "', '" + key.decode("utf-8") +  "', '" +  piecelistname + "')"
        c.execute(query)
    conn.commit()
    conn.close()

    os.system("rm -rf  output")


# In[81]:

#pull_file("teamviewer_13.1.8286_amd64.deb")


# In[ ]:



