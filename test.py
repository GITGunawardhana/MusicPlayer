from tkinter import *
import tkinter.messagebox
from tkinter import filedialog
from tkinter import ttk
from ttkthemes import themed_tk as tk
from mutagen.mp3 import MP3
from pygame import mixer
import os
import time
import threading
from functions import display_icon, set_vol, about_us, isnewone

root = tk.ThemedTk()

root.get_themes()                # Returns a list of all themes that can be set
root.set_theme("ubuntu")         # Sets an available theme

# Font Styles - normal, bold, roman, italic, underline and overstrike

def on_closing():
    # tkinter.messagebox.showinfo('Music Player', 'Do you want to close!')
    stop()
    root.destroy()

# playlist - contains the full path (full path is requered to play the music inside the 'play()' function)
playlist = []

# browse
def browse_file():
    global filename_path
    filename_path = filedialog.askopenfilename()
    if filename_path:
        add_to_playlist(filename_path)
    else:
        tkinter.messagebox.showerror('File not found', 'Please choose file.')

index = 0

def add_to_playlist(filename):
    global index
    # playlist_box.insert(index, "{:02d}: {}".format(index + 1, os.path.basename(filename)))  # .format(index, filename)
    playlist_box.insert(index, "{} {}".format("-", os.path.basename(filename)))  # .format(index, filename)
    playlist.append(filename)
    index += 1
    playlist_box.pack()


# Create menubar
menubar = Menu(root)
root.config(menu=menubar)

# create the sub-menu1
subMenu = Menu(menubar, tearoff=0)
menubar.add_cascade(label="File", menu=subMenu)
subMenu.add_command(label="Open", command=browse_file)
# create the sub-menu2
subMenu = Menu(menubar, tearoff=0)
menubar.add_cascade(label="Help", menu=subMenu)
subMenu.add_command(label="AboutUs", command=about_us)
# create the sub-menu3
subMenu = Menu(menubar, tearoff=0)
menubar.add_command(label="Exit", command=on_closing)

mixer.init()  # initializing the mixer

# root.geometry('100x300')
root.title("Music Player")
root.iconbitmap('windowicon.ico')

# seperate to two frames
# firstframe - leftframe, rightframe
firstfarme = ttk.Frame(root)
firstfarme.pack()

# leftframe - listbox(playlist), Add button, Del button
leftframe = ttk.Frame(firstfarme, relief = 'ridge')
leftframe.pack(side=LEFT, padx=10)

# rightframe - topframe, middleframe, bottomframe
rightframe = ttk.Frame(firstfarme, relief = 'ridge')
rightframe.pack(padx=10)

# lastframe - statusbar
lastframe = ttk.Frame(root)
lastframe.pack(side=BOTTOM, fill=X)

# topframe - lbl, length_label, current_label
topframe = ttk.Frame(rightframe)
topframe.grid(row=0, column=0, pady=20)

# label display
logoimg = display_icon('images/logo.png', 55, 55)

lbl3 = ttk.Label(topframe, image=logoimg)
lbl3.pack()

length_lbl = ttk.Label(topframe, text="Total Length | --:--:--", font="Arial 10")
length_lbl.pack()

current_time_length = ttk.Label(topframe, text="Current Time | --:--:--", relief=GROOVE)
current_time_length.pack()

# play list
playlist_box = Listbox(leftframe, font="Arial 9", width=100)
playlist_box.pack(padx=5, pady=5)

addBtn = ttk.Button(leftframe, text='Add', command=browse_file)
addBtn.pack(side=LEFT,padx=5, pady=5)

def del_from_playlist():
    try:
        selected_file = playlist_box.curselection()
        selected_file = int(selected_file[0])
        playlist_box.delete(selected_file)
        playlist.pop(selected_file)
        print(playlist)
    except IndexError:
        tkinter.messagebox.showerror('File not selected', 'Please select file')

delBtn = ttk.Button(leftframe, text='Remove', command=del_from_playlist)
delBtn.pack(side=LEFT)

# show music lenght
def show_details(play_song):
    file_data = os.path.splitext(play_song)

    if file_data[1] == '.mp3' or file_data[1] == '.MP3':
        audio = MP3(play_song)
        total_length = audio.info.length
    else:
        a = mixer.Sound(play_song)
        total_length = a.get_length()

    # div - total_length/60, mod - total_length % 60
    mins, secs = divmod(total_length, 60)
    mins = round(mins)
    secs = round(secs)
    timeformat = '{:02d}:{:02d}'.format(mins, secs)
    length_lbl['text'] = "Total Length" + ' | ' + timeformat
    length_lbl['font'] = "Arial 10 bold"

    t1 = threading.Thread(target=start_count, args=(total_length, play_song, fname))
    t1.start()

