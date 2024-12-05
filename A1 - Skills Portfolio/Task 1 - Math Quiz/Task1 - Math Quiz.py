# Import the customtkinter library for creating modern-looking Tkinter widgets
import customtkinter

# Import the tkinter library for creating GUI applications
import tkinter as tk

# Import the messagebox module from tkinter to display warning messages to the user
from tkinter import messagebox

# Import the PIL library for handling images, including GIFs, in the application
from PIL import Image, ImageTk, ImageSequence

# Import the os module to interact with the operating system, such as handling file paths
import os

# Import the random module to generate random numbers for quiz questions
import random

# Import the pygame library to handle audio playback in the application
import pygame

# Initialize Pygame mixer for audio playback
pygame.mixer.init()

# Set initial volume levels for background music and sound effects
initial_bgm_volume = 0.25  # 25% volume
initial_sfx_volume = 1.0   # 100% volume

def resource_path(relative_path):
    """Construct the absolute path to the resource file."""
    base_path = os.path.join("A1 - Skills Portfolio", "Task 1 - Math Quiz", "Assets")
    return os.path.join(base_path, relative_path)

def update_bgm_volume(volume):
    """Adjust the background music volume based on the slider's current value."""
    pygame.mixer.music.set_volume(float(volume) / 100)

def update_sfx_volume(volume):
    """Adjust the sound effect volume based on the slider's current value."""
    button_sound_effect.set_volume(float(volume) / 100)

def bgmusic():
    """Load and continuously play the background music in a loop."""
    music_path = resource_path("Gonna Fly Now (From the Film- Rocky).mp3")
    pygame.mixer.music.load(music_path)
    pygame.mixer.music.set_volume(initial_bgm_volume)
    pygame.mixer.music.play(loops=-1)

# Start playing the background music when the application launches
bgmusic()

# Load the button click sound effect and set its initial volume
button_sound_effect = pygame.mixer.Sound(resource_path("Click Sound Effect.mp3"))
button_sound_effect.set_volume(initial_sfx_volume)

def buttonsound():
    """Play the button click sound effect whenever a button is pressed."""
    button_sound_effect.play()

# Create and configure the main application window using customtkinter
root = customtkinter.CTk()
root.title("Quiz Game - Exercise 1")  # Set the window title for clarity
root.geometry("1440x900")             # Define the window size to match design specifications
root.resizable(False, False)          # Prevent the window from being resized to maintain layout integrity

def show_frame(frame):
    """Display the specified frame while hiding all others to manage different views."""
    for f in all_frames:
        f.pack_forget()                    # Hide every frame to ensure only the desired one is visible
    frame.pack(fill=tk.BOTH, expand=True)  # Show the chosen frame, allowing it to fill the window

# Initialize global variables to keep track of the quiz state
score = 0
question_count = 0
difficulty = 1
option = None
first_attempt = True
num1, num2, operation, correct_answer = None, None, None, None

# Dictionaries to manage CheckBox variables for quiz options and difficulty levels
option_vars = {}
difficulty_vars = {}

def option_selected(selected_value):
    """Ensure that only one quiz option is active at any given time."""
    for value, var in option_vars.items():
        if value != selected_value:
            var.set(0)  # Deselect other options to maintain single selection

def difficulty_selected(selected_value):
    """Ensure that only one difficulty level is active at any given time."""
    for value, var in difficulty_vars.items():
        if value != selected_value:
            var.set(0)  # Deselect other difficulty levels to maintain single selection

def start_quiz():
    """Initialize and start the quiz based on the user's selected options and difficulty."""
    global difficulty, option, score, question_count, first_attempt
    feedback_label.pack_forget()  # Hide any existing feedback to start fresh

    # Retrieve the selected quiz options and difficulty level from the CheckBoxes
    selected_options = [value for value, var in option_vars.items() if var.get() == 1]
    selected_difficulties = [value for value, var in difficulty_vars.items() if var.get() == 1]

    # Ensure the user has selected exactly one difficulty level before starting
    if len(selected_difficulties) != 1:
        messagebox.showwarning("Selection Required", "Please select exactly one difficulty before starting the quiz.")
        return

    option = selected_options[0] if selected_options else None
    difficulty = selected_difficulties[0]
    score = 0
    question_count = 0
    first_attempt = True

    generate_problem()  # Generate the first question for the quiz
    show_frame(quiz_frame)  # Transition to the quiz frame to begin

