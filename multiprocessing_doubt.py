import tkinter as tk
import multiprocessing
import time
import threading

def start_counter(stopper):
    i = 0
    while True:
        if stopper.get() == True:
            break
        print(i)
        time.sleep(1)
        i+=1


def on_button1_click():
    print("Button 1 clicked")
    button1.config(state=tk.DISABLED)
    button2.config(state=tk.NORMAL)

    with multiprocessing.Manager() as manager:
        stopper = manager.Value('stopper', False)
        process = multiprocessing.Process(target=start_counter, daemon=True, args=(stopper,))
        process.start()

        time.sleep(5)
        stopper.set(True)


def on_button2_click():
    print("Button 2 clicked")
    button2.config(state=tk.DISABLED)
    button1.config(state=tk.NORMAL)

print('whole code ran')
    
if __name__ == '__main__':
    # Create main window
    root = tk.Tk()
    root.title("recorder")

    # Create a frame to hold the buttons
    frame = tk.Frame(root)
    frame.pack(pady=20, padx=20)

    # Create buttons
    button1 = tk.Button(frame, text="Button 1", command= lambda:on_button1_click(), padx = 15, pady=10, state=tk.NORMAL)
    button2 = tk.Button(frame, text="Button 2", command=lambda:on_button2_click(), padx = 15, pady=10, state=tk.DISABLED)

    # Pack buttons one below the other
    button1.pack(side=tk.LEFT, pady=5)
    button2.pack(side=tk.RIGHT, pady=5)

    # Run the main loop
    root.mainloop()

