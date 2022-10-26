"""Playlist Trader 1.0

Usage:
  playlist_trader.py --help
  playlist_trader.py --export (--spotify | --youtube) --url="<playlist_url>" [--name=<file_name>]
  playlist_trader.py --generate (--spotify | --youtube) --file="<file_path>" [--name=<playlist_name>]
  playlist_trader.py --version

Options:
  -h --help        Show this screen.
  -v --version     Show version.
  -e --export      Export a playlist to a csv file
  -g --generate    Generate a playlist from a csv file
  -s --spotify     Use Spotify API
  -y --youtube     Use Youtube API

"""
from docopt import docopt
from utils.process_argv import process_argv

def main(argv):
    process_argv(argv)
   
if __name__ == "__main__":
    arguments = docopt(__doc__, version='Playlist Trader 1.0')
    main(arguments)