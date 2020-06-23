from mutagen.mp3 import MP3
import os
import time

path = r"C:\Users\Matt\Music"

def convert(seconds):
    seconds = seconds % (24 * 3600)
    hour = seconds // 3600
    seconds %= 3600
    minutes = seconds // 60
    seconds %= 60

    return "%d:%02d:%02d" % (hour, minutes, seconds)


list = os.listdir(path) # dir is your directory path
number_files = len(list)
duration = 0
for i in list:
    if ".mp3" in i:
        audiofile = MP3(path + "\\" + i)
        print(i)
        duration = audiofile.info.length
        strtime = convert(duration)
        print(strtime)

f = open("currentSongDuration.txt", "w+")
while(duration>0):
    strtime = convert(duration)
    f.write(strtime[len(strtime)-5:])
    time.sleep(1)
    f.truncate()
    f.seek(0)
    duration = duration - 1
    print(strtime)
