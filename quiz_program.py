import tkinter as tk
from tkinter import ttk, messagebox
from ttkbootstrap import Style
from PIL import Image, ImageTk  # Import Image and ImageTk from PIL library
from quiz_data import quiz_data, quiz_data2  # Import quiz_data for both rounds
import pygame  # Import pygame for playing sound

# Initialize pygame
pygame.mixer.init()

# Initialize timer and timer_running flag
timer = 25
timer_running = False

# Function to display the current question and choices
def show_question():
    global timer, timer_running
    # Get the current question from the appropriate quiz_data list
    if current_round == 1:
        question = quiz_data[current_question]
    else:
        question = quiz_data2[current_question]
    
    qs_label.config(text=question["question"])

    # Display the choices on the buttons
    choices = question["choices"]
    for i in range(4):
        choice_btns[i].config(text=choices[i], state="normal") # Reset button state

    # Clear the feedback label and disable the next button
    feedback_label.config(text="")
    next_btn.config(state="disabled")
    
    # Reset and start the timer
    timer = 25
    timer_running = True
    update_timer()
    play_tick_sound()

# Function to update the timer label
def update_timer():
    global timer, timer_running
    if timer_running:
        if timer > 0:
            timer_label.config(text="Time left: {}s".format(timer))
            timer -= 1
            timer_label.after(1000, update_timer)
        else:
            timer_running = False
            check_answer(-1)

# Function to play the ticking sound effect
def play_tick_sound():
    pygame.mixer.music.load("tick.mp3")
    pygame.mixer.music.play(-1)  # Play in an infinite loop

# Function to stop the ticking sound effect
def stop_tick_sound():
    pygame.mixer.music.stop()

# Function to check the selected answer and provide feedback
def check_answer(choice):
    global score_round1, score_round2, timer_running
    # Stop the timer
    timer_running = False

    # Get the current question from the appropriate quiz_data list
    if current_round == 1:
        question = quiz_data[current_question]
    else:
        question = quiz_data2[current_question]
    
    # Check if the choice is valid (not from timeout)
    if choice >= 0:
        selected_choice = choice_btns[choice].cget("text")

        # Check if the selected choice matches the correct answer
        if selected_choice == question["answer"]:
            # Update the respective score and display it
            if current_round == 1:
                score_round1 += 1
                score_label.config(text="Score Round 1: {}/{}".format(score_round1, len(quiz_data)))
            else:
                score_round2 += 1
                score_label.config(text="Score Round 2: {}/{}".format(score_round2, len(quiz_data2)))
            feedback_label.config(text="Correct!", foreground="green")
        else:
            feedback_label.config(text="Incorrect!", foreground="blue")
    
    # Disable all choice buttons and enable the next button
    for button in choice_btns:
        button.config(state="disabled")
    next_btn.config(state="normal")
    stop_tick_sound()

# Function to move to the next question or next round
def next_question():
    global current_question, current_round

    current_question += 1

    if current_round == 1:
        if current_question < len(quiz_data):
            # If there are more questions in the first round, show the next question
            show_question()
        else:
            # If the first round is completed, check if it's eligible for the second round
            if score_round1 / len(quiz_data) > 0.6:
                # Create a button to proceed to the second round
                messagebox.showinfo("Round 1 Completed", "Congratulations! You have passed Round 1.")
                current_round = 2
                current_question = 0
                show_question()
            else:
                messagebox.showinfo("Round 1 Completed", "Unfortunately, you did not qualify for Round 2.")
                root.destroy()
    else:
        if current_question < len(quiz_data2):
            # If there are more questions in the second round, show the next question
            show_question()
        else:
            # If all questions in the second round have been answered, end the quiz
            messagebox.showinfo("Quiz Completed",
                                "Quiz Completed! Final score Round 1: {}/{} | Round 2: {}/{}".format(score_round1, len(quiz_data), score_round2, len(quiz_data2)))
            root.destroy()

# Create the main window
root = tk.Tk()
root.title("Quiz App")
root.geometry("850x600")
style = Style(theme="flatly")

# Configure the font size for the question and choice buttons
style.configure("TLabel", font=("Helvetica", 20))
style.configure("TButton", font=("Helvetica", 16))

# Load the background image (change the filename to your JPEG image)
background_image = Image.open("background_image.jpeg")
background_photo = ImageTk.PhotoImage(background_image)

# Create a label to display the background image
background_label = tk.Label(root, image=background_photo)
background_label.place(relwidth=1, relheight=1)  # Fill the entire window with the background image

# Create the question label
qs_label = ttk.Label(
    root,
    anchor="center",
    wraplength=500,
    padding=10
)
qs_label.pack(pady=10)

# Create the choice buttons
choice_btns = []
for i in range(4):
    button = ttk.Button(
        root,
        command=lambda i=i: check_answer(i)
    )
    button.pack(pady=5)
    choice_btns.append(button)

# Create the feedback label
feedback_label = ttk.Label(
    root,
    anchor="center",
    padding=10
)
feedback_label.pack(pady=10)

# Create the timer label with red background color
timer_label = ttk.Label(
    root,
    text="Time left: 25s",
    anchor="center",
    padding=10,
    background="red",  # Set background color to red
    foreground="white",  # Set foreground (text) color to white
)
timer_label.place(relx=0.8, rely=0.05)  # Position the timer label in the top right corner

# Initialize the scores and current round
score_round1 = 0
score_round2 = 0
current_round = 1

# Create the score label
score_label = ttk.Label(
    root,
    text="Score Round 1: 0/{}".format(len(quiz_data)),
    anchor="center",
    padding=10
)
score_label.pack(pady=10)

# Create the next button
next_btn = ttk.Button(
    root,
    text="Next",
    command=next_question,
    state="disabled"
)
next_btn.pack(pady=10)

# Initialize the current question index
current_question = 0

# Show the first question
show_question()

# Start the main event loop
root.mainloop()
