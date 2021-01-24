import spotipy, os, youtube_dl, json, platform
from spotipy.oauth2 import SpotifyClientCredentials
from youtube_search import YoutubeSearch

# Check for MacOS and Windows users
if platform.system() == "Darwin":
    print("!MacOS has not been tested and might just crash!")
if platform.system() == "Windows":
    print("!Windows has not been tested and might just crash!")

# Load options
f = open("./dl_opts.json")
options = json.load(f)
os.environ["SPOTIPY_CLIENT_ID"] = options["clientid"]
os.environ["SPOTIPY_CLIENT_SECRET"] = options["clientsec"]
ydl_opts = options["ydl_opts"]

# Promp for Playlist URI
playlist_id = input("Input Spotify Playlist URI: ")

# Login to Spotify API
sp = spotipy.Spotify(client_credentials_manager=SpotifyClientCredentials())

# Set error detection Variable
flawless = True
successfull = 0

# Create download folder
try:
    os.mkdir("./Downloaded")
except OSError:
    print("Creation of the download folder failed. (Maybe the folder already exists)")
    x = input("Continue? (y/n)")
    if x != "y":
        exit()

# Fetch Playlist Tracks from Spotify
results = sp.user_playlist_tracks("lol", playlist_id, fields='items,uri,name,id,total', market='fr')
tracknum = len(results["items"])
print(str(tracknum) + " songs found.")

# Loop over Tracks and Download them
for item in results["items"]:
    #Create Trackname
    track_Name = item["track"]["artists"][0]["name"] + " - " + item["track"]["name"]
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
            successfull += 1
            #Rename and move the file
            try:
                dl_file_name = video_name+"-"+video_id
                os.rename(r"./"+dl_file_name+".mp3",r"./Downloaded/"+track_Name+".mp3")
                print("Song has been renamed and moved")
            except FileNotFoundError:
                print("Song couldn't be renamed.")
                flawless = False

# Present end result
print("\n\n\n")
if flawless:
    print("Playlist downloading completed without errors.")
else:
    print("Playlist download completed with errors. Check Folder for missing songs or renames.")

print("The songs can be found at: " + os.getcwd() + "/Downloaded")
print("Downloaded " + str(successfull) + " out of " + str(tracknum) + " songs")