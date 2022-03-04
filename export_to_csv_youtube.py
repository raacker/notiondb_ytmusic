from ytmusicapi import YTMusic
import pathlib

playlist_id = "PLAYLIST_ID"
playlist_name = "PLAYLIST_NAME"

current_path = pathlib.Path(__file__).parent.resolve()
ytmusic = YTMusic(str(current_path) + "/ytmusic_auth.json")
list = ytmusic.get_playlist(playlist_id, 1000)

tracks = list["tracks"]

f = open(str(current_path) + "/" + playlist_name + ".csv", "w")

for track in tracks:
    f.write(str(track["title"]) + "," + str(track["artists"][0]['name']) + "\n")

f.close()