from ytmusicapi import YTMusic
from pathlib import Path
from APIs.api_provider import APIProvider

class YoutubeAPI(APIProvider):
    def __init__(self):
        self.ytmusic = YTMusic(str(Path.cwd()) + '/auth/ytmusic_auth.json')

    def export_playlist_to_csv(self, playlist_id, csv_name):
        plist = self.ytmusic.get_playlist(playlist_id, 1000)

        tracks = plist["tracks"]

        f = open(str(Path.cwd()) + "/output/" + csv_name, "w")

        for track in tracks:
            f.write(str(track["title"]) + "," + str(track["artists"][0]['name']) + "\n")

        f.close()


    def generate_playlist_from_csv(self, csv_name):
        playlist_id = self.ytmusic.create_playlist(csv_name)

        f = open(str(Path.cwd()) + "/output/" + csv_name, "r")

        searchHitMiss = []
        count = 0
        for line in f.readlines():
            tokens = line.split(",")
            result = self.ytmusic.search(line)

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

        f.close()