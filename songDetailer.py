from mutagen.mp3 import MP3
import os
import time
import tkinter as tk
from tkinter import messagebox
from tkinter import Listbox
from tkinter import filedialog
from tkinter import Scrollbar
from tkinter import Frame
import vlc

after_id=None
songs=[]
player= None
audiofile=None
path = ""
#path = r"C:\Users\Matt\Music"

border_effects = {
    "flat": tk.FLAT,
    "sunken": tk.SUNKEN,
    "raised": tk.RAISED,
    "groove": tk.GROOVE,
    "ridge": tk.RIDGE,
}

def open_file(window, entry, listbox):
    currdir = os.getcwd()
    tempdir =  filedialog.askdirectory()
    if(len(tempdir)>0):
        entry.config(text=tempdir, width=len(tempdir)+5)
        entry.pack()
        global path
        path = entry.cget('text')
        findSongs(path, listbox)
        #entry.pack(side=tk.LEFT, fill=tk.Y)
    else:
        messagebox.showinfo("Error", "No File Selected")

def convert(seconds):
    seconds = seconds % (24 * 3600)
    hour = seconds // 3600
    seconds %= 3600
    minutes = seconds // 60
    seconds %= 60

    return "%d:%02d:%02d" % (hour, minutes, seconds)

def findSongs(path, listbox):
    if(path=="Select directory of music"):
        messagebox.showinfo("Error", "Folder Not Specified")
        return
    list = os.listdir(path) # dir is your directory path
    number_files = len(list)
    duration = 0
    for i in list:
        if ".mp3" in i:
            audiofile = MP3(path + '/' + i)
            duration = audiofile.info.length
            strtime = convert(duration)
            #print(i)
            listbox.insert(tk.END, i)
            songs.append((i, duration))
            #print(strtime)


def countdowner(song, songlabel, currsong, window):
    global after_id
    if after_id:
        stopTimer(window)

    duration = 0
    nextsong=0
    if(isinstance(song, int)):
        nextsong = song
    else:
        nextsong = song[0]

    for i in range(0,len(songs)):
        if(i==nextsong):
            duration=songs[i][1]
            title=songs[i][0]
    currsong.config(text=title)

    global player
    player = vlc.MediaPlayer(path+ '/' + title)
    player.play()
    changeTitle(title[0:len(title)-4])
    changeTime(song,window,duration,songlabel)

def changeTitle(song):
    f = open("currentSongTitle.txt", "w+")
    f.truncate(0)
    f.seek(0)
    f.write(song)


def changeTime(song,window,duration,songlabel):
    f = open("currentSongDuration.txt", "w+")
    if(duration>0):
        strtime = convert(duration)
        f.write(strtime[len(strtime)-5:])
        f.truncate()
        f.seek(0)
        duration = duration - 1
        songlabel.config(text=str(strtime))
        global after_id
        after_id = window.after(1000,lambda: changeTime(song,window,duration,songlabel))
    else:
        countdowner(song[0]+1, songlabel, currsong, window)

def stopTimer(window):
    global after_id
    if after_id:
        window.after_cancel(after_id)
        after_id = None
        global player
        player.stop()

if __name__ == '__main__':
    window = tk.Tk()
    frame = tk.Frame()
    label_a = tk.Label(master=frame, text="Edgar eats penis")
    frame.pack()
    entry = tk.Label(frame, width=20, bg="white", fg="black", text="Select directory of music")
    entry.pack(side=tk.LEFT)

    folder = tk.Button(frame, text="File Explorer",command=lambda: open_file(window, entry, listbox), width=10)
    folder.pack(side=tk.LEFT)

    seperator = Frame()
    seperator.pack()
    scrollbar = Scrollbar(seperator, orient="vertical")
    listbox = Listbox(seperator, yscrollcommand=scrollbar.set, width=30)
    scrollbar.config(command=listbox.yview)
    listbox.pack(side=tk.LEFT)
    scrollbar.pack(side=tk.LEFT, fill=tk.X)

    player = Frame()
    player.pack()
    currsong = tk.Label(player, text="")
    currsong.pack(side=tk.TOP)
    timeleftlabel = tk.Label(player, text="Time Left: ")
    timeleftlabel.pack(side=tk.LEFT)
    timeleft = tk.Label(player, text="")
    timeleft.pack(side=tk.LEFT)
    start = tk.Button(player, text="Start",command=lambda: countdowner(listbox.curselection(), timeleft, currsong, window), width=15)
    start.pack(side=tk.LEFT)
    stop = tk.Button(player, text="Stop",command=lambda: stopTimer(window), width=15)
    stop.pack(side=tk.LEFT)

    window.mainloop()
