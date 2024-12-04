# Importing necessary libraries and modules
import customtkinter as ctk  # CustomTkinter for creating the GUI
import track_library as lib  # Import the track library where tracks data is handled
import font_manager  # Import the font manager to handle font styling

# Create the main application window class (TrackViewer)
class TrackViewer(ctk.CTk):

    # Initialization method to set up the application window
    def __init__(self):
        super().__init__()

        # Configure the main window settings
        self.title("Track Viewer")  # Set the title of the window
        self.geometry("800x500")  # Set the size of the window
        ctk.set_appearance_mode("Dark")  # Set dark mode for the window
        ctk.set_default_color_theme("blue")  # Set the default color theme to blue

        # Create the layout and widgets for the window
        self.create_widgets()

        # Load songs from CSV on startup
        lib.load_songs_from_csv()  # Call the function to load songs from the CSV file using the track library

    # Method to create and arrange widgets in the window
    def create_widgets(self):
        # Header Frame (holds the header label)
        header_frame = ctk.CTkFrame(self, corner_radius=10)  # Create a frame for the header
        header_frame.pack(pady=10, padx=10, fill="x")  # Pack the frame with padding and stretching in the X direction

        # Header label to display "Track Viewer"
        self.header_label = ctk.CTkLabel(
            header_frame,  # Set the parent frame for the label
            text="Track Viewer",  # The text that will be shown in the label
            font=font_manager.FONT_SECONDARY,  # Use the secondary font defined in font_manager
        )
        self.header_label.pack(pady=10)  # Pack the label with padding

        # Input and Buttons Frame (holds the user input fields and buttons)
        input_frame = ctk.CTkFrame(self, corner_radius=10)  # Create a frame for inputs and buttons
        input_frame.pack(pady=10, padx=10, fill="x")  # Pack the input frame

        # Button to list all tracks
        self.list_button = ctk.CTkButton(
            input_frame, text="List All Tracks", command=self.list_all_tracks
        )  # Create a button with text "List All Tracks"
        self.list_button.grid(row=0, column=0, padx=10, pady=10)  # Place the button in the frame using grid layout

        # Label asking for track number input
        self.track_num_label = ctk.CTkLabel(
            input_frame, text="Enter Track Number:", font=font_manager.FONT_BOLD
        )  # Create the label asking the user for track number input
        self.track_num_label.grid(row=0, column=1, padx=10, pady=10)  # Position the label

        # Create a validation function to only allow numeric input
        validate_input = self.register(self.validate_numeric_input)

        # Track number entry field with validation (only numeric values allowed)
        self.track_num_entry = ctk.CTkEntry(input_frame,
                                             validate="key",  # Enable validation on key press
                                             validatecommand=(validate_input, "%S"))  # Validate the input using the function
        self.track_num_entry.grid(row=0, column=2, padx=10, pady=10)  # Position the entry field

        # Button to view a specific track
        self.view_button = ctk.CTkButton(
            input_frame, text="View Track", command=self.view_track
        )  # Create the button to view the track details
        self.view_button.grid(row=0, column=3, padx=10, pady=10)  # Position the button

        # Text Display Frame (for displaying track list and track details)
        text_frame = ctk.CTkFrame(self, corner_radius=10)  # Create a frame to hold text boxes
        text_frame.pack(pady=10, padx=10, fill="both", expand=True)  # Pack the text frame

        # Textbox for listing all tracks
        self.list_textbox = ctk.CTkTextbox(text_frame, width=400, height=200)  # Create a textbox for track list
        self.list_textbox.grid(row=0, column=0, padx=10, pady=10, sticky="nsew")  # Place the textbox

        # Textbox for displaying track details
        self.track_textbox = ctk.CTkTextbox(text_frame, width=200, height=100)  # Create a textbox for track details
        self.track_textbox.grid(row=0, column=1, padx=10, pady=10, sticky="nsew")  # Place the textbox

        # Make the first row and columns expandable for responsive design
        text_frame.grid_rowconfigure(0, weight=1)  # Make the row expand
        text_frame.grid_columnconfigure(0, weight=2)  # Make the first column expand more
        text_frame.grid_columnconfigure(1, weight=1)  # Make the second column expand less

        # Status Label (for displaying messages like success or error)
        self.status_label = ctk.CTkLabel(
            self, text="", font=font_manager.FONT_SECONDARY, text_color="lightgreen"
        )  # Create a label to display status messages
        self.status_label.pack(pady=5)  # Pack the status label with padding

    # Function to validate numeric input (only numbers allowed)
    def validate_numeric_input(self, input_value):
        """Only allows numeric input"""
        if input_value.isdigit():  # Allow only digits
            return True
        else:
            return False

    # Function to list all tracks
    def list_all_tracks(self):
        track_list = lib.list_all()  # Fetch all tracks from the loaded data
        self.list_textbox.configure(state="normal")  # Enable editing the textbox
        self.list_textbox.delete("1.0", "end")  # Clear the existing content

        # Insert all track details into the textbox
        self.list_textbox.insert("1.0", track_list)  # Insert the list of tracks
        self.list_textbox.configure(state="disabled")  # Disable editing the textbox

        self.status_label.configure(text="List Tracks button was clicked!")  # Update status message

    # Function to view the track details based on user input (Track ID)
    def view_track(self):
        key = self.track_num_entry.get()  # Get the track number entered by the user
        name = lib.get_name(key)  # Retrieve track name using the track ID
        self.track_textbox.configure(state="normal")  # Enable editing the textbox
        self.track_textbox.delete("1.0", "end")  # Clear the existing content
        
     
        
        # If the track exists, display its details
        if name is not None:
            artist = lib.get_artist(key)  # Get track artist
            rating = lib.get_rating(key)  # Get track rating
            play_count = lib.get_play_count(key)  # Get track play count
            track_details = f"Name: {name}\nArtist: {artist}\nRating: {rating}\nPlays: {play_count}"
            self.track_textbox.insert("1.0", track_details)  # Insert the track details into the textbox
            self.status_label.configure(
                text=f"View Track button was clicked! Track {key} found.", text_color="lightgreen"
            )
            
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
            
            self.track_textbox.insert("1.0", f"Track {key} not found")  # If track not found, show message

            self.status_label.configure(
                text=f"View Track button was clicked! Track {key} not found.", text_color="red"
            )

        self.track_textbox.configure(state="disabled")  # Disable editing the textbox after displaying details

# Run the application
if __name__ == "__main__":
    app = TrackViewer()  # Create an instance of the TrackViewer class
    app.mainloop()  # Start the main event loop
