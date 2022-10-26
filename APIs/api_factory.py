from enum import Enum
from apis.spotify_api import SpotifyAPI
from apis.youtube_api import YoutubeAPI

class Provider(Enum):
    Spotify = 0,
    Youtube = 1 

def generate_api_manager(api):
    if Provider.Spotify == api:
        return SpotifyAPI()
    elif Provider.Youtube == api:
        return YoutubeAPI()
    return None