from abc import abstractmethod

class APIProvider():
    @abstractmethod
    def export_playlist_to_csv(playlist_uri, csv_name):
        pass

    @abstractmethod
    def generate_playlist_from_csv(csv_name):
        pass