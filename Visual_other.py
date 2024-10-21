import tkinter as tk
import random

ROUNDS = 3

class VisualERP:
    def __init__(self, root):
        self.root = root
        self.root.title("Visual Test")
        self.colors = ["red", "orange", "yellow", "green", "blue", "purple", "black"]

        # Get screen dimensions
        screen_width = self.root.winfo_screenwidth()
        screen_height = self.root.winfo_screenheight()

        # Set window dimensions
        self.root.geometry(f"{screen_width}x{screen_height}")

        # Initialize score and game state
        self.score = 0
        self.display_step = 0
        self.countdown = 5
        self.x = 0
        self.y = 0
        self.accept_input = False  # Input allowed only when (y/n) is shown
        self.accept_restart = False
        self.accept_start = False
        self.round_number = 0
        self.color_delay = 500 #Change this to change the amount of time the color is shown
        self.response_delay = 1000 #Change this to change the amount of time the question is shown
        self.question_id = None  # Initialize question_id

        # Set up the labels
        self.message_label = tk.Label(root, text="Welcome", font=("Arial", 200))
        self.message_label.place(relx=0.5, rely=0.4, anchor="center")

        self.score_label = tk.Label(root, text=f"Score: {self.score}", font=("Arial", 16))
        self.score_label.place(relx=0.5, rely=0.9, anchor="center")

        # Entry field for setting delay time
        self.delay_entry = tk.Entry(root, font=("Arial", 16))
        self.delay_entry.place(relx=0.4, rely=0.8, anchor="center")
        self.delay_entry.insert(0, "1000")
        self.delay_label = tk.Label(root, text="Time word is shown (ms):", font=("Arial", 16))
        self.delay_label.place(relx=0.4, rely=0.75, anchor="center")

        # Entry for response delay
        self.response_entry = tk.Entry(root, font=("Arial", 16))
        self.response_entry.place(relx=0.6, rely=0.8, anchor="center")
        self.response_entry.insert(0, "1000")
        self.response_label = tk.Label(root, text="Time to respond (ms):", font=("Arial", 16))
        self.response_label.place(relx=0.6, rely=0.75, anchor="center")

        # Button to update delay time
        self.delay_button = tk.Button(root, text="Update", font=("Arial", 16), command=self.update_delay)
        self.delay_button.place(relx=0.5, rely=0.85, anchor="center")

        # Key event listeners
        self.root.bind("<KeyPress-y>", lambda event: self.process_input(True))
        self.root.bind("<KeyPress-n>", lambda event: self.process_input(False))
        self.root.bind("<KeyPress-r>", lambda event: self.restart_game(True))
        self.root.bind("<KeyPress-space>", lambda event: self.start_game(True))

        # Start display cycle
        self.root.after(000, self.start_screen)

    def start_screen(self):
        """Display start screen message."""
        #set the font size to 100
        self.message_label.config(font=("Arial", 100))
        self.message_label.config(text="Press Spacebar\n to Begin", fg="black")
        self.accept_start = True

    def count(self):
        self.message_label.config(font=("Arial", 200))
        """Updates the countdown label and decrements the counter."""
        if self.countdown > 0:
            self.message_label.config(text=self.countdown)
            self.countdown -= 1
            self.root.after(1000, self.count)
        else:
            self.start_round()

    def start_round(self):
        """Start a new round."""
        if self.round_number < ROUNDS:
            tf = random.randint(1, 100)
            if tf < 20:
                self.x = random.randint(0, 6)
                self.y = random.randint(0, 6)
                while self.y == self.x:
                    self.y = random.randint(0, 6)
            else:
                self.x = random.randint(0, 6)
                self.y = self.x

            self.display_step += 1
            #three words place the colored word ramdomly
            random_int = random.randint(1, 3)
            #color1 color2 color3
            self.message_label.config(fg=self.colors[self.x], text=self.colors[self.y])

            # Schedule the question prompt
            self.root.after(self.color_delay, self.show_question)

        else:
            self.show_final()

    def show_question(self):
        """Display the question and wait for user input."""
        #clear screen first
        self.message_label.config(text="")
        self.message_label.config(text="(y) or (n)", fg="black")
        self.accept_input = True  # Enable input only when the question is shown

        # Schedule transition to blank screen if no input is given
        self.question_id = self.root.after(self.response_delay, self.show_blank)

    def process_input(self, user_said_yes):
        """Process user input and cancel timeout if needed."""
        if not self.accept_input:
            return  # Ignore input if not allowed

        self.accept_input = False  # Disable input after one response

        # Cancel the scheduled transition to blank screen
        if self.question_id:
            self.root.after_cancel(self.question_id)

        # Check if the answer is correct
        if (user_said_yes and self.x == self.y) or (not user_said_yes and self.x != self.y):
            self.score += 1

        # Update the score label
        self.score_label.config(text=f"Score: {self.score}")

        # Proceed to the next round
        self.show_blank()

    def show_blank(self):
        """Display a blank screen."""
        self.accept_input = False  # Disable input during blank screen
        self.round_number += 1
        self.message_label.config(text="")
        random_int = random.randint(1000, 2000)
        self.root.after(random_int, self.start_round)

    def show_final(self):
        """Display the final score."""
        self.message_label.config(
            font=("Arial", 36),
            text=f"Game Over! Final Score: {self.score}\nPress R to Return to Main Menu\n Press Space to Replay",
            fg="black"
        )
        self.accept_restart = True
        self.accept_start = True

    def restart_game(self, restart):
        """Restart the game."""
        if not self.accept_restart:
            return
        self.accept_restart = False
        self.score = 0
        self.round_number = 0
        self.countdown = 5
        self.score_label.config(text=f"Score: {self.score}")
        self.start_screen()
    def start_game(self, start):
        """Start the game."""
        if not self.accept_start:
            return
        self.accept_start = False
        self.round_number = 0
        self.countdown = 5
        self.score = 0
        self.score_label.config(text=f"Score: {self.score}")
        self.count()

    def update_delay(self):
        """Update delay values."""
        try:
            color_delay = int(self.delay_entry.get())
            response_delay = int(self.response_entry.get())
            if color_delay > 0 and response_delay > 0:
                self.color_delay = color_delay
                self.response_delay = response_delay
            else:
                self.message_label.config(text="Please enter a positive number")
        except ValueError:
            self.message_label.config(text="Please enter a valid number")
        self.root.focus_set()

# Main application loop
if __name__ == "__main__":
    root = tk.Tk()
    app = VisualERP(root)
    root.mainloop()
