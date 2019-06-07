
# coding: utf-8

# In[2]:

import tkinter
import dbutils
import fileutils
from tkinter import filedialog


# In[84]:

def filepick():
    global filename
    filename = filedialog.askopenfilename(initialdir = "~/")


# In[85]:

def fetch_files(listbox):
    listbox.delete(0, tkinter.END)
    filelist = fileutils.get_list()
    for x in filelist:
        listbox.insert(tkinter.END,x)


# In[130]:

window = tkinter.Tk()


# In[131]:

l1 = tkinter.Label(window, text="Enter Password")
l1.grid(column=0, row=0)


# In[132]:

txt = tkinter.Entry(window, width = 10)
txt.grid(column=1, row=0)


# In[133]:

bt = tkinter.Button(window, text="Fetch DataBase",command=lambda: dbutils.fetch_db(txt.get()))
bt.grid(column=1,row=1)


# In[134]:

global filename
filename = ""
btupload_start = tkinter.Button(window, text="Choose file", command=lambda: filepick())
btupload_start.grid(column=0, row=2)


# In[135]:

bt_upload = tkinter.Button(window, text="Upload", command=lambda: fileutils.push_file(filename))
bt_upload.grid(column=0, row=3)


# In[136]:

bt_delete = tkinter.Button(window, text="Delete", command = lambda: fileutils.delete_file(listbox.get(tkinter.ACTIVE)))
bt_delete.grid(column=1, row=5)


# In[137]:

listbox = tkinter.Listbox(window)
listbox.grid(column=1, row=3)


# In[138]:

btdownload_start = tkinter.Button(window, text = "View Files", command = lambda: fetch_files(listbox))
btdownload_start.grid(column=1, row=2)


# In[139]:

bt_download = tkinter.Button(window, text="Download", command = lambda: fileutils.pull_file(listbox.get(tkinter.ACTIVE)))
bt_download.grid(column = 1, row = 4)


# In[140]:

l1 = tkinter.Label(window, text="Enter Password")
l1.grid(column=0, row=6)


# In[141]:

txt2 = tkinter.Entry(window, width = 10)
txt2.grid(column=1, row=6)


# In[142]:

bt_pushdb = tkinter.Button(window, text="Push Database", command = lambda: dbutils.push_db(txt.get()))
bt_pushdb.grid(column=1, row=7)


# In[143]:

window.mainloop()


# In[ ]:



