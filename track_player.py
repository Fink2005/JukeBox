# Import necessary libraries
import customtkinter as ctk  # CustomTkinter for building the GUI with modern elements
import subprocess  # To run external scripts (like Python scripts) from within the program
import threading  # To allow concurrent execution of functions (e.g., running the YouTube script in a separate thread)
import font_manager  # Import the custom font manager for consistent font usage across the app

# Define the main application class, inheriting from CTk for creating a CustomTkinter app
class JukeBoxApp(ctk.CTk):

    # Initialization method to configure the window
    def __init__(self):
        super().__init__()

        # Configure window properties (title, size, appearance mode, and theme)
        self.title("JukeBox")  # Set the title of the window
        self.geometry("600x300")  # Set the size of the window (width x height)
        ctk.set_appearance_mode("Dark")  # Enable dark mode for the app's appearance
        ctk.set_default_color_theme("blue")  # Set the color theme to blue for consistency in the UI

        # Create a frame that holds the main content of the window
        self.main_frame = ctk.CTkFrame(self)  # Create a frame widget
        self.main_frame.pack(pady=20, padx=20, fill="both", expand=True)  # Pack the frame with padding and allow expansion

        # Header Label displaying an introductory message
        self.header_label = ctk.CTkLabel(
            self.main_frame,  # Attach the label to the main_frame
            text="Select an option by clicking one of the buttons below",  # Text to be displayed
            font=font_manager.FONT_BOLD,  # Use the bold font style from font_manager
            wraplength=500,  # Set the maximum line width for text wrapping
            justify="center",  # Center-align the text
        )
        self.header_label.pack(pady=10)  # Pack the label with padding for spacing

        # Buttons to trigger different actions in the app

        # Button to trigger YouTube functionality
        self.youtube_button = ctk.CTkButton(
            self.main_frame, text="Youtube", command=self.run_youtube_script  # Button text and command to run YouTube-related functionality
        )
        self.youtube_button.pack(pady=10)  # Pack the button with padding between buttons

        # Button to view tracks
        self.view_button = ctk.CTkButton(
            self.main_frame, text="View Tracks", command=self.view_tracks  # Button text and command to show tracks
        ) 
        self.view_button.pack(pady=10)  # Pack the button with padding

        # Button to create the track list
        self.create_button = ctk.CTkButton(
            self.main_frame, text="Create Track List", command=self.create_track_list  # Button text and command to create track list
        )
        self.create_button.pack(pady=10)  # Pack the button with padding

        # Button to update tracks (presumably for modifying the existing track list)
        self.update_button = ctk.CTkButton(
            self.main_frame, text="Update Tracks", command=self.update_tracks  # Button text and command to update tracks
        )
        self.update_button.pack(pady=10)  # Pack the button with padding

        # Status Label to display messages regarding the button clicks or any status updates
        self.status_label = ctk.CTkLabel(
            self.main_frame, text="", font=font_manager.FONT_PRIMARY, text_color="lightgreen"  # Use the primary font and set green text color
        )
        self.status_label.pack(pady=10)  # Pack the label with padding

    # Method to be executed when the "View Tracks" button is clicked
    def view_tracks(self):
        self.update_status("View Tracks button was clicked!")  # Update the status label with a message
        subprocess.run(["python", "view_tracks.py"])  # Run the 'view_tracks.py' script using subprocess

    # Method to be executed when the "Create Track List" button is clicked
    def create_track_list(self):
        self.update_status("Create Track List button was clicked!")  # Update the status label with a message
        subprocess.run(["python", "create_track_list.py"])  # Run the 'create_track_list.py' script using subprocess

    # Method to be executed when the "Update Tracks" button is clicked
    def update_tracks(self):
        self.update_status("Update Tracks button was clicked!")  # Update the status label with a message
        subprocess.run(["python", "update_tracks.py"])  # Run the 'update_tracks.py' script using subprocess

    # Method to be executed when the "Youtube" button is clicked
    def run_youtube_script(self):
        threading.Thread(target=self.youtube).start()  # Run the youtube method in a new thread to prevent blocking the UI

    # Method to execute YouTube-related functionality
    def youtube(self):
        self.update_status("Youtube button was clicked!")  # Update the status label with a message
        subprocess.run(["python", "youtube.py"])  # Run the 'youtube.py' script using subprocess

    # Method to update the status label with the provided message
    def update_status(self, message):
        self.status_label.configure(text=message)  # Update the status label's text to the provided message


# Main block to run the application
if __name__ == "__main__":
    app = JukeBoxApp()  # Create an instance of the JukeBoxApp class
    app.mainloop()  # Start the main event loop for the application
