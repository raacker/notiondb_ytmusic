from enum import Enum
from APIs.spotify_api import SpotifyAPI
from APIs.youtube_api import YoutubeAPI

class Provider(Enum):
    Spotify = 0,
    Youtube = 1 

def generate_api_manager(api):
    if Provider.Spotify == api:
        return SpotifyAPI()
    elif Provider.Youtube == api:
        return YoutubeAPI()
    return None