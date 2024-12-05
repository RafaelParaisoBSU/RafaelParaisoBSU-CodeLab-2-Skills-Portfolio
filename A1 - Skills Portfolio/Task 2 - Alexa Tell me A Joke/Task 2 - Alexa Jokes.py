# Import the customtkinter library for creating modern-looking Tkinter widgets
import customtkinter

# Import the standard tkinter library for creating GUI applications
import tkinter as tk

# Import the PIL library for handling images, including GIFs
from PIL import Image, ImageTk, ImageSequence

# Import the random module to select random jokes from a list
import random

# Import the os module for interacting with the operating system, such as file paths
import os

# Import the pyttsx3 library for text-to-speech functionality
import pyttsx3

# Import the threading module to handle concurrent execution of threads
import threading

# Import the pygame library for handling audio playback
import pygame

# Configure the appearance mode to light and set the default color theme to dark blue for the customtkinter widgets
customtkinter.set_appearance_mode("Dark")  # Modes: "System" (standard), "Dark", "Light"
customtkinter.set_default_color_theme("A1 - Skills Portfolio\\Task 2 - Alexa Tell me A Joke\\Assets\\pink.json")

# Initialize the Pygame mixer to handle audio playback within the application
pygame.mixer.init()

# Define the initial volume levels for background music and sound effects
initial_bgm_volume = 0.25  # This sets the initial volume for background music to 25%
initial_sfx_volume = 0.5   # This sets the initial volume for sound effects to 50%

def update_bgm_volume(volume):
    """Adjust the background music volume based on the slider's value."""
    pygame.mixer.music.set_volume(float(volume) / 100)

def update_sfx_volume(volume):
    """Adjust the sound effect volume based on the slider's value."""
    button_sound_effect.set_volume(float(volume) / 100)

def bgmusic():
    """Load and continuously play the background music on a loop."""
    pygame.mixer.music.load("A1 - Skills Portfolio\\Task 2 - Alexa Tell me A Joke\\Assets\\The Builder.mp3")
    pygame.mixer.music.set_volume(initial_bgm_volume)
    pygame.mixer.music.play(loops=-1)

# Start playing the background music as soon as the application launches
bgmusic()

# Load the button click sound effect and set its initial volume
button_sound_effect = pygame.mixer.Sound("A1 - Skills Portfolio\\Task 2 - Alexa Tell me A Joke\\Assets\\Robot Click Sound Effect.mp3")
button_sound_effect.set_volume(initial_sfx_volume)

def buttonsound():
    """Play the button click sound effect when a button is pressed."""
    button_sound_effect.play()

# Initialize the main application window using customtkinter
root = customtkinter.CTk()
root.title("Alexa Joke Teller")  # Set the window title to "Alexa Joke Teller"
root.geometry("1280x720")        # Define the window size as 1280x720 pixels
root.resizable(False, False)     # Prevent the window from being resizable

# Define different frames within the application for organizing content
title_frame = customtkinter.CTkFrame(root)
main_frame = customtkinter.CTkFrame(root)
options_frame = customtkinter.CTkFrame(root)

# Initialize the text-to-speech engine using pyttsx3
engine = pyttsx3.init()
engine_lock = threading.Lock()  # Create a lock to manage concurrent access to the TTS engine

# Configure the speech rate and select the second available voice for the TTS engine
engine.setProperty('rate', 200)
voices = engine.getProperty('voices')
engine.setProperty('voice', voices[1].id)

def resource_path(relative_path):
    """Construct the absolute path to a resource file within the project directory."""
    return os.path.join("A1 - Skills Portfolio\\Task 2 - Alexa Tell me A Joke\\Assets", relative_path)

def load_gif(widget, gif_path, update_interval=14):
    """Load a GIF image and animate it on the specified widget at the given interval."""
    gif_image = Image.open(resource_path(gif_path))  # Open the GIF image from the resource path
    frames = [ImageTk.PhotoImage(frame.convert("RGBA")) for frame in ImageSequence.Iterator(gif_image)]
    frame_count = len(frames)

    def update_frame(frame_index=0):
        """Update the widget with the next frame of the GIF animation."""
        frame_index = (frame_index + 1) % frame_count
        widget.configure(image=frames[frame_index])
        widget.image = frames[frame_index]                        # Keep a reference to prevent garbage collection
        widget.after(update_interval, update_frame, frame_index)  # Schedule the next frame update

    widget.configure(image=frames[0])  # Set the initial frame of the GIF
    widget.image = frames[0]
    update_frame()                     # Start the animation loop

# Load the background image for the options frame and set its size to cover the entire window
options_bg_image = customtkinter.CTkImage(
    Image.open(resource_path("alexaoptions.png")), size=(1280, 720)
)

# Position all frames to occupy the full window area
for frame in (title_frame, main_frame, options_frame):
    frame.place(relx=0, rely=0, relwidth=1, relheight=1)

