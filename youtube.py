import os  # For working with the operating system, e.g., file paths
import csv  # For handling CSV file operations
import random  # To generate random values (used for rating)
import requests  # To make HTTP requests (used for YouTube API)
import yt_dlp  # YouTube downloader (used to download audio from YouTube)
import customtkinter as ctk  # CustomTkinter for GUI (UI framework)
from PIL import Image, ImageTk  # For image handling (optional but included)
from io import BytesIO  # For handling in-memory binary streams (optional)
import re  # For regular expression operations (used for sanitizing filenames)

# Directory to store downloaded songs
# Get the current directory where the script is located
current_directory = os.path.dirname(os.path.realpath(__file__))

# Define the path for JukeBox/music folder relative to the script directory
DOWNLOAD_FOLDER = os.path.join(current_directory, "music")

# Function to search for YouTube videos and get the best result
def search_youtube(query, limit=10):
    # Construct the YouTube API URL to search for videos based on the query
    search_url = f"https://www.googleapis.com/youtube/v3/search?part=snippet&q={query}&maxResults={limit}&key=AIzaSyCu2Pnj7biHRcacbf_ifq7QMe6vmbN3cb4"
    response = requests.get(search_url).json()  # Send request to the YouTube API and parse the response as JSON
    return response.get("items", [])  # Return the list of search results (video items)

# Function to sanitize the file name (remove special characters and dashes)
def sanitize_filename(filename):
    # Remove all characters that are not alphanumeric
    sanitized_name = re.sub(r'[^a-zA-Z0-9]', '', filename) 
    
    # Limit the length of the sanitized filename to a maximum of 100 characters
    sanitized_name = sanitized_name[:100] 
    
    return sanitized_name  # Return the sanitized filename

# Function to download YouTube video as audio
def download_youtube_audio(video_url, video_title, download_folder):
    if not video_url:
        return None, "No video URL provided."  # If no video URL is given, return error message

    # Sanitize the video title to create a valid filename
    sanitized_title = sanitize_filename(video_title)  
    filename = os.path.join(download_folder, f"{sanitized_title}")  # Create a complete file path with the sanitized title

    # yt-dlp options for downloading the best audio format and converting it to mp3
    ydl_opts = {
        'format': 'bestaudio/best',  # Download the best audio format available
        'outtmpl': filename,  # Save the file using the sanitized filename
        'postprocessors': [{
            'key': 'FFmpegExtractAudio',  # Post-process the audio and convert it to mp3 format
            'preferredcodec': 'mp3',  # Use mp3 codec
            'preferredquality': '192',  # Set the audio quality to 192kbps
        }],
        'quiet': True,  # Suppress unnecessary output
    }

    try:
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            ydl.download([video_url])  # Download the audio from the YouTube URL
        return filename, f"{video_title} downloaded successfully to {download_folder}."  # Return success message and the file path
    except Exception as e:
        return None, f"Failed to download {video_title}. Error: {str(e)}"  # If any error occurs, return an error message

# Function to get the next available Track ID from the CSV file
def get_next_track_id(csv_file):
    if not os.path.isfile(csv_file):
        return 1  # If the file doesn't exist, start with 1
    with open(csv_file, mode="r", encoding="utf-8") as f:
        reader = csv.reader(f)
        next(reader, None)  # Skip the header row
        track_ids = [int(row[0][1:]) for row in reader if row and row[0].startswith("0")]  # Extract numerical part of Track ID
        return max(track_ids, default=0) + 1  # Return the next available Track ID (starting from the highest existing ID + 1)

