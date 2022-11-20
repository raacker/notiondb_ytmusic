from ytmusicapi import YTMusic
from apis.api_provider import APIProvider
import utils.utils as utils
import re

class YoutubeAPI(APIProvider):
    def __init__(self):
        self.ytmusic = YTMusic(utils.get_auth_path() + 'ytmusic_auth.json')

    def get_youtube_playlist_id(url):
        id_start = re.search("list=", url)
        if not id_start:
            return url

        return url[id_start.end():]

    def export_playlist_to_csv(self, playlist_id, csv_name = ""):
        playlist_id = YoutubeAPI.get_youtube_playlist_id(playlist_id)
        plist = self.ytmusic.get_playlist(playlist_id, 1000)

        tracks = plist["tracks"]

        if not csv_name:
            csv_name = plist["title"]
        if ".csv" not in csv_name:
            csv_name += ".csv"

        f = open(utils.get_output_path() + csv_name, "w")

        for track in tracks:
            f.write(str(track["title"]) + "," + str(track["artists"][0]['name']) + "\n")

        f.close()


    def generate_playlist_from_csv(self, csv_name, playlist_name = ""):
        f = open(utils.get_output_path() + csv_name, "r")
        if not f:
            return

        if not playlist_name:
            playlist_name = csv_name
        if ".csv" in playlist_name:
            playlist_name = playlist_name[:-4]

        playlist_id = self.ytmusic.create_playlist(playlist_name, "Description")

        searchHitMiss = []
        for line in f.readlines():
            song_name, artist_name = utils.generate_song_artist_tuple(line)
            search_query = song_name + " " + artist_name
            result = self.ytmusic.search(search_query)

            foundResult = None
            for res in result:
                if res['resultType'] == "song":
                    foundResult = res
                    break
            
            if foundResult == None:
                searchHitMiss.append((line, "Couldn't find a song type result"))
            else:
                addResult = self.ytmusic.add_playlist_items(playlist_id, [foundResult['videoId']])
                if (addResult['status'] != 'STATUS_SUCCEEDED'):
                    message = addResult['actions'][0]['addToToastAction']['item']['notificationActionRenderer']['responseText']['runs'][0]['text']
                    searchHitMiss.append((line, message))

        if len(searchHitMiss) != 0:
            print ("Manual action required")
            print (searchHitMiss)
        else:
            print ("Successfully fetched all songs!")

        print ("Playlist URL : https://music.youtube.com/playlist?list=" + playlist_id)
        f.close()