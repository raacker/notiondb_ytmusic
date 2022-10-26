from apis.api_factory import Provider
from apis.api_factory import generate_api_manager

def process_argv(argv):
    api_provider = None

    if argv['--spotify']:
        api_provider = generate_api_manager(Provider.Spotify)
    elif argv['--youtube']:
        api_provider = generate_api_manager(Provider.Youtube)

    if argv['--export']:
        if not argv['--url']:
            return False

        api_provider.export_playlist_to_csv(argv['--url'], argv['--name'])
        return True
    if argv['--generate']:
        if not argv['--file']:
            return False

        api_provider.generate_playlist_from_csv(argv['--file'], argv['--name'])
        return True