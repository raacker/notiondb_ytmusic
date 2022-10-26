import os
import json
import logging
import pathlib
from pprint import pprint

def parse_song_comma_separated(song_string):
    line = song_string.replace("\n", "")
    comma_index = line.rindex(",")
    song_name = line[:comma_index].strip()
    artist_name = line[comma_index+1:].strip()
    return (song_name, artist_name)

### Format : song_name,artist
def generate_artist_map(csv_file_name):

    f = open(csv_file_name, "r")
    artist_map = {}

    for line in f.readlines():
        song_name, artist_name = parse_song_comma_separated(line)

        if song_name == "" or artist_name == "":
            continue 

        if not artist_name in artist_map: 
            artist_map[artist_name] = []
        artist_map[artist_name].append(song_name)
    return artist_map

### Expect to have { Songname: Artist } format
def check_duplicates(csv_file_name):
    artist_map = generate_artist_map(csv_file_name)

    print (artist_map)
