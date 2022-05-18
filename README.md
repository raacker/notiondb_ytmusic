# playlist_api
Auto import and export python script for Youtube Music & Spotify. Apple Music or other platforms can be added as well!


## Youtube Auth

API : [ytmusicapi](https://github.com/sigma67/ytmusicapi)

[Setup instruction](https://ytmusicapi.readthedocs.io/en/latest/setup.html)

Get Packet data and copy informations you need to fill into ytmusic_auth.json


## Spotify Auth

API : [spotipy](https://github.com/plamere/spotipy)

[Spotify Auth Scope](https://developer.spotify.com/documentation/general/guides/authorization/scopes/)

1. Go to [Spotify Developers dashboard](https://developer.spotify.com/dashboard/login)
2. Login and create a new project
3. At the dashboard, locate Client ID, Client Secret and put them into spotify_json file
4. Under "Edit Settings", set "Redirect URIs" to http://localhost
5. Run script and you will see a black webpage with an url. Copy the url and paste to the terminal.


# How to get Spotify URI

Just FYI if you don't know how to copy it.

If you do Right Click -> Share, hold ALT to change "Copy link to playlist" to Spotify URI