def random_int():
    """Generate a random integer within a range based on the current difficulty level."""
    if difficulty == 1:
        return random.randint(1, 9)
    elif difficulty == 2:
        return random.randint(10, 99)
    elif difficulty == 3:
        return random.randint(1000, 9999)
    elif difficulty == 4:
        return random.randint(10000, 99999)

def decide_operation():
    """Select a random mathematical operation based on the chosen quiz option."""
    if option in [2, 3]:
        return random.choice(['+', '-', '*', '/'])  # More operations depending on the options
    else:
        return random.choice(['+', '-'])            # Main operations for default options

def generate_problem():
    """Create a new math problem tailored to the current difficulty and selected operations."""
    global num1, num2, operation, correct_answer, first_attempt, question_count

    if question_count >= 10:
        show_results()              # End the quiz if the maximum number of questions is reached
        return

    first_attempt = True            # Reset attempt status for the new question
    operation = decide_operation()  # Choose the operation for the current problem
    num1 = random_int()             # Generate the first operand
    num2 = random_int()             # Generate the second operand

    # Adjust operands to ensure valid and challenging problems
    if operation == '/':
        while num2 == 0:
            num2 = random_int()     # Prevent division by zero
        quotient = random.randint(1, max_value() // num2)
        num1 = num2 * quotient      # Ensure the division results in a whole number
    elif operation == '*':
        max_multiplier = max_value() // num1 if num1 != 0 else 1
        num2 = random.randint(1, max_multiplier)  # Avoid excessively large results
    elif operation == '-':
        if num1 < num2:
            num1, num2 = num2, num1  # Ensure a non-negative result

    # Calculate the correct answer based on the chosen operation
    if operation == '+':
        correct_answer = num1 + num2
    elif operation == '-':
        correct_answer = num1 - num2
    elif operation == '*':
        correct_answer = num1 * num2
    elif operation == '/':
        correct_answer = num1 // num2

    question_count_label.configure(text=f"Question {question_count + 1} of 10")  # Update the question counter
    display_problem()  # Show the generated problem to the user

def max_value():
    """Return the maximum allowed value for operands based on the current difficulty."""
    if difficulty == 1:
        return 9
    elif difficulty == 2:
        return 99
    elif difficulty == 3:
        return 9999
    elif difficulty == 4:
        return 99999

def display_problem():
    """Display the current math problem to the user and prepare the answer entry."""
    question_text = f"{num1} {operation} {num2} = "
    question_label.configure(text=question_text)  # Update the question label with the new problem
    answer_entry.delete(0, tk.END)                # Clear any previous input from the answer entry
    answer_entry.focus()                          # Set focus to the answer entry for immediate input

def check_answer(event=None):
    """Validate the user's answer and update the score based on correctness."""
    global score, question_count, first_attempt
    user_answer = answer_entry.get().strip()
    answer_entry.delete(0, tk.END)        # Clear the answer entry after submission

    try:
        user_answer = int(user_answer)    # Attempt to convert the input to an integer
    except ValueError:
        feedback_label.configure(text="Please enter a valid integer.", text_color="white", fg_color="red")
        feedback_label.pack(pady=(5, 0))  # Show error feedback for invalid input
        return

    if user_answer == correct_answer:
        # Award more points if the correct answer is given on the first attempt
        score_increment = 10 if first_attempt else 5
        score += score_increment
        score_label.configure(text=f"Score: {score}")  # Update the score display
        feedback_label.configure(text="Correct!", text_color="white", fg_color="green")
        feedback_label.pack(pady=(5, 0))               # Provide positive feedback
        quiz_frame.after(1000, lambda: [feedback_label.pack_forget(), next_question()])  # Proceed to next question after a short delay
    else:
        if option == 1:
            # Immediate feedback without allowing a retry for option 1 which is "Easy Mode"
            feedback_label.configure(text="Incorrect! Try again.", text_color="white", fg_color="red")
            feedback_label.pack(pady=(5, 0))
        else:
            if first_attempt:
                # Allow a second attempt for options other than "Easy Mode"
                first_attempt = False
                feedback_label.configure(text="Incorrect! Try again.", text_color="white", fg_color="red")
                feedback_label.pack(pady=(5, 0))
            else:
                # Reveal the correct answer after the second incorrect attempt
                feedback_label.configure(
                    text=f"Incorrect! The correct answer was {correct_answer}.",
                    text_color="white",
                    fg_color="red"
                )
                feedback_label.pack(pady=(5, 0))
                quiz_frame.after(1000, lambda: [feedback_label.pack_forget(), next_question()])  # Proceed after showing the correct answer

def next_question():
    """Move to the next question or end the quiz if all questions have been answered."""
    global question_count, first_attempt
    question_count += 1   # Increment the question counter
    first_attempt = True  # Reset the attempt status for the new question

    if question_count >= 10:
        show_results()      # Show results if the quiz is complete
    else:
        generate_problem()  # Generate and display the next problem
        feedback_label.pack_forget()  # Hide any existing feedback before the next question

def show_results():
    """Display the final score and ranking to the user upon quiz completion."""
    ranking = calculate_ranking()                                             # Determine the user's ranking based on their score
    results_label.configure(text=f"Your Score: {score}\nRanking: {ranking}")  # Update the results display
    show_frame(results_frame)                                                 # Transition to the results frame to show the final outcome

def calculate_ranking():
    """Determine the user's ranking based on their final score."""
    if score >= 95:
        return "A+"
    elif score >= 85:
        return "A"
    elif score >= 75:
        return "B"
    elif score >= 65:
        return "C"
    elif score >= 50:
        return "D"
    else:
        return "F"

def reset_variables():
    """Reset all quiz-related variables and UI elements to their default states."""
    global score, question_count, difficulty, option, first_attempt
    global num1, num2, operation, correct_answer

    # Reset the quiz state variables
    score = 0
    question_count = 0
    difficulty = 1
    option = None
    first_attempt = True
    num1, num2, operation, correct_answer = None, None, None, None

    # Reset UI components to their initial states
    feedback_label.pack_forget()
    score_label.configure(text="Score: 0")
    question_count_label.configure(text="Question 1 of 10")
    answer_entry.delete(0, tk.END)

    # Deselect all option and difficulty CheckBoxes
    for var in option_vars.values():
        var.set(0)
    for var in difficulty_vars.values():
        var.set(0)

def update_frame():
    """Animate the background GIF by cycling through its frames at regular intervals."""
    global frame_index
    frame_index = (frame_index + 1) % frame_count
    titlebg.configure(image=frames[frame_index])  # Update the background image to the next frame
    root.after(14, update_frame)                  # Schedule the next frame update after 14 milliseconds

# Load background images and prepare frames for GIF animation
background_image = Image.open(resource_path("titlebg.gif"))
menu_bg_image = customtkinter.CTkImage(
    Image.open(resource_path("descbg.png")), size=(1440, 900)
)
quiz_bg_img = customtkinter.CTkImage(
    Image.open(resource_path("descbg.png")), size=(1440, 900)
)
options_bg_img = customtkinter.CTkImage(
    Image.open(resource_path("descbg.png")), size=(1440, 900)
)

frames = [ImageTk.PhotoImage(frame.convert("RGBA")) for frame in ImageSequence.Iterator(background_image)]
frame_count = len(frames)
frame_index = 0  # Initialize the frame index for animation

# Create frames for different sections of the application
title_frame = customtkinter.CTkFrame(root)
options_frame = customtkinter.CTkFrame(root)
menu_frame = customtkinter.CTkFrame(root)
diff_frame = customtkinter.CTkFrame(root)
quiz_frame = customtkinter.CTkFrame(root)
results_frame = customtkinter.CTkFrame(root)
audio_frame = customtkinter.CTkFrame(root)

# Collect all frames into a list for easy management
all_frames = [
    title_frame,
    options_frame,
    menu_frame,
    diff_frame,
    quiz_frame,
    results_frame,
    audio_frame
]

# Setting up the title screen background with the first frame of my animated background.
titlebg = customtkinter.CTkLabel(
    title_frame, text="", image=frames[0], width=1440, height=900
)
titlebg.place(x=0, y=0)

# Creating the 'Audio' button on the title screen to navigate to the audio settings.
# I wanted it to be prominent, so I used a large font size.
title_audio = customtkinter.CTkButton(
    title_frame,
    text="Audio",
    font=("League Gothic", 72),
    width=400,
    height=50,
    command=lambda: [show_frame(audio_frame), buttonsound()],
    cursor="hand2",
    border_width=5,
    border_color='black'
)
title_audio.pack(side=tk.BOTTOM, pady=(0, 30))

# Adding the 'Options' button just above the 'PLAY?' button for easy access to game settings.
title_options = customtkinter.CTkButton(
    title_frame,
    text="Options",
    font=("League Gothic", 72),
    width=400,
    height=50,
    command=lambda: [show_frame(options_frame), buttonsound()],
    cursor="hand2",
    border_width=5,
    border_color='black'
)
title_options.pack(side=tk.BOTTOM, pady=(0, 10))

# Creating the 'PLAY?' button to start the game.
# I chose a green color to make it stand out and indicate action.
title_start = customtkinter.CTkButton(
    title_frame,
    text="PLAY?",
    font=("League Gothic", 72),
    width=400,
    height=50,
    fg_color='green',
    hover_color='darkgreen',
    command=lambda: [show_frame(menu_frame), buttonsound()],
    cursor="hand2",
    border_width=5,
    border_color='black'
)
title_start.pack(side=tk.BOTTOM, pady=(0, 10))

# Setting up the audio settings screen with the same background for consistency.
audiobg = customtkinter.CTkLabel(
    audio_frame,
    text="",
    image=options_bg_img,
    width=1440,
    height=900
)
audiobg.place(x=0, y=0)

# Adding a header label 'Audio:' to indicate the current settings screen.
audio_header = customtkinter.CTkLabel(
    audio_frame,
    text="Audio:",
    fg_color="#5a825d",
    font=("Montserrat", 72, 'bold')
)
audio_header.pack(side=tk.TOP, pady=(150, 5))

# Adding a label and slider for the background music volume.
# Starting at 25% volume to keep the music subtle initially.
bgm_volume_label = customtkinter.CTkLabel(
    audio_frame,
    text="Background Music Volume:",
    font=('Montserrat', 32, 'bold'),
    fg_color="#5a825d"
)
bgm_volume_label.pack(pady=(20, 10))

bgm_volume_slider = customtkinter.CTkSlider(
    audio_frame,
    from_=0,
    to=100,
    command=update_bgm_volume,
    width=400,
    height=30,
    bg_color="#5a825d",
    fg_color="white",
    button_color="darkgreen"
)
bgm_volume_slider.set(25)
bgm_volume_slider.pack()

# Adding a label and slider for the sound effects volume.
# Set to 100% so the button clicks are noticeable.
sfx_volume_label = customtkinter.CTkLabel(
    audio_frame,
    text="Sound Effect Volume:",
    font=('Montserrat', 32, 'bold'),
    fg_color="#5a825d"
)
sfx_volume_label.pack(pady=(50, 10))

sfx_volume_slider = customtkinter.CTkSlider(
    audio_frame,
    from_=0,
    to=100,
    command=update_sfx_volume,
    width=400,
    height=30,
    bg_color="#5a825d",
    fg_color="white",
    button_color="darkgreen"
)
sfx_volume_slider.set(100)
sfx_volume_slider.pack()

# Adding a 'BACK' button at the bottom-left to navigate back to the title screen.
# Chose red to make it easily identifiable as a navigation button.
audio_back_button = customtkinter.CTkButton(
    audio_frame,
    text="BACK",
    font=('League Gothic', 48),
    width=400,
    height=100,
    fg_color='red',
    hover_color='maroon',
    cursor="hand2",
    command=lambda: [show_frame(title_frame), buttonsound()],
    border_width=5,
    border_color='black'
)
audio_back_button.place(relx=0.0, rely=1.0, anchor=tk.SW, x=50, y=-50)

# Setting up the options screen background.
optionsbg = customtkinter.CTkLabel(
    options_frame, text="", image=options_bg_img, width=1440, height=900
)
optionsbg.place(x=0, y=0)

# Adding the 'Options:' header to clearly indicate the settings screen.
options_header = customtkinter.CTkLabel(
    options_frame,
    text="Options:",
    fg_color="#5a825d",
    font=("Montserrat", 72, 'bold')
)
options_header.pack(side=tk.TOP, pady=(150, 5))

# Defining the quiz options for the player to choose from.
# Wanted to provide varying levels of challenge.
quiz_options = [
    ("IMPOSSIBLE Mode - Adds Multiplication and Division AND 5-digit questions.", 3),
    ("Multiplication and Division - Adds Multiplication and Division.", 2),
    ("Easy Mode - You have INFINITE Retries.", 1),
]

# Creating checkboxes for each quiz option.
# Ensuring only one option can be selected at a time.
for text, value in quiz_options:
    var = tk.IntVar(value=0)
    option_vars[value] = var

    cb = customtkinter.CTkCheckBox(
        options_frame,
        text=text,
        variable=var,
        onvalue=1,
        offvalue=0,
        command=lambda v=value: option_selected(v),
        font=('Poppins', 24, 'bold'),
        bg_color="#5a825d",
        cursor="hand2",
    )
    cb.pack(anchor=tk.CENTER, pady=30)

# Adding a 'BACK' button to return to the title screen from the options menu.
options_back = customtkinter.CTkButton(
    options_frame,
    text="BACK",
    font=('League Gothic', 48),
    width=400,
    height=100,
    fg_color='red',
    hover_color='maroon',
    cursor="hand2",
    command=lambda: [show_frame(title_frame), buttonsound()],
    border_width=5,
    border_color='black'
)
options_back.place(relx=0.0, rely=1.0, anchor=tk.SW, x=50, y=-50)

def update_difficulty_options(*args):
    """Dynamic update of difficulty options based on the selected quiz mode.
    
    If 'IMPOSSIBLE Mode' is selected, add 'Impossible (5-digit)' difficulty to the choices.
    """
    # Clearing existing difficulty options to refresh the list.
    for widget in difficulty_frame.winfo_children():
        widget.destroy()

    # Base difficulty levels available to the player.
    available_difficulties = [
        ("Easy (1-digit)", 1),
        ("Intermediate (2-digit)", 2),
        ("Hard (4-digit)", 3),
    ]

    # If 'IMPOSSIBLE Mode' is active, include the 'Impossible' difficulty.
    if 3 in [value for value, var in option_vars.items() if var.get() == 1]:
        available_difficulties.append(("Impossible (5-digit)", 4))

    # Resetting the difficulty variables.
    difficulty_vars.clear()

    # Creating checkboxes for each difficulty level.
    for text, value in available_difficulties:
        var = tk.IntVar(value=0)
        difficulty_vars[value] = var

        cb = customtkinter.CTkCheckBox(
            difficulty_frame,
            text=text,
            variable=var,
            onvalue=1,
            offvalue=0,
            command=lambda v=value: difficulty_selected(v),
            font=('Poppins', 32, 'bold'),
            bg_color="#5a825d",
            cursor="hand2"
        )
        cb.configure(width=400)
        cb.pack(anchor=tk.CENTER, pady=(30, 0), fill='both', expand=True)

# Setting up the menu screen background.
menubg = customtkinter.CTkLabel(
    menu_frame, text="", image=menu_bg_image, width=1440, height=900
)
menubg.place(x=0, y=0)

# Adding a header 'How to Play:' to guide new players.
menu_header = customtkinter.CTkLabel(
    menu_frame,
    text="How to Play:",
    fg_color="#5a825d",
    font=("Montserrat", 72, 'bold')
)
menu_header.pack(side=tk.TOP, pady=(150, 5))

# Providing game instructions.
# Wanted to make sure players understand the scoring and difficulty options.
menu_text = customtkinter.CTkLabel(
    menu_frame,
    text=(
        "This Quiz has 10 questions to solve. Each question is worth 10 points. "
        "If you get an answer wrong, you get another attempt worth 5 points. "
        "You can choose between 3 difficulties:\n\n"
        "Easy (1-digit questions)\n\n"
        "Intermediate (2-digit questions)\n\n"
        "Hard (4-digit questions)"
    ),
    fg_color="#5a825d",
    font=('Poppins', 24),
    wraplength=1200,
)
menu_text.pack()

# Adding a 'BACK' button to return to the title screen.
menu_back = customtkinter.CTkButton(
    menu_frame,
    text="BACK",
    font=('League Gothic', 48),
    width=400,
    height=100,
    fg_color='red',
    hover_color='maroon',
    cursor="hand2",
    command=lambda: [show_frame(title_frame), buttonsound()],
    border_width=5,
    border_color='black'
)
menu_back.place(relx=0.0, rely=1.0, anchor=tk.SW, x=50, y=-50)

# Adding a 'NEXT' button to proceed to the difficulty selection screen.
menu_next = customtkinter.CTkButton(
    menu_frame,
    text="NEXT",
    font=('League Gothic', 48),
    width=400,
    height=100,
    cursor="hand2",
    command=lambda: [update_difficulty_options(), show_frame(diff_frame), buttonsound()],
    border_width=5,
    border_color='black'
)
menu_next.place(relx=1.0, rely=1.0, anchor=tk.SE, x=-50, y=-50)

# Setting up the background for the difficulty selection screen with the same image as the menu for consistency.
diffbg = customtkinter.CTkLabel(
    diff_frame, text="", image=menu_bg_image, width=1440, height=900
)
diffbg.place(x=0, y=0)

# Adding a header to prompt the user to choose a difficulty level.
diff_header = customtkinter.CTkLabel(
    diff_frame,
    text="Choose a Difficulty:",
    fg_color="#5a825d",
    font=("Montserrat", 72, 'bold')
)
diff_header.pack(side=tk.TOP, pady=(150, 50))

# Creating a frame to neatly hold the difficulty CheckBoxes.
difficulty_frame = customtkinter.CTkFrame(diff_frame, fg_color="#5a825d", bg_color="#5a825d")
difficulty_frame.pack()

# Initialize the difficulty options based on the user's selections.
update_difficulty_options()

# Adding a 'BACK' button to return to the menu screen if the user changes their mind.
diff_back = customtkinter.CTkButton(
    diff_frame,
    text="BACK",
    font=('League Gothic', 48),
    width=400,
    height=100,
    fg_color='red',
    hover_color='maroon',
    cursor="hand2",
    command=lambda: [show_frame(menu_frame), buttonsound()],
    border_width=5,
    border_color='black'
)
diff_back.place(relx=0.0, rely=1.0, anchor=tk.SW, x=50, y=-50)

# Adding a 'START QUIZ' button to proceed once the difficulty is selected.
diff_next = customtkinter.CTkButton(
    diff_frame,
    text="START QUIZ",
    font=('League Gothic', 48),
    width=400,
    height=100,
    fg_color='green',
    hover_color='darkgreen',
    cursor="hand2",
    command=lambda: [start_quiz(), buttonsound()],
    border_width=5,
    border_color='black'
)
diff_next.place(relx=1.0, rely=1.0, anchor=tk.SE, x=-50, y=-50)

# Setting up the quiz screen with the appropriate background image.
quizbg = customtkinter.CTkLabel(
    quiz_frame, text="", image=quiz_bg_img, width=1440, height=900
)
quizbg.place(x=0, y=0)

# Displaying the player's current score at the top of the quiz screen.
score_label = customtkinter.CTkLabel(
    quiz_frame,
    text="Score: 0",
    fg_color="#5a825d",
    font=('Montserrat', 64, 'bold')
)
score_label.pack(pady=(130, 0))

# Showing the question count so the player knows their progress.
question_count_label = customtkinter.CTkLabel(
    quiz_frame,
    text="Question 1 of 10",
    fg_color="#5a825d",
    font=('Poppins', 48, 'bold')
)
question_count_label.pack(pady=5)

# Label to display the current math question.
question_label = customtkinter.CTkLabel(
    quiz_frame,
    fg_color="#5a825d",
    font=('Poppins', 72, 'bold')
)
question_label.pack()

# Entry field for the player to input their answer.
answer_entry = customtkinter.CTkEntry(
    quiz_frame,
    width=500,
    height=100,
    font=('Montserrat', 36)
)
answer_entry.pack(pady=40)
answer_entry.bind("<Return>", check_answer)  # Allowing 'Enter' key to submit the answer.

# Feedback label to provide immediate response after an answer is submitted.
feedback_label = customtkinter.CTkLabel(
    quiz_frame,
    width=500,
    height=100,
    font=('Poppins', 19, 'bold')
)
feedback_label.pack(pady=50)
feedback_label.pack_forget()  # Hide it initially until needed.

# Adding a 'SUBMIT' button for answer submission.
submit_button = customtkinter.CTkButton(
    quiz_frame,
    text="SUBMIT",
    fg_color='green',
    hover_color='darkgreen',
    font=('League Gothic', 48),
    width=400,
    height=100,
    cursor="hand2",
    command=lambda: [check_answer(), buttonsound()],
    border_width=5,
    border_color='black'
)
submit_button.place(relx=1.0, rely=1.0, anchor=tk.SE, x=-50, y=-50)

# Adding an 'EXIT' button to allow the player to leave the quiz at any time.
quiz_exit_button = customtkinter.CTkButton(
    quiz_frame,
    text="EXIT",
    fg_color='red',
    hover_color='maroon',
    font=('League Gothic', 48),
    width=400,
    height=100,
    cursor="hand2",
    command=lambda: [reset_variables(), show_frame(diff_frame), buttonsound()],
    border_width=5,
    border_color='black'
)
quiz_exit_button.place(relx=0.0, rely=1.0, anchor=tk.SW, x=50, y=-50)

# Setting up the results screen background using the same image for consistency.
resultsbg = customtkinter.CTkLabel(
    results_frame, text="", image=quiz_bg_img, width=1440, height=900
)
resultsbg.place(x=0, y=0)

# Label to display the final score and ranking after the quiz ends.
results_label = customtkinter.CTkLabel(
    results_frame,
    text="Your Score: 0\nRanking: F",
    font=('Montserrat', 72, 'bold'),
    fg_color='green'
)
results_label.pack(pady=(150, 50))

# Adding a 'PLAY AGAIN?' button for the player to retry the quiz.
play_again_button = customtkinter.CTkButton(
    results_frame,
    text="PLAY AGAIN?",
    font=('League Gothic', 64),
    width=500,
    height=150,
    fg_color='green',
    hover_color='darkgreen',
    cursor="hand2",
    command=lambda: [reset_variables(), show_frame(diff_frame), buttonsound()],
    border_width=5,
    border_color='black'
)
play_again_button.place(relx=0.0, rely=1.0, anchor=tk.SW, x=50, y=-50)

# Adding an 'EXIT' button to return to the main menu from the results screen.
exit_button = customtkinter.CTkButton(
    results_frame,
    text="EXIT",
    font=('League Gothic', 64),
    width=500,
    height=150,
    fg_color='red',
    hover_color='maroon',
    cursor="hand2",
    command=lambda: [reset_variables(), show_frame(menu_frame), buttonsound()],
    border_width=5,
    border_color='black'
)
exit_button.place(relx=1.0, rely=1.0, anchor=tk.SE, x=-50, y=-50)

# Starting the background animation for the title screen.
update_frame()

# Displaying the title screen as the initial frame when the application launches.
show_frame(title_frame)

# Starting the main application loop.
root.mainloop()