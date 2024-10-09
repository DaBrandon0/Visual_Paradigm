import tkinter as tk
import random
import threading
import time







score = 0
colors = ["red","orange","yellow","green","blue","purple","black"]

tf = 0

# Create the main window
root = tk.Tk()
root.title("Visual")

answer=tk.StringVar()

# Instructions Label
label = tk.Label(root, text="Press Spacebar to Begin", font=("Helvetica", 16))
label.pack(pady=50)


def submit():
    if(answer.get()=="yes"):
        if(20 <= tf):
            score = score + 1
    else:
        if(20 > tf):
            score = score + 1

# Function to start the countdown on spacebar press

def start(event):
    for x in range(6):
        label.config(text= 5-x , fg='black')
        label.update_idletasks()
        time.sleep(1)
    while(1):
        tf = random.randint(1,100)
        if(20 > tf):
            x = random.randint(0,6)
            y = random.randint(0,6)
            while (y == x):
                y = random.randint(0,6)
            label.config(text= colors[x] , fg= colors[y])
            label.update()
            time.sleep(2)
        else:
            x = random.randint(0,6)
            label.config(text= colors[x] , fg= colors[x])
            label.update()
            time.sleep(2)
        label.config(text= "Did the color and word match?" , fg= "black")
        
        label.update()
        while(1):
            n = None

enter = tk.Entry(root,textvariable = answer, font=('calibre',10,'normal'))
sub = tk.Button(root,text = 'Submit', command = submit)
enter.update()
sub.update()

# Set the spacebar key event to start the process
root.bind('<space>', start)

# Set window size
root.geometry("400x200")

# Run the GUI main loop
root.mainloop()




        


        

        
    
    
    
        
    


