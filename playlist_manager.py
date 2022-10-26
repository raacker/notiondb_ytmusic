"""Playlist Manager

Usage:
  playlist_manager.py --help
  playlist_manager.py --export (--spotify | --youtube) --url="<playlist_url>" --file=<file_path>
  playlist_manager.py --generate (--spotify | --youtube) --file=<file_path> [--name=<playlist_name>]
  playlist_manager.py --version

Options:
  -h --help        Show this screen.
  -v --version     Show version.
  -e --export      Export a playlist to a csv file
  -g --generate    Generate a playlist from a csv file
  -s --spotify     Use Spotify API
  -y --youtube     Use Youtube API

"""
from docopt import docopt
from process_argv import process_argv

def main(argv):
    process_argv(argv)
   
if __name__ == "__main__":
    arguments = docopt(__doc__, version='Playlist Manager 1.0')
    main(arguments)