import tkinter as tk
import multiprocessing
import time

def start_counter(stopper):
    i = 0
    while True:
        if stopper.value:  
            print('breaked loop')
            break
        print(i)
        time.sleep(1)
        i += 1

def record():
    global process  # Use a global variable to track the process
    print("Button 1 clicked")
    button1.config(state=tk.DISABLED)
    button2.config(state=tk.NORMAL)

    stopper.value = False  # Reset stopper before starting
    process = multiprocessing.Process(target=start_counter, daemon=True, args=(stopper,))
    process.start()


def stop():
    stopper.value = True  # Signal the process to stop
    print("Button 2 clicked")
    button2.config(state=tk.DISABLED)
    button1.config(state=tk.NORMAL)



if __name__ == '__main__':
    # Create a multiprocessing manager and stopper
    manager = multiprocessing.Manager()
    stopper = manager.Value('b', False)  # 'b' for boolean

    # Create main window
    root = tk.Tk()
    root.title("Recorder")

    # Create a frame to hold the buttons
    frame = tk.Frame(root)
    frame.pack(pady=20, padx=20)

    # Create buttons
    button1 = tk.Button(frame, text="resord", command=record, padx=15, pady=10, state=tk.NORMAL)
    button2 = tk.Button(frame, text="stop", command=stop, padx=15, pady=10, state=tk.DISABLED)

    # Pack buttons one below the other
    button1.pack(side=tk.LEFT, pady=5)
    button2.pack(side=tk.RIGHT, pady=5)

    # Run the main loop
    root.mainloop()
