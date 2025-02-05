import tkinter as tk
import random
import time
import csv
import os

import socket
from pylsl import StreamInfo, StreamOutlet, StreamInlet, resolve_stream, local_clock
import threading

"""
 
7000 + block number: Marks the start of a new block.
8000 + block number: Marks the end of the current block.

6000 + round number: Marks the start of a new round within a block.

3001: Stimulus is a match (text and color are the same).
3002: Stimulus is a mismatch (text and color are different).

4001: User correctly identified a match.
4002: User correctly identified a mismatch.

5001: User incorrectly identified a match as a mismatch.
5002: User incorrectly identified a mismatch as a match.
"""


# Setup UDP
udp_marker = socket.socket(socket.AF_INET,socket.SOCK_DGRAM)
ip = '127.0.0.1'
port = 12345

# Set up LSL stream
info = StreamInfo('NBackMarkers', 'Markers', 1, 0, 'string', 'visual_nback_task_001')
outlet = StreamOutlet(info)

BLOCKS = 13

black_color = "black"
class VisualERP:
    def sendTiD(self, base_message):
        message = base_message
        udp_marker.sendto(message.encode('utf-8'), (ip, port))
        print(f"Sent UDP message: {message}")

    def __init__(self, root):
        self.root = root
        self.root.title("Visual Paradigm")
        self.colors = [
            "red", "orange", "yellow", "green", "blue", 
            "purple"
        ]

        # Get screen dimensions
        screen_width = self.root.winfo_screenwidth()
        screen_height = self.root.winfo_screenheight()

        # Set window dimensions
        self.root.geometry(f"{screen_width}x{screen_height}")

        # Initialize score and game state
        self.score = 0
        self.display_step = 0
        self.countdown = 3
        self.ROUNDS = 30
        self.block = 0
        self.x = 0
        self.y = 0
        self.accept_input = False  
        self.accept_restart = False
        self.accept_start = False
        self.round_number = 0
        self.color_delay = 800     #THIS IS TIME PERSON SEES THE COLOR WORDS
        self.response_delay = 1000  #THIS IS TIME PERSON HAS TO RESPOND
        self.question_id = None 
        self.start_time = None

        # Set up the Text widget for message display
        # Set up the Text widget for message display
        # Set up the Text widget for message display
        self.message_label = tk.Text(
            root, 
            height=20,  # Increased height for a larger text area
            width=80,  # Increased width for more space
            font=("Arial", 500),  # Larger font for readability
            wrap="word", 
            bg="#D9D9D9", 
            relief="flat", 
            bd=10
        )
        self.message_label.tag_configure("center", justify="center")
        self.message_label.place(relx=0.5, rely=0.5, anchor="center")  

        # Set up the score label
        self.score_label = tk.Label(
            root, 
            text=f"Score: {self.score}", 
            font=("Arial", 100),  
            bg="#D9D9D9"
        )
        self.score_label.place(relx=0.5, rely=0.9, anchor="center") 

        # Key event listeners
        self.root.bind("<KeyPress-y>", lambda event: self.process_input(True))
        self.root.bind("<KeyPress-n>", lambda event: self.process_input(False))
        self.root.bind("<KeyPress-r>", lambda event: self.restart_game(True))
        self.root.bind("<KeyPress-space>", lambda event: self.start_game(True))

        # listen to asdf 
        self.root.bind("<KeyPress-a>", lambda event: self.process_input(True))
        self.root.bind("<KeyPress-s>", lambda event: self.process_input(True))
        self.root.bind("<KeyPress-d>", lambda event: self.process_input(True))
        self.root.bind("<KeyPress-f>", lambda event: self.process_input(True))

        # listen to jkl;
        self.root.bind("<KeyPress-j>", lambda event: self.process_input(False))
        self.root.bind("<KeyPress-k>", lambda event: self.process_input(False))
        self.root.bind("<KeyPress-l>", lambda event: self.process_input(False))
        self.root.bind("<KeyPress-semicolon>", lambda event: self.process_input(False))

        self.block_number = 0  # Track the current block
        
        self.start_screen()

    # Display start message
    def start_screen(self):
        if self.block < BLOCKS:
            self.sendTiD("7000")  # Event ID for block start
            self.ROUNDS = 30
            self.message_label.configure(state="normal")
            self.message_label.delete("1.0", tk.END)
            self.message_label.insert(tk.END, "Press Spacebar\n to Begin", "center")
            self.message_label.configure(state="disabled")
            self.accept_start = True
        else:
            #end the program
            self.root.destroy()

    # Countdown
    def count(self):
        if self.countdown > 0:
            self.message_label.configure(state="normal")
            self.message_label.delete("1.0", tk.END)
            self.message_label.insert(tk.END, str(self.countdown), "center")
            self.message_label.configure(state="disabled")
            self.countdown -= 1
            self.root.after(1000, self.count)
        else:
            self.start_round()

    # Display the three words
    def start_round(self):
        self.start_time = time.time() 
        if self.round_number < self.ROUNDS:
            self.display_step += 1
            self.sendTiD("6000")  # Event ID for round start
            tf = random.randint(1, 100)
            if tf < 20:
                self.x = random.randint(0, self.colors.__len__() - 1)
                self.y = random.randint(0, self.colors.__len__() - 1)
                while self.y == self.x:
                    self.y = random.randint(0, self.colors.__len__() - 1)
            else:
                self.x = random.randint(0, self.colors.__len__() - 1)
                self.y = self.x
            random_color2 = random.randint(0, self.colors.__len__() - 1)  # Random color for color3
            random_color3 = random.randint(0, self.colors.__len__() - 1)  # Random color for color3
            random_int = random.randint(1, 3)  # Random placement selection

            self.sendTiD("3001" if self.x == self.y else "3002")  # Event ID for match or mismatch
            self.message_label.configure(state="normal")
            self.message_label.delete("1.0", tk.END)
            #mismatch could be first word
            if random_int == 1:
                self.message_label.insert(tk.END, self.colors[self.y] + " ", ("color1", "center"))
                self.message_label.tag_configure("color1", foreground=self.colors[self.x])  # Random color for color3

                self.message_label.insert(tk.END, self.colors[random_color2] + " ", ("color2", "center"))
                self.message_label.tag_configure("color2", foreground=black_color)  # Black text for color1

                self.message_label.insert(tk.END, self.colors[random_color3] + " ", ("color3", "center"))
                self.message_label.tag_configure("color3", foreground=black_color)  # Black text for color2
            #mismatch could be second word
            elif random_int == 2:
                self.message_label.insert(tk.END, self.colors[random_color2] + " ", ("color1", "center"))
                self.message_label.tag_configure("color1", foreground=black_color)  # Black text for color1

                self.message_label.insert(tk.END, self.colors[self.y] + " ", ("color2", "center"))
                self.message_label.tag_configure("color2", foreground=self.colors[self.x])  # Random color for color3

                self.message_label.insert(tk.END, self.colors[random_color3] + " ", ("color3", "center"))
                self.message_label.tag_configure("color3", foreground=black_color)  # Black text for color2
            #mismatch could be third word
            else:
                self.message_label.insert(tk.END, self.colors[random_color2] + " ", ("color1", "center"))
                self.message_label.tag_configure("color1", foreground=black_color)  # Black text for color1

                self.message_label.insert(tk.END, self.colors[random_color3] + " ", ("color2", "center"))
                self.message_label.tag_configure("color2", foreground=black_color)  # Black text for color2

                self.message_label.insert(tk.END, self.colors[self.y] + " ", ("color3", "center"))
                self.message_label.tag_configure("color3", foreground=self.colors[self.x]) 
           
            self.message_label.configure(state="disabled")
            self.accept_input = True
          
        else:
            self.show_final()

    # Displays a blank screen between rounds
    def show_blank(self):
        if(self.accept_input):
            self.ROUNDS += 1
        self.accept_input = False
        self.round_number += 1
        self.message_label.configure(state="normal")
        self.message_label.delete("1.0", tk.END)
        self.message_label.configure(state="disabled")

        #CHANGE THIS TO CHANGE THE BLANK TIME BETWEEN THE ROUNDS
        possible_delay = [1000]
        random_delay = random.choice(possible_delay)
        self.root.after(random_delay, self.start_round)

    def show_final(self):
        self.sendTiD("8000")  # Event ID for block end
        # Existing final screen display logic
        self.message_label.configure(state="normal")
        self.message_label.delete("1.0", tk.END)
        self.message_label.insert(tk.END, f"Final Score: {self.score}\n Press R to Restart", "center")
        self.message_label.configure(state="disabled")
        self.block += 1
        self.accept_restart = True

    def process_input(self, user_said_yes):
        if not self.accept_input:
            return

        self.accept_input = False

        # Calculate response time
        response_time = time.time() - self.start_time

        # Determine if the stimulus was a match or mismatch
        is_match = self.x == self.y

        # Determine if the user's response was correct
        correct = (user_said_yes and is_match) or (not user_said_yes and not is_match)

        # Send event ID based on correctness and match/mismatch
        if correct:
            if is_match:
                self.sendTiD("4001")  # Correct with Match
            else:
                self.sendTiD("4002")  # Correct with Mismatch
        else:
            if is_match:
                self.sendTiD("5001")  # Incorrect with Match
            else:
                self.sendTiD("5002")  # Incorrect with Mismatch
        
        # Update score if the response was correct
        if correct:
            self.score += 1

        # Update the score display and move to the next round
        self.score_label.config(text=f"Score: {self.score}")
        self.show_blank()

    def restart_game(self, restart):
        # Restart the game
        if not self.accept_restart:
            return
        self.accept_restart = False
        self.round_number = 0
        self.countdown = 3
        self.score = 0
        self.score_label.config(text=f"Score: {self.score}")
        self.start_screen()

    def start_game(self, start):
        # Start the game
        if not self.accept_start:
            return
        self.accept_start = False
        self.round_number = 0
        self.countdown = 3
        self.score = 0
        self.score_label.config(text=f"Score: {self.score}")
        self.count()
    


if __name__ == "__main__":
    root = tk.Tk()
    app = VisualERP(root)
    root.mainloop()
