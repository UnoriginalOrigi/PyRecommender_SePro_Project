from tkinter import *
from tkinter import ttk
import spotipy
from util.credential_manager import EXPECTED_INPUT_LENGTH,login_attempt
from util.general_func import clean_up

#Button size 75x25

class Login_Window:
    def __init__(self,root):
        self.__logged_in = False
        self.master = root
        self.master.geometry("800x800")
        self.master.resizable(0,0)

        self.frame = ttk.Frame(self.master, width=800, height=800)
        self.frame.pack()
        self.master.update()

        self.button1 = ttk.Button(self.frame, text="Login", command=self.login_window)
        self.button1.place(x=5, y=self.frame.winfo_height()-30)
        self.button2 = ttk.Button(self.frame, text="Quit", command=self.master.destroy)
        self.button2.place(x=self.frame.winfo_width()-80, y=self.frame.winfo_height()-30)
        self.master.update()

        self.label1 = ttk.Label(self.frame, text="Client ID")
        self.entry_text1 = StringVar()
        self.entry1 = ttk.Entry(self.frame,width=35,textvariable=self.entry_text1)
        self.entry_text1.trace_add("write", lambda *args: self.character_limit(self.entry_text1))
        self.entry_text2 = StringVar()
        self.label2 = ttk.Label(self.frame, text="Client Secret")
        self.entry2 = ttk.Entry(self.frame,show="*",width=35,textvariable=self.entry_text2)
        self.entry_text2.trace_add("write", lambda *args: self.character_limit(self.entry_text2))
        self.entry1.place(x=self.frame.winfo_width()/2-102.5, y=self.frame.winfo_height()/2-30)
        self.entry2.place(x=self.frame.winfo_width()/2-102.5, y=self.frame.winfo_height()/2+30)
        self.label1.place(x=self.frame.winfo_width()/2-102.5, y=self.frame.winfo_height()/2-52)
        self.label2.place(x=self.frame.winfo_width()/2-102.5, y=self.frame.winfo_height()/2+8)
        self.master.update()


    def character_limit(self, txt_entry):
        if len(txt_entry.get()) > EXPECTED_INPUT_LENGTH:
            txt_entry.set(txt_entry.get()[:EXPECTED_INPUT_LENGTH])

    def login_window(self):
        try:
            login_attempt(self.entry1.get(),self.entry2.get())
            self.__logged_in = True
            self.master.destroy()
        except spotipy.oauth2.SpotifyOauthError:
                print("Invalid Credentials Given, failed to connect")

    def get_login_status(self):
         return self.__logged_in

class Test:
    def __init__(self,root):
        self.master = root
        self.master.geometry("800x800")
        self.master.resizable(0,0)

def tkinter_program():
    root = Tk(screenName="Login PyRecommender",baseName="Login PyRecommender",className="Login PyRecommender")
    access_window = Login_Window(root)
    root.mainloop()
    __logged_in = access_window.get_login_status()
    if(__logged_in):
        root = Tk(screenName="PyRecommender",baseName="PyRecommender",className="PyRecommender")
        access_window = Test(root)
        root.mainloop()
    clean_up()