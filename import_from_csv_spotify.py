import spotipy
from spotipy.oauth2 import SpotifyOAuth
import json

playlist_name = ""

auth_json_f = open('spotify_auth.json')
auth_json = json.load(auth_json_f)

sp = spotipy.Spotify(auth_manager=SpotifyOAuth(client_id=auth_json['client_id'],
                                               client_secret=auth_json['client_secret'],
                                               redirect_uri="http://localhost",
                                               scope="playlist-modify-public"))


current_user = sp.current_user()

playlist_obj = sp.user_playlist_create(current_user['id'], playlist_name)
playlist_id = playlist_obj['uri']

f = open((playlist_name + ".csv"), "r")

track_uris = set()
searchHitMiss = []
count = 0
for line in f.readlines():
    line = line.replace("\n", "")
    comma_index = line.rindex(",")
    song_name = line[:comma_index].strip()
    artist_name = line[comma_index+1:].strip()
    search_query = song_name + " " + artist_name
    result = sp.search(q=search_query, limit=1)

    foundURI = False
    for item in result['tracks']['items']:
        track_uris.add(item['uri'])
        foundURI = True
        break
    
    if not foundURI:
        searchHitMiss.append(line)

# spotify api request limit is 100
max_track_request = 99
result_uris = list(track_uris)
for i in range(0, len(result_uris), max_track_request):
    tracks = result_uris[i:i + max_track_request]
    addResult = sp.playlist_add_items(playlist_id, tracks)

if len(searchHitMiss) != 0:
    print ("Manual action required")
    print (searchHitMiss)
else:
    print ("Successfully fetched all songs!")

f.close()