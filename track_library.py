# Importing required libraries
import csv  # To read and write CSV files
from library_item import LibraryItem  # Importing the LibraryItem class that represents a track item

# Dictionary to hold the songs data
library = {}  # A dictionary that will store tracks, indexed by Track ID

# Load the songs from the CSV
def load_songs_from_csv():
    try:
        # Open the CSV file in read mode, using UTF-8 encoding
        with open("songs_list.csv", mode="r", encoding="utf-8") as file:
            reader = csv.DictReader(file)  # Using DictReader to read the CSV as a dictionary
            
            # Clear previous library data to avoid duplication
            library.clear()

            # Load all the rows into the library as LibraryItem objects
            for row in reader:
                # Extract data from each row in the CSV file
                track_id = row["Track ID"]
                name = row["Name"]
                artist = row["Singer"]
                source = row["File Path"]
                rating = int(row["Rating"])  # Convert Rating to an integer
                play_count = int(row["Plays"])  # Convert Plays to an integer

                # Create a LibraryItem object and store it in the library dictionary
                library[track_id] = LibraryItem(track_id, name, artist, source, rating, play_count)
        
        # Print how many tracks were loaded for debugging purposes
        print(f"Loaded {len(library)} tracks")
        
        # Return the library dictionary
        return library
    except Exception as e:
        # If there is an error reading the CSV file, print the error message
        print(f"Error loading songs from CSV: {e}")
        return {}  # Return an empty dictionary in case of an error

# List all tracks in a string format to display in the UI
def list_all():
    output = ''  # Initialize an empty string to hold the track list
    for track_id, track in library.items():
        # Concatenate track details (name, artist, rating) to the output string
        output += f"Name: {track.name}, Singer: {track.artist}, Rating: {track.rating}\n \n"
    
    return output  # Return the complete track list string

# Get track name based on track_id
def get_name(key):
    # Return the name of the track if it exists in the library, otherwise return None
    return library[key].name if key in library else None

# Get artist based on track_id
def get_artist(key):
    # Return the artist of the track if it exists in the library, otherwise return None
    return library[key].artist if key in library else None

# Get track rating based on track_id
def get_rating(key):
    # Return the rating of the track if it exists, otherwise return -1 (indicating no rating)
    return library[key].rating if key in library else -1

# Get track file source (path) based on track_id
def get_music_source(key):
    # Return the file path of the track if it exists, otherwise return None
    return library[key].source if key in library else None

# Get play count based on track_id
def get_play_count(key):
    try:
        # Retrieve and return the play count of the track if it exists
        item = library[key]
        return item.play_count
    except KeyError:
        # If the track doesn't exist, return -1 to indicate error
        return -1

# Increment play count based on track_id
def increment_play_count(key):
    try:
        # Increase the play count for the specified track
        item = library[key]
        item.play_count += 1
    except KeyError:
        # If the track doesn't exist, do nothing
        return
    
# Set the name of the track
def set_name(track_id, new_name):
    if track_id in library:
        # If the track exists, update its name
        library[track_id].name = new_name
        write_to_csv()  # Save changes to the CSV file

# Set the artist of the track
def set_artist(track_id, new_artist):
    if track_id in library:
        # If the track exists, update its artist
        library[track_id].artist = new_artist
        write_to_csv()  # Save changes to the CSV file

# Set the rating of the track
def set_rating(track_id, rating):
    if track_id in library:
        # If the track exists, update its rating
        library[track_id].rating = rating
        print(f"Updated rating for Track {track_id} to {rating}")
        write_to_csv()  # Save changes to the CSV file

# Set the play count of the track
def set_play_count(track_id):
    if track_id in library:
        # If the track exists, set its play count
        library[track_id].plays = library[track_id].play_count
        write_to_csv()  # Save changes to the CSV file

# Write updated track data back to CSV
def write_to_csv():
    # Open the CSV file in write mode to overwrite it with updated data
    with open("songs_list.csv", mode="w", newline="", encoding="utf-8") as file:
        writer = csv.writer(file)
        # Write the header row with the column names
        writer.writerow(["Track ID", "ID", "Name", "Singer", "File Path", "Rating", "Plays"])  

        # Iterate over all tracks and write their data to the CSV file
        for track_id, track in library.items():
            writer.writerow([track_id, track.track_id, track.name, track.artist, track.source, track.rating, track.play_count])

# Get track by ID
def get_track_by_id(track_id):
    # Return the track object based on the provided track_id if it exists
    return library.get(track_id)

# List all tracks loaded from the CSV
def list_all_tracks():
    # Return the entire library dictionary, which contains all tracks
    return library
