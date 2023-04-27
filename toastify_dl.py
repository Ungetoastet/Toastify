import spotipy, os, youtube_dl, json, platform
from spotipy.oauth2 import SpotifyClientCredentials
from youtube_search import YoutubeSearch

# Check for MacOS and Windows users
if platform.system() == "Darwin":
    print("!MacOS has not been tested and might just crash!")
if platform.system() == "Windows":
    print("!Windows has not been tested and might just crash!")

# Set error detection Variables
flawless = True

def Download(track_Name):
    #Get video from yt
    try:
        search_resdic = YoutubeSearch(track_Name, max_results=1).to_dict()
    except KeyError:
        print("Youtube equivalent could not be found for " + track_Name)
        search_resdic = "Failed"
        flawless = False
    
    if search_resdic != "Failed":
        #Get video information
        try:
            video_id = search_resdic[0]["id"]
            video_name = search_resdic[0]["title"]
        except IndexError:
            print("Youtube equivalent could not be found for " + track_Name)
            video_id = "Failed"
            flawless = False
        
        if video_id != "Failed":
            print("\nDownloading song: " + track_Name)
            #Download the video and convert to mp3
            with youtube_dl.YoutubeDL(ydl_opts) as ydl:
                ydl.download(['http://youtu.be/'+video_id])
            #Rename and move the file
            try:
                dl_file_name = video_name+"-"+video_id
                os.rename(r"./"+dl_file_name+".mp3",r"./"+playlist_name+"/"+track_Name+".mp3")
                print("Song has been renamed and moved")
            except FileNotFoundError:
                print("Song couldn't be renamed.")
                flawless = False

# Load options
f = open("./dl_opts.json")
options = json.load(f)
os.environ["SPOTIPY_CLIENT_ID"] = options["clientid"]
os.environ["SPOTIPY_CLIENT_SECRET"] = options["clientsec"]
ydl_opts = options["ydl_opts"]

# Prompt for Playlist URI
playlist_id = input("Input Spotify Playlist URI: ")
playlist_name = playlist_id.split(":")[2]

# Login to Spotify API
sp = spotipy.Spotify(client_credentials_manager=SpotifyClientCredentials())

action = input("redownload/sync/cancel? (r/s/c)")

# Create download folder
try:
    os.mkdir("./" + playlist_name)
except OSError:
    print("Creation of the download folder failed. Probably the folder already exists.")
    
if action == "c":
    exit()

# Fetch Playlist Tracks from Spotify
results = sp.user_playlist_tracks("lol", playlist_id, fields='items,uri,name,id,total', market='fr')
tracknum = len(results["items"])
print(str(tracknum) + " songs found.")


# Loop over Tracks and Download them
for item in results["items"]:
    #Create Trackname
    track_Name = item["track"]["artists"][0]["name"] + " - " + item["track"]["name"]
    if action == "r":
        Download(track_Name)
    if action == "s":
        try:
            f = open("./"+playlist_name+"/" + track_Name + ".mp3")
            print("\nSong found, skipping...")
        except IOError:
            Download(track_Name)
        finally:
            f.close()

# Present end result
print("\n\n\n")
if flawless:
    print("Playlist downloading completed without errors.")
else:
    print("Playlist download completed with errors. Check Folder for missing songs or renames.")

print("The songs can be found at: " + os.getcwd() + "/"+playlist_name)