from pathlib import Path

def generate_song_artist_tuple(line):
    line = line.replace("\n", "")
    comma_index = line.rindex(",")
    song_name = line[:comma_index].strip()
    artist_name = line[comma_index+1:].strip()
    return (song_name, artist_name)

def get_auth_path():
    return str(Path.cwd()) + '/auth/'
    
def get_output_path():
    return str(Path.cwd()) + '/output/'