import tkinter as tk
import random

ROUNDS = 20

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
        self.accept_input = False  
        self.accept_restart = False
        self.accept_start = False
        self.round_number = 0
        self.color_delay = 500  
        self.response_delay = 1000  
        self.question_id = None  

        # Set up the Text widget for message display with proper formatting
        self.message_label = tk.Text(
            root, 
            height=2, 
            width=20, 
            font=("Arial", 100), 
            wrap="word", 
            bg="white", 
            relief="flat", 
            bd=0
        )
        self.message_label.tag_configure("center", justify="center")
        self.message_label.place(relx=0.5, rely=0.4, anchor="center")

        self.score_label = tk.Label(root, text=f"Score: {self.score}", font=("Arial", 16))
        self.score_label.place(relx=0.5, rely=0.9, anchor="center")

        # Entry field for setting delay time
        self.delay_entry = tk.Entry(root, font=("Arial", 16))
        self.delay_entry.place(relx=0.4, rely=0.8, anchor="center")
        self.delay_entry.insert(0, "1000")
        self.delay_label = tk.Label(root, text="Time word is shown (ms):", font=("Arial", 16))
        self.delay_label.place(relx=0.4, rely=0.75, anchor="center")

        self.response_entry = tk.Entry(root, font=("Arial", 16))
        self.response_entry.place(relx=0.6, rely=0.8, anchor="center")
        self.response_entry.insert(0, "1000")
        self.response_label = tk.Label(root, text="Time to respond (ms):", font=("Arial", 16))
        self.response_label.place(relx=0.6, rely=0.75, anchor="center")

        self.delay_button = tk.Button(root, text="Update", font=("Arial", 16), command=self.update_delay)
        self.delay_button.place(relx=0.5, rely=0.85, anchor="center")

        # Key event listeners
        self.root.bind("<KeyPress-y>", lambda event: self.process_input(True))
        self.root.bind("<KeyPress-n>", lambda event: self.process_input(False))
        self.root.bind("<KeyPress-r>", lambda event: self.restart_game(True))
        self.root.bind("<KeyPress-space>", lambda event: self.start_game(True))

        self.root.after(0, self.start_screen)

    def start_screen(self):
        """Display start screen message."""
        self.message_label.delete("1.0", tk.END)
        self.message_label.insert(tk.END, "Press Spacebar\n to Begin", "center")
        self.accept_start = True

    def count(self):
        """Updates the countdown label and decrements the counter."""
        if self.countdown > 0:
            self.message_label.delete("1.0", tk.END)
            self.message_label.insert(tk.END, str(self.countdown), "center")
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

            # Insert colored word
            self.message_label.delete("1.0", tk.END)
            # place three words and one of them is randomly colored
            random_color2 = random.randint(0, 6)  # Random color for color3
            random_color3 = random.randint(0, 6)  # Random color for color3
            random_int = random.randint(1, 3)  # Random placement selection

            # Use black for color1 and color2, random color for color3
            black_color = "black"

            if random_int == 1:
                self.message_label.insert(tk.END, self.colors[self.y] + " ", ("color3", "center"))
                self.message_label.tag_configure("color3", foreground=self.colors[self.x])  # Random color for color3

                self.message_label.insert(tk.END, self.colors[random_color2] + " ", ("color1", "center"))
                self.message_label.tag_configure("color1", foreground=black_color)  # Black text for color1

                self.message_label.insert(tk.END, self.colors[random_color3] + " ", ("color2", "center"))
                self.message_label.tag_configure("color2", foreground=black_color)  # Black text for color2

            elif random_int == 2:
                self.message_label.insert(tk.END, self.colors[random_color2] + " ", ("color1", "center"))
                self.message_label.tag_configure("color1", foreground=black_color)  # Black text for color1

                self.message_label.insert(tk.END, self.colors[self.y] + " ", ("color3", "center"))
                self.message_label.tag_configure("color3", foreground=self.colors[self.x])  # Random color for color3

                self.message_label.insert(tk.END, self.colors[random_color3] + " ", ("color2", "center"))
                self.message_label.tag_configure("color2", foreground=black_color)  # Black text for color2

            else:
                self.message_label.insert(tk.END, self.colors[random_color2] + " ", ("color1", "center"))
                self.message_label.tag_configure("color1", foreground=black_color)  # Black text for color1

                self.message_label.insert(tk.END, self.colors[random_color3] + " ", ("color2", "center"))
                self.message_label.tag_configure("color2", foreground=black_color)  # Black text for color2

                self.message_label.insert(tk.END, self.colors[self.y] + " ", ("color3", "center"))
                self.message_label.tag_configure("color3", foreground=self.colors[self.x])  # Random color for color3
            #self.message_label.insert(tk.END, self.colors[self.y] + " ", ("color1", "center"))
            #self.message_label.tag_configure("color1", foreground=self.colors[self.x])

            self.root.after(self.color_delay, self.show_question)
        else:
            self.show_final()

    def show_question(self):
        """Display the question and wait for user input."""
        self.message_label.delete("1.0", tk.END)
        self.message_label.insert(tk.END, "(y) or (n)", "center")
        self.accept_input = True

        self.question_id = self.root.after(self.response_delay, self.show_blank)

    def process_input(self, user_said_yes):
        """Process user input and cancel timeout if needed."""
        if not self.accept_input:
            return

        self.accept_input = False

        if self.question_id:
            self.root.after_cancel(self.question_id)

        if (user_said_yes and self.x == self.y) or (not user_said_yes and self.x != self.y):
            self.score += 1

        self.score_label.config(text=f"Score: {self.score}")

        self.show_blank()

    def show_blank(self):
        """Display a blank screen."""
        self.accept_input = False
        self.round_number += 1
        self.message_label.delete("1.0", tk.END)
        self.root.after(random.randint(1000, 2000), self.start_round)

    def show_final(self):
        """Display the final score."""
        self.message_label.delete("1.0", tk.END)
        self.message_label.insert(tk.END, f"Game Over! Final Score: {self.score}\nPress R to Return to Main Menu\nPress Space to Replay", "center")
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
                self.message_label.delete("1.0", tk.END)
                self.message_label.insert(tk.END, "Please enter a positive number", "center")
        except ValueError:
            self.message_label.delete("1.0", tk.END)
            self.message_label.insert(tk.END, "Please enter a valid number", "center")
        self.root.focus_set()

if __name__ == "__main__":
    root = tk.Tk()
    app = VisualERP(root)
    root.mainloop()
