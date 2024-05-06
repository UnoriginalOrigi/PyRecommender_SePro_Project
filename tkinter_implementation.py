from tkinter import *
from tkinter import ttk
from tkinter.constants import DISABLED, NORMAL, SINGLE
import os
import re
import spotipy
from util.credential_manager import EXPECTED_INPUT_LENGTH,login_attempt,credential_loader
from util.general_func import clean_up, related_artists_search, INPUT_SIZE
from util.MyAES import loadKey

#Button size 75x25

class __Login_Window:
    def __init__(self,root):
        self.sp = None
        self.__logged_in = False
        self.master = root
        self.master.geometry("400x400")
        self.master.resizable(0,0)

        self.frame = ttk.Frame(self.master, width=400, height=400)
        self.frame.pack()
        self.master.update()

        self.button1 = ttk.Button(self.frame, text="Login", command=self.__login_window)
        self.button2 = ttk.Button(self.frame, text="Quit", command=self.master.destroy)
        self.button3 = ttk.Button(self.frame, text="Load Saved Details", command=self.__saved_login,state=DISABLED)
        if os.path.exists("client_info.txt"):
            self.button3['state'] = NORMAL
            self.label3 = ttk.Label(self.frame, text="Saved Details Found")
        else:
            self.label3 = ttk.Label(self.frame, text="No Saved Details")

        self.button1.place(x=self.frame.winfo_width()-80, y=self.frame.winfo_height()-30)
        self.button2.place(x=5, y=self.frame.winfo_height()-30)
        self.label3.place(x=self.frame.winfo_height()/2-50, y=self.frame.winfo_height()-52)
        self.button3.place(x=self.frame.winfo_height()/2-50, y=self.frame.winfo_height()-30)

        self.master.update()

        self.label4 = ttk.Label(self.frame, text="Attempt to Login",foreground='red')

        self.label1 = ttk.Label(self.frame, text="Client ID")
        self.entry_text1 = StringVar()
        self.entry1 = ttk.Entry(self.frame,width=35,textvariable=self.entry_text1)
        self.entry_text1.trace_add("write", lambda *args: self.__character_limit(self.entry_text1))
        self.entry_text2 = StringVar()
        self.label2 = ttk.Label(self.frame, text="Client Secret")
        self.entry2 = ttk.Entry(self.frame,show="*",width=35,textvariable=self.entry_text2)
        self.entry_text2.trace_add("write", lambda *args: self.__character_limit(self.entry_text2))
        self.entry1.place(x=self.frame.winfo_width()/2-102.5, y=self.frame.winfo_height()/2-30)
        self.entry2.place(x=self.frame.winfo_width()/2-102.5, y=self.frame.winfo_height()/2+30)
        self.label1.place(x=self.frame.winfo_width()/2-102.5, y=self.frame.winfo_height()/2-52)
        self.label2.place(x=self.frame.winfo_width()/2-102.5, y=self.frame.winfo_height()/2+8)
        self.label4.place(x=self.frame.winfo_width()/2-102.5, y=self.frame.winfo_height()/2+60)
        self.master.update()


    def __character_limit(self, txt_entry):
        if len(txt_entry.get()) > EXPECTED_INPUT_LENGTH:
            txt_entry.set(txt_entry.get()[:EXPECTED_INPUT_LENGTH])

    def __login_window(self):
        if len(self.entry1.get()) < EXPECTED_INPUT_LENGTH or len(self.entry2.get()) < EXPECTED_INPUT_LENGTH:
            self.label4.config(text="Invalid Credentials. Input too short.") #Credentials wrong length
        else:
            try:
                self.sp = login_attempt(self.entry1.get(),self.entry2.get())
                self.__logged_in = True
                self.master.destroy()
            except spotipy.oauth2.SpotifyOauthError: #Invalid credentials
                self.label4.config(text="Invalid Credentials. Check Credentials")
                self.label4.place()

    def get_login_status(self):
         return self.__logged_in, self.sp
    
    def __saved_login(self):
        params = loadKey()
        client_id, client_secret = credential_loader(params)
        try:
            self.sp = login_attempt(client_id,client_secret)
            self.__logged_in = True
            self.master.destroy()
        except spotipy.oauth2.SpotifyOauthError:
            self.label4.config(text="Invalid Credentials. File Corrupted or Key Invalid") #Unable to decrypt
            self.label4.place()

