# Toastify - Spotify Playlist Downloader
## WARNING
Currently doesnt work - waiting fix

## Description
A small script that fetches Spotify Playlist using the Spotify API.
The names of the songs then get redirected to a youtube search engine, downloaded from youtube and converted to an mp3 using ffmpeg.
This should work on Windows and Linux (maybe MacOS, haven't tried).
I made this in a single afternoon, so there might be lots of bugs and glitches.

## Installation
This programm runs using python 3.9 (https://www.python.org/downloads/) and ffmpeg (https://ffmpeg.org/), so you have to have those installed.
You will also need some python libraries (can be installed via pip):
- Spotipy
- youtube_dl
- youtube_search

All settings are saved in the "dl_opts.json" file.
There, you will need to change the "clientid" and "clientsec" to your own values to those of your Spotify App (https://developer.spotify.com/dashboard/applications)

## Usage
First, get the URI of the Playlist ready.
In order to do that, navigate to the Playlist you want to download.
Then press "Share" and "Copy Playlist URI". This URI should look something this: "spotify:playlist:randomgibberish"
Execute "toastify_dl.py" via a terminal and enter the URI when prompted.
Have Fun!
