from APIs.api_factory import Provider
from APIs.api_factory import generate_api_manager

def process_argv(argv):
    api_provider = None

    if argv['--spotify']:
        api_provider = generate_api_manager(Provider.Spotify)
    elif argv['--youtube']:
        api_provider = generate_api_manager(Provider.Youtube)

    if argv['--export']:
        if not argv['--url'] or not argv['--file']:
            return False

        api_provider.export_playlist_to_csv(argv['--url'], argv['--file'])
        return True
    if argv['--generate']:
        if not argv['--file']:
            return False

        api_provider.generate_playlist_from_csv(argv['--file'])
        return True