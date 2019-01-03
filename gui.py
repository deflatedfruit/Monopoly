from tkinter import *


class BoardFrame(Frame):
    def __init__(self, master, *args, **kwargs):
        super().__init__(master, *args, **kwargs)
        self.master = master


class PlayerFrame(Frame):
    def __init__(self, master, *args, **kwargs):
        super().__init__(master, *args, **kwargs)
        self.master = master


class PropertyPopup(Toplevel):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
