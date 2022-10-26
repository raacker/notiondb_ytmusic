import spotipy
from spotipy.oauth2 import SpotifyClientCredentials
from spotipy.oauth2 import SpotifyOAuth
import json
from apis.api_provider import APIProvider
import utils.utils as utils
import re

class SpotifyAPI(APIProvider):
    def __init__(self):
        auth_json_f = open(utils.get_auth_path() + '/spotify_auth.json')
        self.auth_json = json.load(auth_json_f)

    def get_spotifyURL(url):
        if re.search("^spotify:playlist:*", url):
            return url

        playlist = re.search("playlist/", url)
        playlist_end = re.search("\?", url)
        return "spotify:playlist:" + url[playlist.end():playlist_end.start()]

    def export_playlist_to_csv(self, playlist_uri, csv_name = ""):
        sp = spotipy.Spotify(auth_manager=SpotifyClientCredentials(
            client_id=self.auth_json['client_id'],
            client_secret=self.auth_json['client_secret']))
        
        playlist_uri = SpotifyAPI.get_spotifyURL(playlist_uri)
        playlist_info = sp.playlist(playlist_id=playlist_uri)

        if not csv_name:
            csv_name = playlist_info["name"]
        if ".csv" not in csv_name:
            csv_name += ".csv"

        f = open(utils.get_output_path() + csv_name, "w")
        
        tracks = playlist_info['tracks']
        while tracks is not None:
            for item in tracks['items']:
                track = item['track']
                song_name = track['name']
                artist_name = track['artists'][0]['name']
                f.write(song_name + "," + artist_name + "\n")
            tracks = sp.next(tracks)
        f.close()


    def generate_playlist_from_csv(self, csv_name, playlist_name = ""):
        sp = spotipy.Spotify(auth_manager=SpotifyOAuth(client_id=self.auth_json['client_id'],
                                                    client_secret=self.auth_json['client_secret'],
                                                    redirect_uri="http://localhost",
                                                    scope="playlist-modify-public"))
        f = open(utils.get_output_path() + csv_name, "r")
        if not f:
            return

        current_user = sp.current_user()

        if not playlist_name:
            playlist_name = csv_name
        if ".csv" in playlist_name:
            playlist_name = playlist_name[:-4]

        playlist_obj = sp.user_playlist_create(current_user['id'], playlist_name)
        playlist_id = playlist_obj['uri']


        track_uris = set()
        searchHitMiss = []
        count = 0
        for line in f.readlines():
            song_name, artist_name = utils.generate_song_artist_tuple(line)
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