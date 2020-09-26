
import os
import subprocess
import eyed3
import urllib.request as urllib2

from pytube import YouTube

# ---- Compile Data
url = input("Enter Youtube URL: ")
new_filename = input("Enter File name: ")
new_album = input("Enter Album name (Enter to reuse file name): ") or new_filename
new_author = input("Enter Author name: ") or "user"

print("1: Get YouTube Thumbnail")
print("2: Use default")
print("3: Custom")
print("4: None")
inputId = int(input("Enter Album Cover option: "))

if inputId == 1:
    new_album_cover = "https://img.youtube.com/vi/" + url.split("v=",1)[1] + "/0.jpg"
elif inputId == 2:
    new_album_cover = os.path.join(os.path.dirname(__file__), '../public/image/file.png')
elif inputId == 3:
    new_album_cover = input("Enter Album Cover url: ")

# ---- Download file
print("Downloading " + new_filename + " ...")
yt = YouTube(url)
try:
    yt.streams.filter(only_audio=True).first().download(filename=new_filename)
except:
    try:
        vids = yt.streams()
        for i in range(len(vids)):
            print(i,'. ',vids[i])
        vnum = int(input("Enter stream number: "))
        vids[vnum].download(filename=new_filename)
    except:
        print("Failed to download...")

# ---- Convert to MP3
print("Converting to mp3 ...")
subprocess.call([
    'ffmpeg',
    '-i', 
    os.path.join(new_filename + ".mp4"),
    '-metadata', 'title=' + new_filename,
    '-metadata', 'author=' + new_author,
    '-metadata', 'album=' + new_album,
    '-metadata', 'album_artist=' + new_author,
    os.path.join(new_filename + ".mp3"),
], stderr=subprocess.DEVNULL, stdout=subprocess.DEVNULL)

# ---- Add album cover
if inputId != 4:
    print("Adding album cover ...")

    audiofile = eyed3.load(os.path.join(new_filename + ".mp3"))
    if (audiofile.tag == None):
        audiofile.initTag()

    if inputId == 2:
        audiofile.tag.images.set(3, open(u"{}".format(new_album_cover),'rb').read(), 'image/jpeg')
    else:
        response = urllib2.urlopen(u"{}".format(new_album_cover))  
        imagedata = response.read()
        audiofile.tag.images.set(3, imagedata , "image/jpeg" ,u"Description")

    audiofile.tag.save()

# ---- Clean Up
print("Cleaning up ...")
test = os.listdir('.')
for item in test:
    if item.endswith(".mp4"):
        os.remove(os.path.join(item))

print('Completed')