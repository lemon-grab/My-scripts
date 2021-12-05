#!/usr/bin/env python3 
import pytube
 
path = "/home/lemon-grab/Videos"
url = input("link: ")
youtube = pytube.YouTube(url)
video = youtube.streams.get_highest_resolution()
video.download(path)
