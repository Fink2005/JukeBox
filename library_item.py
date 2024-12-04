class LibraryItem:
    # Constructor method to initialize a LibraryItem object
    def __init__(self, track_id, name, artist, source, rating=0, play_count=0):

        self.track_id = track_id  # Set the track's unique ID
        self.name = name  # Set the track's name (song title)
        self.artist = artist  # Set the track's artist (singer or band name)
        self.source = source  # Set the source file path of the track
        self.rating = rating  # Set the track's rating (default is 0)
        self.play_count = play_count  # Set the play count (default is 0)