def show_frame(frame):
    """Bring the specified frame to the front, making it visible to the user."""
    frame.tkraise()

# Load jokes from the "randomJokes.txt" file and store them as tuples of setup and punchline
jokes = []
with open(resource_path("randomJokes.txt"), 'r', encoding='utf-8') as f:
    for line in f:
        line = line.strip()
        if line and '?' in line:
            setup, punchline = line.split('?', 1)
            setup += '?'
            jokes.append((setup.strip(), punchline.strip()))

current_joke = None  # Initialize the variable to keep track of the current joke being displayed

def show_joke_setup():
    """Select a random joke and display its setup while preparing to show the punchline."""
    global current_joke
    current_joke = random.choice(jokes)          # Choose a random joke from the list
    joke_text.configure(text=current_joke[0])    # Display the joke's setup
    speak_text(current_joke[0])                  # Use TTS to speak the setup
    show_punchline_button.pack(pady=(10))        # Show the "Show Punchline" button
    tell_joke_button.pack_forget()               # Hide the "Tell Joke" button
    another_joke_button.pack_forget()            # Hide the "Another Joke" button
    quit_button.pack_forget()                    # Hide the "Quit" button

def show_joke_punchline():
    """Display the punchline of the current joke and provide options for another joke or quitting."""
    joke_text.configure(text=f"{current_joke[0]}\n\n{current_joke[1]}")  # Show both setup and punchline
    speak_text(current_joke[1])          # Use TTS to speak the punchline
    show_punchline_button.pack_forget()  # Hide the "Show Punchline" button
    another_joke_button.pack(pady=(10))  # Show the "Another Joke" button
    quit_button.pack(pady=10)            # Show the "Quit" button

def another_joke():
    """Reset the joke display area to prepare for displaying a new joke."""
    joke_text.configure(text="")          # Clear the current joke text
    tell_joke_button.pack(pady=(10))      # Show the "Tell Joke" button
    another_joke_button.pack_forget()     # Hide the "Another Joke" button
    quit_button.pack_forget()             # Hide the "Quit" button

def quit_button_click():
    """Handle the event when the user clicks the quit button, resetting the interface."""
    tell_joke_button.pack(pady=(10))      # Show the "Tell Joke" button
    joke_text.configure(text="")          # Clear the joke text
    show_punchline_button.pack_forget()   # Hide the "Show Punchline" button
    another_joke_button.pack_forget()     # Hide the "Another Joke" button
    quit_button.pack_forget()             # Hide the "Quit" button

def speak_text(text):
    """Use the text-to-speech engine to speak the provided text in a separate thread."""
    def run_speech():
        with engine_lock:       # Ensure that only one thread accesses the TTS engine at a time
            engine.say(text)    # Queue the text to be spoken
            engine.runAndWait() # Execute the speech

    threading.Thread(target=run_speech).start()  # Start the speech in a new thread to avoid blocking the main thread

# Add a background label to the title frame and place it to cover the entire frame
title_bg = customtkinter.CTkLabel(title_frame, text="")
title_bg.place(x=0, y=0, relwidth=1, relheight=1)

# Load and animate the title GIF on the title frame's background label
load_gif(title_bg, "alexatitle.gif")

# Create the "Start" button on the title frame with specified styling and functionality
title_start = customtkinter.CTkButton(
    title_frame,
    text="Start",
    width=200,
    height=75,
    font=("Montserrat", 32, "bold"),
    command=lambda: [show_frame(main_frame), buttonsound()],  # Switch to main frame and play button sound on click
)
title_start.pack(side="top", anchor="w", padx=(350, 50), pady=(475, 20))  # Position the "Start" button

# Create the "Options" button on the title frame with specified styling and functionality
title_options = customtkinter.CTkButton(
    title_frame,
    text="Options",
    width=200,
    height=75,
    font=("Montserrat", 32, "bold"),
    command=lambda: [show_frame(options_frame), buttonsound()],  # Switch to options frame and play button sound on click
    bg_color="blue",
)
title_options.pack(side="top", anchor="w", padx=(350, 50))  # Position the "Options" button

# Add a background image to the options frame and ensure it covers the entire frame
options_bg = customtkinter.CTkLabel(
    options_frame,
    image=options_bg_image,
    text=""
)
options_bg.place(relx=0, rely=0, relwidth=1, relheight=1)

# Add a header label for the audio settings in the options frame with specified styling
audio_header = customtkinter.CTkLabel(
    options_frame,
    text="Audio:",
    text_color="purple",
    bg_color="black",
    font=("Montserrat", 48, 'bold')
)
audio_header.pack(side=tk.TOP, pady=(300, 0))  # Position the audio header label