# Function to write song details to a CSV file with the next available Track ID
def write_to_csv(song_name, singer, file_path, rating, plays):
    csv_file = "songs_list.csv"  # Path to the CSV file where song details will be stored
    
    # Get the next available Track ID
    next_track_id = get_next_track_id(csv_file)

    # Create a unique Track ID (e.g., 01, 02, 03, etc.)
    track_id = f"{next_track_id:02d}"  # Ensure the Track ID has leading zeroes

    # Count existing rows for ID
    row_count = sum(1 for _ in open(csv_file, "r", encoding="utf-8")) if os.path.exists(csv_file) else 0
    id_number = row_count - 1 if row_count > 1 else 0  # ID starts at 0 after the header row

    # Write to CSV
    with open(csv_file, mode="a", newline="", encoding="utf-8") as f:
        writer = csv.writer(f)
        file_exists = os.path.isfile(csv_file) and os.path.getsize(csv_file) > 0
        if not file_exists:
            # Write header if the file is empty
            writer.writerow(["Track ID", "ID", "Name", "Singer", "File Path", "Rating", "Plays"])
        
        # Write the new song details to the CSV file
        writer.writerow([track_id, id_number, song_name, singer, f"{file_path}.mp3", rating, plays])

# YouTube Music Downloader App
class YouTubeApp(ctk.CTk):
    def __init__(self):
        super().__init__()

        # Configure the main window
        self.title("YouTube Music Downloader")
        self.geometry("1200x700")
        ctk.set_appearance_mode("Dark")  # Dark appearance mode
        ctk.set_default_color_theme("blue")  # Set color theme to blue

        # Variables
        self.track_results = []  # Store the search results for tracks
        self.track_counter = 1  # Initialize track_id starting from 01

        # Create layout
        self.create_layout()

    def create_layout(self):
        # Configure grid layout with resizing columns and rows
        self.grid_columnconfigure(1, weight=1)
        self.grid_rowconfigure(0, weight=1)

        # Left Sidebar
        self.sidebar = ctk.CTkFrame(self, width=200, corner_radius=0)
        self.sidebar.grid(row=0, column=0, sticky="ns")
        self.sidebar.grid_rowconfigure(4, weight=1)

        # Add a logo or title to the sidebar
        self.logo_label = ctk.CTkLabel(self.sidebar, text="YouTube Downloader", font=("Arial", 18, "bold"))
        self.logo_label.grid(row=0, column=0, padx=20, pady=(20, 10))

        # Add a search button to the sidebar
        self.search_button = ctk.CTkButton(self.sidebar, text="Search", command=self.show_search, corner_radius=10)
        self.search_button.grid(row=1, column=0, padx=20, pady=10)

        # Add an exit button to the sidebar
        self.exit_button = ctk.CTkButton(self.sidebar, text="Exit", command=self.quit, corner_radius=10)
        self.exit_button.grid(row=3, column=0, padx=20, pady=10)

        # Content Area
        self.content_frame = ctk.CTkFrame(self, corner_radius=10)
        self.content_frame.grid(row=0, column=1, sticky="nsew", padx=20, pady=20)
        self.content_frame.grid_rowconfigure(0, weight=1)
        self.content_frame.grid_columnconfigure(0, weight=1)

        # Start with Search Screen
        self.show_search()

    def show_search(self):
        # Clear existing widgets and prepare the search UI
        for widget in self.content_frame.winfo_children():
            widget.destroy()

        search_frame = ctk.CTkFrame(self.content_frame)
        search_frame.pack(fill="both", expand=True)

        search_label = ctk.CTkLabel(search_frame, text="Search for Music", font=("Arial", 24, "bold"))
        search_label.pack(pady=20)

        search_entry = ctk.CTkEntry(search_frame, placeholder_text="Enter song, artist, or album...")
        search_entry.pack(pady=10, padx=50, fill="x")

        # Button to initiate search
        search_button = ctk.CTkButton(search_frame, text="Search", command=lambda: self.search_music(search_entry.get(), search_frame))
        search_button.pack(pady=10)

        self.status_label = ctk.CTkLabel(search_frame, text="")
        self.status_label.pack(pady=10)

    def search_music(self, query, parent_frame):
        # Clear previous results before displaying new search results
        for widget in parent_frame.winfo_children():
            if isinstance(widget, ctk.CTkFrame) and widget != parent_frame:
                widget.destroy()
                    # If no search query is provided, display an error message
        if not query:
            self.status_label.configure(text="Please enter a search term.", text_color="red")
            return

        # Indicate that the search is in progress
        self.status_label.configure(text="Searching...", text_color="lightgreen")
        self.update_idletasks()  # Ensure the UI is updated before proceeding

        # Perform the YouTube search using the query
        self.track_results = search_youtube(query)
        print("Search Results:", self.track_results)  # Debugging: Print the search results to the console

        # If no results are found, update the status label and return
        if not self.track_results:
            self.status_label.configure(text="No results found.", text_color="red")
            return

        # Create a new frame to hold the search results
        results_frame = ctk.CTkFrame(parent_frame)
        results_frame.pack(fill="both", expand=True)

        # Loop through the search results and create a button for each video
        for i, video in enumerate(self.track_results):
            video_title = video["snippet"]["title"]  # Extract the video title
            video_url = f"https://www.youtube.com/watch?v={video['id']['videoId']}"  # Construct the video URL
            channel_name = video["snippet"]["channelTitle"]  # Extract the channel name
            
            # Create a frame to display the track info
            track_frame = ctk.CTkFrame(results_frame, corner_radius=10)
            track_frame.pack(pady=5, padx=10, fill="x")

            # Add the video title as a label
            track_label = ctk.CTkLabel(track_frame, text=f"{i + 1}. {video_title}", anchor="w")
            track_label.pack(side="left", fill="x", expand=True, padx=10)

            # Add the "Download" button to each video result
            download_button = ctk.CTkButton(
                track_frame, 
                text="Download", 
                command=lambda v_url=video_url, v_title=video_title, v_channel=channel_name: self.download_track(v_url, v_title, v_channel)
            )
            download_button.pack(side="right", padx=10)

        # Indicate that the search has completed
        self.status_label.configure(text="Search completed!", text_color="lightgreen")

    def download_track(self, video_url, video_title, channel_name):
        # Update status label indicating the download is starting
        self.status_label.configure(text="Downloading...", text_color="lightgreen")
        self.update_idletasks()

        # Perform the download and get the file path
        file_path, message = download_youtube_audio(video_url, video_title, DOWNLOAD_FOLDER)

        # If the download is successful, write the song details to the CSV file
        if file_path:
            rating = random.randint(1, 5)  # Simulate a random rating for the track
            write_to_csv(video_title, channel_name, file_path, rating, plays=0)  # Save song details to CSV

            # Update the status label with success message
            self.status_label.configure(text=f"Downloaded {video_title}!", text_color="lightgreen")
        else:
            # If the download fails, show the error message
            self.status_label.configure(text=message, text_color="red")

    def show_downloads(self):
        # Clear the content and prepare to display downloaded tracks
        for widget in self.content_frame.winfo_children():
            widget.destroy()

        # Create a frame to hold the downloaded tracks list
        downloads_frame = ctk.CTkFrame(self.content_frame)
        downloads_frame.pack(fill="both", expand=True)

        # Display the heading for downloaded tracks
        downloads_label = ctk.CTkLabel(downloads_frame, text="Downloaded Tracks", font=("Arial", 24, "bold"))
        downloads_label.pack(pady=20)

        # Try to open and read the CSV file containing the downloaded tracks
        try:
            with open("songs_list.csv", mode="r", encoding="utf-8") as file:
                reader = csv.reader(file)
                next(reader)  # Skip header row
                for row in reader:
                    track_id, id_number, song_name, singer, file_path, rating = row

                    # Create a frame to display each downloaded song's information
                    song_frame = ctk.CTkFrame(downloads_frame, corner_radius=10)
                    song_frame.pack(fill="x", pady=5, padx=10)

                    # Label showing track details (ID, name, singer, and rating)
                    song_label = ctk.CTkLabel(song_frame, text=f"Track ID: {track_id} - {song_name} by {singer} | Rating: {rating}")
                    song_label.pack(side="left", fill="x", expand=True, padx=10)

                    # Button to play the song from the downloaded file
                    play_button = ctk.CTkButton(song_frame, text="Play", command=lambda fp=file_path: self.play_song(fp))
                    play_button.pack(side="right", padx=10)

        except FileNotFoundError:
            # If the CSV file is not found, show a message indicating no downloads yet
            self.status_label.configure(text="No songs downloaded yet.", text_color="red")

    

# Create and run the application
if __name__ == "__main__":
    app = YouTubeApp()  # Create an instance of the YouTubeApp class
    app.mainloop()  # Start the main event loop to run the GUI

        #