# def isoldone(fn=False):
#     return fn

def start_count(t, file, fnew):
    # global newone
    global paused
    global ischecker
    ischecker = 1
    # mixer.music.get_busy(): -> return FALSE when we press the stop button (music stop playing)
    while t and ischecker:
        if paused:
            continue
        else:
            mins, secs = divmod(t, 60)
            mins = round(mins)
            secs = round(secs)
            timeformat = "{:02d}:{:02d}".format(mins, secs)
            try:
                current_time_length["text"] = "Current Time | " + timeformat
            except:
                exit()
            time.sleep(1)
            t -= 1
        if isnewone(file, fnew):
            break

# play command
def play():
    global paused, fname
    global newone, filename_path, play_it
    try:
        if statusbar["text"] == "   Music Player Paused":
            mixer.music.unpause()
            paused = False
            statusbar["text"] = "   Playing : " + filename_path.split("/")[-1]
        else:
            try:
                stop()
                time.sleep(1)
                selected_song = playlist_box.curselection()
                selected_song = int(selected_song[0])
                play_it = playlist[selected_song]
                filename_path = play_it
                fname = filename_path
                mixer.music.load(play_it)
                mixer.music.play()
                statusbar['text'] = "   Playing : " + os.path.basename(play_it)
                statusbar["font"] = 'ms\ serif 9 bold'
                show_details(play_it)
            except:
                tkinter.messagebox.showerror('File not found', 'Please choose file.')
    except:
        # tkinter.messagebox.showerror("Not found file - Music Player", "Please choose a file")
        browse_file()

# pause command
paused = False

def pause():
    global paused, play_it
    if statusbar["text"] != "   Music Player Paused":
        mixer.music.pause()
        paused = True
        statusbar["text"] = "   Music Player Paused"
    else:
        mixer.music.unpause()
        paused = False
        statusbar["text"] = "   Playing : " + play_it.split("/")[-1]

# stop command
def stop():
    global ischecker
    ischecker = 0
    mixer.music.stop()
    statusbar["text"] = "   Music Player Stoped"
    statusbar["text"] = "   Welcome to Music Player"
    statusbar["font"] = 'ms\ serif 9 italic'
    length_lbl["text"] = "Total Length | --:--:--"
    current_time_length.configure(text="Current Time | --:--:--")

# mute music
muted = False

def music_mute():
    global muted

    if muted:
        muted = False
        scale.set(25)
        # muteUnmuteBtn.configure(image=unmuteImg)
        muteUnmuteBtn["image"] = unmuteImg  # method 1 for change image of the button
    else:
        # mixer.music.set_volume(0)
        muted = True
        scale.set(0)
        muteUnmuteBtn.configure(image=muteImg)  # method 2 for change image of the button

# middle frame - play, pause, stop button
middleframe = ttk.Frame(rightframe, relief=RAISED, borderwidth=0)
middleframe.grid(row=1, column=0, padx=20)

# play
playImg = display_icon('images/play.png', 20, 20)
playBtn = ttk.Button(middleframe, image=playImg, command=play)
playBtn.grid(row=0, column=0)

# pause
pauseImg = display_icon('images/pause.png', 20, 20)
pauseBtn = ttk.Button(middleframe, image=pauseImg, command=pause)
pauseBtn.grid(row=0, column=1, padx=5)

# stop
stopImg = display_icon('images/stop.png', 20, 20)
stopBtn = ttk.Button(middleframe, image=stopImg, command=stop)
stopBtn.grid(row=0, column=2)

# bottomframe - for volume control part
bottomframe = ttk.Frame(rightframe)
bottomframe.grid(row=2, column=0, pady=5)

# mute and unmute images
muteImg = display_icon('images/mute.png', 20, 20)
unmuteImg = display_icon('images/unmute.png', 20, 20)
# mute unmute button
muteUnmuteBtn = ttk.Button(bottomframe, image=unmuteImg, command=music_mute)
muteUnmuteBtn.grid(row=0, column=0)

# volume bar
scale = ttk.Scale(bottomframe, from_=0, to=100, orient=HORIZONTAL, command=set_vol)
scale.set(25)
scale.grid(row=0, column=1)

statusbar = ttk.Label(lastframe, text="   Welcome to Music Player", relief='ridge', anchor=W, font='ms\ serif 9')
statusbar.pack(fill=X)

try:
    root.protocol("WM_DELETE_WINDOW", on_closing)
except:
    root.protocol("WM_DELETE_WINDOW", on_closing)

root.mainloop()