from ytmusicapi import YTMusic

ytmusic = YTMusic('headers_auth.json')
playlistID = "PLAYLIST_ID"
plist = ytmusic.get_playlist(playlistID)

f = open("import_list.csv", "r")

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
        addResult = ytmusic.add_playlist_items(playlistID, [foundResult['videoId']])
        if (addResult['status'] != 'STATUS_SUCCEEDED'):
            message = addResult['actions'][0]['addToToastAction']['item']['notificationActionRenderer']['responseText']['runs'][0]['text']
            searchHitMiss.append((line, message))

print ("Manual action required")
print (searchHitMiss)

f.close()