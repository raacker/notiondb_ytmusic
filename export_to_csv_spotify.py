import spotipy
from spotipy.oauth2 import SpotifyClientCredentials
import json
import pathlib

#playlist_uri = ""
#export_csv_name = ""
playlist_uri = "spotify:playlist:3uGRo6dvdiD3HgCt6AfGQ9"
export_csv_name = "new_found_in_feb"

auth_json_f = open('spotify_auth.json')
auth_json = json.load(auth_json_f)

sp = spotipy.Spotify(auth_manager=SpotifyClientCredentials(client_id=auth_json['client_id'],
                                               client_secret=auth_json['client_secret']))


result = sp.playlist_items(playlist_id=playlist_uri, limit=100)
current_path = pathlib.Path(__file__).parent.resolve()
f = open(str(current_path) + "/" + export_csv_name + ".csv", "w")

for item in result['items']:
    track = item['track']
    song_name = track['name']
    artist_name = track['artists'][0]['name']
    f.write(song_name + "," + artist_name + "\n")

f.close()