import os
import hashlib
import  sqlite3
import subprocess
import time
import signal
import sys
import string
import random
import pickle
from shutil import copyfile
#os.system("mkdir /tmp/outputs")

#command = './rclone  --config rclone.conf  mount gdrive:encrypt/ /tmp/outputs'
#proc = subprocess.Popen(command, shell=True)
#time.sleep(10)
conn = sqlite3.connect('files.db')
c = conn.cursor()

a = subprocess.check_output("./hpenc psk",  shell=True)
key = a.split()[-1]
#print(key.decode("utf-8"))
filename = sys.argv[1]
os.system("mkdir output")
command = "tar cvf - " + filename + " | ./hpenc -b 16M -k " + key.decode("utf-8")  +" | split -b 2M - output/"
os.system(command)
l = []
origfilename = filename.split("/")[-1]
for x in sorted(os.listdir("output")):
    filename = str(time.time()) + ''.join(random.SystemRandom().choice(string.ascii_uppercase + string.ascii_lowercase + string.digits) for _ in range(10))
    print(x, filename)
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

#os.kill(proc.pid, signal.SIGINT)
#os.system("rmdir /tmp/outputs/ -rf")
