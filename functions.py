from tkinter import *
from PIL import Image, ImageTk
import tkinter.messagebox
from pygame import mixer

def resize_image(img, h, w):
    img = img.resize((h, w))
    img = ImageTk.PhotoImage(img)
    return img

def display_icon(url, h, w):
    img = Image.open(url)
    img = resize_image(img, h, w)
    return img

# set volume command
def set_vol(val):
    volume = float(val) / 100
    mixer.music.set_volume(volume)

# about us
def about_us():
    tkinter.messagebox.showinfo("About Us - Music Player", "This is a music player build using Python Tkinter by GIT")

# help for current time
def isnewone(f, fnew):
    if f != fnew:
        return True
    else:
        return False
