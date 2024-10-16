import tkinter as tk
import random
import time

ROUNDS = 20
class VisualERP:
    def __init__(self, root):
        self.root = root
        self.root.title("Visual Test")
        self.colors = ["red","orange","yellow","green","blue","purple","black"]

        # Initialize score and game state
        self.score = 0
        self.display_step = 0
        self.countdown = 5
        self.x = 0
        self.y = 0
        self.accept_input = False

        # Set up the labels
        self.message_label = tk.Label(root, text="Welcome", font=("Arial", 20))
        self.message_label.pack(pady=20)

        self.score_label = tk.Label(root, text=f"Score: {self.score}", font=("Arial", 16))
        self.score_label.pack(pady=10)

        # Set up key event listener
        self.root.bind("<KeyPress-y>", lambda event: self.process_input(True))
        self.root.bind("<KeyPress-n>", lambda event: self.process_input(False))

        # Start the display cycle
        self.root.after(2000, self.update_display)  # 2-second delay before the first update
    def update_display(self):
        if self.display_step <= 4:
            self.message_label.config(text=self.countdown)
            self.countdown -= 1
            self.display_step += 1
            # Schedule the next update after 1 second
            self.root.after(1000, self.update_display)
        elif self.display_step > 4 and self.display_step <= 5:
            tf = random.randint(1,100)
            if(20 > tf):
                self.x = random.randint(0,6)
                self.y = random.randint(0,6)
                while (self.y == self.x):
                    self.y = random.randint(0,6)
            else:
                self.x = random.randint(0,6)
                self.y = self.x
            self.display_step += 1
            self.message_label.config(fg=self.colors[self.y], text=self.colors[self.x])
            self.root.after(3000, self.update_display)
        elif self.display_step == 6:
           #user types yes or no and if x == y then score += 1
            self.message_label.config(text=f"were they the same? (y/n)", fg="black")
            self.accept_input = True
            #wait for user input


    def process_input(self, user_said_yes):
        """Processes the user's input and updates the score."""
        if not self.accept_input:
            return
        self.accept_input = False
        if (user_said_yes and self.x == self.y) or (not user_said_yes and self.x != self.y):
            self.score += 1  # Correct answer

        # Update the score label
        self.score_label.config(text=f"Score: {self.score}")
        # Reset the game for the next round
        self.countdown = 5
        self.display_step = 0
        self.update_display()  # Start next round

# Main application loop
if __name__ == "__main__":
    root = tk.Tk()
    app = VisualERP(root)
    root.mainloop()
