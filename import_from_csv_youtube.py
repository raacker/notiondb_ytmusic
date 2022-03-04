from ytmusicapi import YTMusic
import pathlib

playlist_id = "PLAYLIST_ID"
playlist_name = "PLAYLIST_NAME"


current_path = pathlib.Path(__file__).parent.resolve()
ytmusic = YTMusic(str(current_path) + "/ytmusic_auth.json")
plist = ytmusic.get_playlist(playlist_id)

f = open(playlist_name + ".csv", "r")

searchHitMiss = []
count = 0
for line in f.readlines():
    tokens = line.split(",")
    result = ytmusic.search(line)

    foundResult = None
    for res in result:
        if res['resultType'] == "song":
            foundResult = res
            break
    
    if foundResult == None:
        searchHitMiss.append((line, "Couldn't find a song type result"))
    else:
        addResult = ytmusic.add_playlist_items(playlist_id, [foundResult['videoId']])
        if (addResult['status'] != 'STATUS_SUCCEEDED'):
            message = addResult['actions'][0]['addToToastAction']['item']['notificationActionRenderer']['responseText']['runs'][0]['text']
            searchHitMiss.append((line, message))

if len(searchHitMiss) != 0:
    print ("Manual action required")
    print (searchHitMiss)
else:
    print ("Successfully fetched all songs!")

f.close()