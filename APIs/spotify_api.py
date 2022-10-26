import spotipy
from spotipy.oauth2 import SpotifyClientCredentials
from spotipy.oauth2 import SpotifyOAuth
import json
from pathlib import Path
from APIs.api_provider import APIProvider

class SpotifyAPI(APIProvider):
    def __init__(self):
        auth_json_f = open(str(Path.cwd()) + '/auth/spotify_auth.json')
        self.auth_json = json.load(auth_json_f)

    def export_playlist_to_csv(self, playlist_uri, csv_name):
        sp = spotipy.Spotify(auth_manager=SpotifyClientCredentials(
            client_id=self.auth_json['client_id'],
            client_secret=self.auth_json['client_secret']))
        
        playlist_info = sp.playlist(playlist_id=playlist_uri)

        f = open(str(Path.cwd()) + "/output/" + csv_name, "w")
        
        tracks = playlist_info['tracks']
        while tracks is not None:
            for item in tracks['items']:
                track = item['track']
                song_name = track['name']
                artist_name = track['artists'][0]['name']
                f.write(song_name + "," + artist_name + "\n")
            tracks = sp.next(tracks)
        f.close()


    def generate_playlist_from_csv(self, csv_name):
        sp = spotipy.Spotify(auth_manager=SpotifyOAuth(client_id=self.auth_json['client_id'],
                                                    client_secret=self.auth_json['client_secret'],
                                                    redirect_uri="http://localhost",
                                                    scope="playlist-modify-public"))

        current_user = sp.current_user()

        playlist_obj = sp.user_playlist_create(current_user['id'], csv_name)
        playlist_id = playlist_obj['uri']

        f = open(str(Path.cwd())  + "/output/" + csv_name, "r")

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