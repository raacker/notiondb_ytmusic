from ytmusicapi import YTMusic

ytmusic = YTMusic('headers_auth.json')
playlistId = "PLAYLIST_ID"
list = ytmusic.get_playlist(playlistId, 300)

tracks = list["tracks"]

f = open("fetch_result.csv", "w")

for track in tracks:
    f.write(str(track["title"]) + "," + str(track["artists"][0]['name']) + "\n")

f.close()