# Create and position the background music volume label in the options frame
bgm_volume_label = customtkinter.CTkLabel(
    options_frame,
    text="Background Music Volume:",
    font=('Poppins', 24, 'bold'),
    text_color="white",
    bg_color="black",
)
bgm_volume_label.pack(pady=(20, 0))  # Add spacing above the label

# Create and configure the background music volume slider with specified range and command
bgm_volume_slider = customtkinter.CTkSlider(
    options_frame,
    from_=0,
    to=100,
    orientation="horizontal",
    command=update_bgm_volume,  # Call the update_bgm_volume function when the slider is moved
    width=400,
    height=30,
    bg_color="black",
)
bgm_volume_slider.set(25)  # Set the initial position of the slider to match initial_bgm_volume
bgm_volume_slider.pack()    # Position the background music volume slider

# Create and position the sound effect volume label in the options frame
sfx_volume_label = customtkinter.CTkLabel(
    options_frame,
    text="Sound Effect Volume:",
    font=('Poppins', 24, 'bold'),
    text_color="white",
    bg_color="black",
)
sfx_volume_label.pack(pady=(20, 0))  # Add spacing above the label

# Create and configure the sound effect volume slider with specified range and command
sfx_volume_slider = customtkinter.CTkSlider(
    options_frame,
    from_=0,
    to=100,
    orientation="horizontal",
    command=update_sfx_volume,  # Call the update_sfx_volume function when the slider is moved
    width=400,
    height=30,
    bg_color="black",
)
sfx_volume_slider.set(50)  # Set the initial position of the slider to match initial_sfx_volume
sfx_volume_slider.pack()    # Position the sound effect volume slider

# Create the "BACK" button in the options frame to return to the title frame and play a button sound
options_back = customtkinter.CTkButton(
    options_frame,
    text="BACK",
    width=200,
    height=75,
    font=("Montserrat", 32, "bold"),
    bg_color="black",
    command=lambda: [show_frame(title_frame), buttonsound()]
)
options_back.pack(side="bottom", anchor="w", padx=(50, 50), pady=(0, 40))  # Position the "BACK" button at the bottom

# Add a background label to the main frame and place it to cover the entire frame
main_bg = customtkinter.CTkLabel(main_frame, text="")
main_bg.place(x=0, y=0, relwidth=1, relheight=1)

# Load and animate the main GIF on the main frame's background label
load_gif(main_bg, "alexamain.gif")

# Create a prompt label in the main frame to instruct the user on how to hear a joke
prompt_label = customtkinter.CTkLabel(
    main_frame,
    text='Tell Alexa to "Tell me a joke" to hear a joke',
    font=("Montserrat", 32, "bold"),
    text_color="white",
    fg_color="black",
)
prompt_label.pack(pady=(190, 10))  # Position the prompt label with vertical padding

# Create the "Alexa, Tell me a Joke!" button in the main frame to initiate joke telling and play a button sound
tell_joke_button = customtkinter.CTkButton(
    main_frame,
    text="Alexa, Tell me a Joke!",
    width=200,
    height=75,
    font=("Montserrat", 24, "bold"),
    bg_color="black",
    command=lambda: [show_joke_setup(), buttonsound()]  # Show joke setup and play sound when clicked
)
tell_joke_button.pack()  # Position the "Tell Joke" button

# Create a label in the main frame to display the joke setup and punchline
joke_text = customtkinter.CTkLabel(
    main_frame,
    text="",
    font=("Poppins", 24),
    wraplength=800,   # Allow text to wrap within 800 pixels for better readability
    justify="center",
    text_color="white",
    fg_color="black",
)
joke_text.pack(pady=(10))  # Position the joke text label with vertical padding

# Define the "Show Punchline" button but do not pack it initially; it will be displayed when appropriate
show_punchline_button = customtkinter.CTkButton(
    main_frame,
    text="Show Punchline",
    width=200,
    height=75,
    font=("Montserrat", 24, "bold"),
    bg_color="black",
    command=lambda: [show_joke_punchline(), buttonsound()]  # Show punchline and play sound when clicked
)

# Define the "Another Joke" button but do not pack it initially; it will be displayed after the punchline
another_joke_button = customtkinter.CTkButton(
    main_frame,
    text="Another Joke",
    width=200,
    height=75,
    font=("Montserrat", 24, "bold"),
    bg_color="black",
    command=lambda: [another_joke(), buttonsound()]  # Prepare for another joke and play sound when clicked
)

# Define the "Quit" button but do not pack it initially; it will be displayed after the punchline
quit_button = customtkinter.CTkButton(
    main_frame,
    text="Quit",
    width=200,
    height=75,
    font=("Montserrat", 24, "bold"),
    bg_color="black",
    command=lambda: [show_frame(title_frame), quit_button_click(), buttonsound()]  # Return to title frame, reset, and play sound when clicked
)

# Start the application by displaying the title frame first
show_frame(title_frame)

# Run the main event loop to keep the application window open and responsive to user interactions
root.mainloop()