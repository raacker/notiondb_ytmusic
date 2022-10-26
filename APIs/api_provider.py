from abc import abstractmethod

class APIProvider():
    @abstractmethod
    def export_playlist_to_csv(self, playlist_uri, csv_name = ""):
        pass

    @abstractmethod
    def generate_playlist_from_csv(self, csv_name, playlist_name = ""):
        pass