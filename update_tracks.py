import customtkinter as ctk
import track_library as lib
import font_manager

class TrackViewer(ctk.CTk):

    def __init__(self):
        super().__init__()

        # Configure the main window
        self.title("Track Viewer")
        self.geometry("1000x500")
        ctk.set_appearance_mode("Dark")  # Enable dark mode
        ctk.set_default_color_theme("blue")  # Set the color theme

        # Variables
        self.track_number_var = ctk.StringVar()
        self.new_rating_var = ctk.StringVar()
        self.new_name_var = ctk.StringVar()
        self.new_artist_var = ctk.StringVar()

        # Create layout
        self.create_widgets()

        # Automatically update the track list when the app starts
        self.update_track_list()

    def create_widgets(self):
        # Input Frame (Track Number, New Rating)
        input_frame = ctk.CTkFrame(self, corner_radius=10)
        input_frame.pack(pady=10, padx=10, fill="x")

        ctk.CTkLabel(input_frame, text="Enter Track ID").grid(row=0, column=0, padx=10, pady=10)

        # Create a validation function to allow only numeric input
        validate_input = self.register(self.validate_numeric_input)

        # Track number entry with validation
        self.track_number_entry = ctk.CTkEntry(input_frame, textvariable=self.track_number_var, validate="key", validatecommand=(validate_input, "%S"))
        self.track_number_entry.grid(row=0, column=1, padx=10, pady=10)

        self.view_button = ctk.CTkButton(input_frame, text="View Track", command=self.view_track)
        self.view_button.grid(row=0, column=2, padx=10, pady=10)

        ctk.CTkLabel(input_frame, text="Enter New Rating (1 to 5)").grid(row=0, column=3, padx=10, pady=10)
        self.new_rating_entry = ctk.CTkEntry(input_frame, textvariable=self.new_rating_var,validate="key", validatecommand=(validate_input, "%S"))
        self.new_rating_entry.grid(row=0, column=4, padx=10, pady=10)

        
        self.update_button = ctk.CTkButton(input_frame, text="Update Rating", command=self.update_rating)
        self.update_button.grid(row=0, column=5, padx=0, pady=10)

        # New Update Box for Updating Name and Artist
        update_frame = ctk.CTkFrame(self, corner_radius=10)
        update_frame.pack(pady=10, padx=10, fill="x")

        ctk.CTkLabel(update_frame, text="New Track Name").grid(row=0, column=0, padx=10, pady=10)
        self.new_name_entry = ctk.CTkEntry(update_frame, textvariable=self.new_name_var)
        self.new_name_entry.grid(row=0, column=1, padx=10, pady=10)

        ctk.CTkLabel(update_frame, text="New Artist").grid(row=0, column=2, padx=10, pady=10)
        self.new_artist_entry = ctk.CTkEntry(update_frame, textvariable=self.new_artist_var)
        self.new_artist_entry.grid(row=0, column=3, padx=10, pady=10)

        self.update_track_button = ctk.CTkButton(update_frame, text="Update Track", command=self.update_track)
        self.update_track_button.grid(row=0, column=4, padx=10, pady=10)

        # Text Display Frame (Track List and Details)
        text_frame = ctk.CTkFrame(self, corner_radius=10)
        text_frame.pack(pady=10, padx=10, fill="both", expand=True)

        self.track_list_textbox = ctk.CTkTextbox(text_frame, width=500, height=200)
        self.track_list_textbox.grid(row=0, column=0, padx=10, pady=10, sticky="nsew")

        self.track_details_textbox = ctk.CTkTextbox(text_frame, width=300, height=100)
        self.track_details_textbox.grid(row=0, column=1, padx=10, pady=10, sticky="nsew")

        # Expandable row and column for text_frame
        text_frame.grid_rowconfigure(0, weight=1)
        text_frame.grid_columnconfigure(0, weight=2)
        text_frame.grid_columnconfigure(1, weight=1)

        # Status Label
        self.status_label = ctk.CTkLabel(self, text="", font=font_manager.FONT_BOLD, text_color="lightgreen")
        self.status_label.pack(pady=5)

    def validate_numeric_input(self, input_value):
        """Only allows numeric input"""
        if input_value.isdigit():  # Allow only digits 
            return True
        else:
            return False

    def update_track_list(self):
        # Load the songs from CSV using the function from track_library.py
        track_list = lib.load_songs_from_csv()  # Call function to load tracks from CSV
        
        if not track_list:
            self.status_label.configure(text="No tracks available.", text_color="red")
            return
        
        self.track_list_textbox.configure(state="normal")
        self.track_list_textbox.delete("1.0", "end")
        
        # List all tracks in the textbox with Name, Singer, and Rating
        for track_id, track in track_list.items():
            # Displaying the Track Name, Singer, and Rating in the list
            self.track_list_textbox.insert("end", f"Name: {track.name}, Singer: {track.artist}, Rating: {track.rating}\n \n")
        
        self.track_list_textbox.configure(state="disabled")

    def view_track(self):
        # Get the track ID from the input field
        track_id = self.track_number_var.get()
        

        # Retrieve the track using the track ID from track_library
        track = lib.get_track_by_id(track_id)

        self.track_details_textbox.configure(state="normal")
        self.track_details_textbox.delete("1.0", "end")

        # If the track exists, show its details; otherwise, show an error message
        if track:
            track_details = f"Track ID: {track_id}\nName: {track.name}\nArtist: {track.artist}\nRating: {track.rating}"
            self.track_details_textbox.insert("1.0", track_details)
            self.status_label.configure(text=f"Track {track_id} found.", text_color="lightgreen")
        # Validate, if view_track input is null the error will be displayed
        elif (len(track_id) == 0): {
             self.status_label.configure(
                text=f"View Track input should not be null ", text_color="red"
            )
        }
        # Validate, if view_track input start at 0 the error will be displayed
        
        elif ( track_id[0] != '0' and track_id[0] != '' and len(track_id) == 1  ):           
             self.status_label.configure(
                text=f"View Track input should start at 0 => 01 , 02 ,etc ", text_color="red"
            )
        #If track not found, show message
        else:
            self.track_details_textbox.insert("1.0", f"Track {track_id} not found.")
            self.status_label.configure(text=f"Track {track_id} not found.", text_color="red")

        self.track_details_textbox.configure(state="disabled")

    def update_rating(self):
        track_id = self.track_number_var.get()
        new_rating = self.new_rating_var.get()
        
        # Validate the rating input
        if not new_rating.isdigit() or int(new_rating) < 1 or int(new_rating) > 5:
            self.status_label.configure(text="Invalid rating. Enter a number from 1 to 5.", text_color="red")
            return

        track = lib.get_track_by_id(track_id)

        if track:
            # Update the track rating in track_library
            lib.set_rating(track_id, int(new_rating))
            self.status_label.configure(text=f"Rating updated for Track {track_id}.", text_color="lightgreen")
            self.view_track()  # Refresh the track details after update
            self.update_track_list()  # Refresh the track list after update
        else:
            self.status_label.configure(text=f"Track {track_id} not found.", text_color="red")

    def update_track(self):
        track_id = self.track_number_var.get()
        new_name = self.new_name_var.get()
        new_artist = self.new_artist_var.get()

        # Validate the input fields
        if not new_name or not new_artist:
            self.status_label.configure(text="Both name and artist must be provided.", text_color="red")
            return

        track = lib.get_track_by_id(track_id)

        if track:
            # Update the track name and artist in track_library
            lib.set_name(track_id, new_name)
            lib.set_artist(track_id, new_artist)

            # Show success message
            self.status_label.configure(text=f"Track {track_id} updated successfully!", text_color="lightgreen")
            self.view_track()  # Refresh the track details after update
            self.update_track_list()  # Refresh the track list after update
        else:
            self.status_label.configure(text=f"Track {track_id} not found.", text_color="red")


if __name__ == "__main__":
    app = TrackViewer()
    app.mainloop()
