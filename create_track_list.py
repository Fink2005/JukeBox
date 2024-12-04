import customtkinter as ctk  # Import customtkinter for GUI components
import track_library as lib  # Import the track_library module to manage tracks
import font_manager  # Import font_manager for custom fonts
import pygame  # Import pygame for audio playback

class CreateViewer(ctk.CTk):  # Define the CreateViewer class inheriting from customtkinter's CTk
    def __init__(self):
        super().__init__()  # Initialize the parent class (CTk)

        lib.load_songs_from_csv()  # Load the songs from the CSV file into the track library
        pygame.mixer.init()  # Initialize pygame mixer for audio playback

        # Configure window settings
        self.title("Create Track List")  # Set the title of the window
        self.geometry("800x650")  # Set window size (800x600)
        self.resizable(True, True)  # Allow the window to be resizable
        ctk.set_appearance_mode("Dark")  # Set appearance mode to dark
        ctk.set_default_color_theme("blue")  # Set the default color theme to blue

        # Header Section
        self.header_frame = ctk.CTkFrame(self, corner_radius=10)  # Create a frame for the header section
        self.header_frame.pack(pady=10, padx=10, fill="x")  # Pack the frame to fill the width
        self.title_label = ctk.CTkLabel(
            self.header_frame, 
            text="JukeBox Playlist Manager",  # Set the title text for the header
            font=("Arial", 20, "bold"),  # Set font to Arial, 20pt, bold
        )
        self.title_label.grid(row=0, column=1, padx=10)  # Place the title label in the first row, second column

        # Input Section
        self.input_frame = ctk.CTkFrame(self, corner_radius=10)  # Create a frame for user input
        self.input_frame.pack(pady=10, padx=10, fill="x")  # Pack the input frame to fill the width
        self.input_label = ctk.CTkLabel(self.input_frame, text="Enter Track ID:", font=font_manager.FONT_BOLD)
        self.input_label.grid(row=0, column=0, padx=10, pady=15)  # Add a label for the track ID input

        # Validation function to only allow numeric input for track ID
        validate_input = self.register(self.validate_numeric_input)

        # Track number entry with validation (only numbers allowed)
        self.input_text = ctk.CTkEntry(self.input_frame, placeholder_text="Track ID", font=font_manager.FONT_SECONDARY,
                                       validate="key", validatecommand=(validate_input, "%S"))
        self.input_text.grid(row=0, column=1, padx=10, pady=10)  # Input field for the track ID

        # Button to view and play the track
        self.view_button = ctk.CTkButton(self.input_frame, text="View & Play Track", command=self.play_and_view_track, font=font_manager.FONT_SECONDARY)
        self.view_button.grid(row=0, column=2, padx=10, pady=10)

        # Button to stop music
        self.stop_button = ctk.CTkButton(self.input_frame, text="Stop", command=self.stop_music, font=font_manager.FONT_SECONDARY)
        self.stop_button.grid(row=0, column=3, padx=10, pady=10)

        # Track Details Section
        self.details_frame = ctk.CTkFrame(self, corner_radius=10)  # Frame for track details
        self.details_frame.pack(pady=10, padx=10, fill="x")
        self.details_label = ctk.CTkLabel(self.details_frame, text="Track Details:", font=font_manager.FONT_BOLD)
        self.details_label.grid(row=0, column=0, padx=10, pady=10, sticky="w")  # Label for track details
        self.details_text = ctk.CTkTextbox(self.details_frame, width=400, height=150)  # Textbox to show track details
        self.details_text.grid(row=1, column=0, columnspan=2, padx=10, pady=10)

        # List of Tracks Section
        self.track_list_frame = ctk.CTkFrame(self, corner_radius=10)  # Frame for the list of tracks
        self.track_list_frame.pack(pady=10, padx=10, fill="x")
        self.track_list_label = ctk.CTkLabel(self.track_list_frame, text="List of Tracks:", font=font_manager.FONT_BOLD)
        self.track_list_label.grid(row=0, column=0, padx=10, pady=10, sticky="w")  # Label for the track list
        self.track_list_text = ctk.CTkTextbox(self.track_list_frame, width=400, height=150)  # Textbox for displaying the track list
        self.track_list_text.grid(row=1, column=0, columnspan=2, padx=10, pady=10)
        
        
        
        
        self.status_label = ctk.CTkLabel(
        self, text="", font=font_manager.FONT_SECONDARY, text_color="lightgreen"
        )  # Create a label to display status messages
        self.status_label.pack(pady=5)  # Pack the status label with padding
        
        
        # List to store track names and play counts
        self.track_names = {}

    # Method to validate that the input is numeric
    def validate_numeric_input(self, input_value):
        """Only allows numeric input"""
        if input_value.isdigit():  # Allow only digits 
            return True
        else:
            return False

    # Method to play and view the track details
    def play_and_view_track(self):
        key = self.input_text.get()  # Get the track ID entered by the user
        name = lib.get_name(key)  # Get the track name from the library based on the track ID
        play_count = lib.get_play_count(key)  # Get the current play count for the track
        source = lib.get_music_source(key)  # Get the source (file path) for the track

        if name:  # If the track is found
            artist = lib.get_artist(key)  # Get the artist for the track
            rating = lib.get_rating(key)  # Get the rating for the track
            track_details = f"Name: {name}\nArtist: {artist}\nRating: {rating}"  # Format the track details

            # If the track is already in the list, increment the play count
            if name in self.track_names:
                self.track_names[name] += 1
                lib.increment_play_count(key)  # Increment the play count in the track library
                lib.set_play_count(key)  # Update the play count in the library
            else:
                self.track_names[name] = 1  # Add the track to the list with a play count of 1
                lib.increment_play_count(key)  # Increment the play count in the track library
                lib.set_play_count(key)  # Update the play count in the library

            self.update_track_list()  # Update the track list UI with the latest play counts

            # Show the track details in the textbox
            self.details_text.configure(state="normal")
            self.details_text.delete("1.0", "end")
            self.details_text.insert("1.0", track_details)
            self.details_text.configure(state="disabled")

            # Play the track if the source is available
      
            if source:
                pygame.mixer.music.load(source)  # Load the track audio file
                pygame.mixer.music.play()  # Play the track
            else:
                self.details_text.configure(state="normal")
                self.details_text.insert("1.0", "\nTrack file not found!")  # Show an error if the track file is not found
                self.details_text.configure(state="disabled")
                
        # Validate, if view_track input is null the error will be displayed
        
        elif (len(key) == 0): {
             self.status_label.configure(
                text=f"View Track input should not be null ", text_color="red"
            )
        }
        # Validate, if view_track input start at 0 the error will be displayed
        
        elif ( key[0] != '0' and key[0] != '' and len(key) == 1  ):           
             self.status_label.configure(
                text=f"View Track input should start at 0 => 01 , 02 ,etc ", text_color="red"
            )      
        else:
            self.details_text.configure(state="normal")
            self.details_text.delete("1.0", "end")
            self.details_text.insert("1.0", "Track not found")  # Show error message if track is not found
            self.details_text.configure(state="disabled")

    # Method to stop the music playback
    def stop_music(self):
        pygame.mixer.music.stop()  # Stop the music playback
        self.details_text.configure(state="normal")
        self.details_text.delete("1.0", "end")  # Clear the track details
        self.details_text.configure(state="disabled")

        # Clear the track names and play counts when stopping
        self.track_names.clear()  # Clear the track list
        self.update_track_list()  # Update the UI to reflect the cleared track list

    # Method to update the track list display
    def update_track_list(self):
        self.track_list_text.configure(state="normal")  # Make the track list textbox editable
        self.track_list_text.delete("1.0", "end")  # Clear the current track list
        for i, (track_name, play_count) in enumerate(self.track_names.items()):  # Loop through the track names and play counts
            self.track_list_text.insert("end", f"{i + 1}. {track_name} (Play Count: {play_count})\n")  # Display each track in the list
        self.track_list_text.configure(state="disabled")  # Make the track list textbox read-only

# Main execution
if __name__ == "__main__":
    app = CreateViewer()  # Create an instance of the CreateViewer
    app.mainloop()
