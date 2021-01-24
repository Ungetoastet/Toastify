import spotipy, os, youtube_dl, json
from spotipy.oauth2 import SpotifyClientCredentials
from youtube_search import YoutubeSearch

f = open("./dl_opts.json")
options = json.load(f)
os.environ["SPOTIPY_CLIENT_ID"] = options["clientid"]
os.environ["SPOTIPY_CLIENT_SECRET"] = options["clientsec"]

playlist_id = input("Input Spotify Playlist URI: ")

sp = spotipy.Spotify(client_credentials_manager=SpotifyClientCredentials())
ydl_opts = options["ydl_opts"]

results = sp.user_playlist_tracks("lol", playlist_id, fields='items,uri,name,id,total', market='fr')
for item in results["items"]:
    track_Name = item["track"]["artists"][0]["name"] + " - " + item["track"]["name"]
    search_res = YoutubeSearch(track_Name, max_results=1).to_json()
    video_id = search_res.split('"')[5]
    video_name = search_res.split('"')[15]
    print("Downloading song: " + track_Name + " with YT id " + video_id)
    with youtube_dl.YoutubeDL(ydl_opts) as ydl:
        dl = ydl.download(['http://youtu.be/'+video_id])

    try:
        dl_file_name = video_name+"-"+video_id.capitalize()
        os.rename(r"./"+dl_file_name+".mp3",r"./"+track_Name+".mp3")
        print("Song has been renamed.")
    except FileNotFoundError:
        print("Song couldn't be renamed.")

print("\n\nPlaylist downloading complete!")