class __Program_Window:
    def __init__(self,root,sp):
        self.sp = sp
        self.master = root
        self.master.geometry("800x800")
        self.master.resizable(0,0)

        self.frame = ttk.Frame(self.master, width=800, height=800)
        self.frame.pack()
        self.master.update()

        self.Lb1 = Listbox(self.frame,width=45,height=40,selectmode=SINGLE)
        self.Lb2 = Listbox(self.frame,width=65,height=40,selectmode=SINGLE)
        self.Lb1.place(x=5, y=5)
        self.Lb2.place(x=self.frame.winfo_width()/2-50, y=5)

        self.label1 = ttk.Label(self.frame, text="Search Input ")
        self.label2 = ttk.Label(self.frame, text="Invalid Input ",state=DISABLED)
        #self.label3 = ttk.Label(self.frame, text="Currently playing: None")
        self.label1.place(x=self.frame.winfo_width()-280, y=self.frame.winfo_height()-48)
        #self.label3.place(x=5, y=self.frame.winfo_height()-48)

        self.dropbox_options = ["Artist","Song"]
        self.dropbox_text = StringVar()
        self.dropbox_text.set("Artist")
        self.dropbox1 = OptionMenu(self.master,self.dropbox_text,*self.dropbox_options)
        self.dropbox1.place(x=self.frame.winfo_width()-360, y=self.frame.winfo_height()-44)

        self.entry_text1 = StringVar()
        self.entry1 = ttk.Entry(self.frame,width=30,textvariable=self.entry_text1)
        self.entry_text1.trace_add("write", lambda *args: self.__character_limit(self.entry_text1))
        self.entry1.place(x=self.frame.winfo_width()-280, y=self.frame.winfo_height()-30)

        self.button1 = ttk.Button(self.frame, text="Find", command=self.__related_search)
        self.button2 = ttk.Button(self.frame, text="Quit", command=self.master.destroy)
        self.button3 = ttk.Button(self.frame, text=">", width=5, command=self.__get_cursor_songs, state=DISABLED)
        self.button4 = ttk.Button(self.frame, text="<", width=5, command=self.__get_related_artists, state=DISABLED)
        #self.button5 = ttk.Button(self.frame, text="Play", command=self.__play_selected_song, state=DISABLED)
        self.button1.place(x=self.frame.winfo_width()-80, y=self.frame.winfo_height()-30)
        self.button2.place(x=5, y=self.frame.winfo_height()-30)
        self.button3.place(x=self.frame.winfo_width()/2-105, y=self.frame.winfo_height()/2-130)
        self.button4.place(x=self.frame.winfo_width()/2-105, y=self.frame.winfo_height()/2-70)
        #self.button5.place(x=self.frame.winfo_width()/2-30, y=self.frame.winfo_height()-30)

    def __get_related_artists(self):
        try:
            self.button4['state'] = NORMAL
            search_query = re.search("(?<=~ ).*?(?= &)",self.Lb2.get(self.Lb2.curselection()[0])) #Input cleaning
            try:
                search_query = search_query.group(0)
            except AttributeError:
                search_query = re.search("(~ .+)",self.Lb2.get(self.Lb2.curselection()[0]))
                search_query = search_query.group(0)[2:]
            results = related_artists_search(self.sp,search_query)
            self.Lb1.delete(0,END)
            for idx, artist in enumerate(results['artists']):
                self.Lb1.insert(idx+1,artist['name'])
        except IndexError:
            pass

    def __get_cursor_songs(self):
        try:
            self.button4['state'] = NORMAL
            #self.button5['state'] = NORMAL
            search_query = re.search("(?<=~ ).*?(?= &)",self.Lb1.get(self.Lb1.curselection()[0])) #Input cleaning
            try:
                search_query = search_query.group(0)
            except AttributeError:
                search_query = re.search("(~ .+)",self.Lb1.get(self.Lb1.curselection()[0]))
            try:
                search_query = search_query.group(0)[2:]
            except AttributeError:
                search_query = self.Lb1.get(self.Lb1.curselection()[0])
            results = self.sp.search(q=search_query, limit=20)
            self.Lb2.delete(0,END)
            for idx, track in enumerate(results['tracks']['items']):
                temp = "{} ~ {}".format(track['name'], track['artists'][0]['name'])
                if len(track['artists']) > 1:
                    for i in range(1, len(track['artists'])):
                        temp = "{} & {}".format(temp, track['artists'][i]['name'])
                self.Lb2.insert(idx+1,temp)
        except IndexError:
            pass

    def __character_limit(self, txt_entry):
        if len(txt_entry.get()) > INPUT_SIZE: #Implemented Char limit
            txt_entry.set(txt_entry.get()[:INPUT_SIZE])

    def __related_search(self):
        print(self.dropbox_text.get())
        if len(self.entry1.get()) > 0 and len(self.entry1.get()) < INPUT_SIZE: #Input Length Validation
            self.label2.place_forget()
            self.Lb1.delete(0,END)
            if(self.dropbox_text.get() == "Artist"):
                related_artists = related_artists_search(self.sp,self.entry1.get())
                self.button3['state'] = NORMAL
                for idx, artist in enumerate(related_artists['artists']):
                    self.Lb1.insert(idx+1,artist['name'])
            else:
                results = self.sp.search(q=self.entry1.get(), limit=20)
                for idx, track in enumerate(results['tracks']['items']):
                    self.Lb1.insert(idx+1,"{} ~ {}".format(track['name'], track['artists'][0]['name']))
        else:
            self.label2.place(x=self.frame.winfo_width()-200, y=self.frame.winfo_height()-48)

def tkinter_program():
    root = Tk(screenName="Login PyRecommender",baseName="Login PyRecommender",className="Login PyRecommender")
    access_window = __Login_Window(root)
    root.mainloop()
    logged_in,sp = access_window.get_login_status()
    if(logged_in):
        root = Tk(screenName="PyRecommender",baseName="PyRecommender",className="PyRecommender")
        access_window = __Program_Window(root,sp)
        root.mainloop()
    clean_up()