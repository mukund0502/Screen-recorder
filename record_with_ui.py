import tkinter as tk
import multiprocessing
import time
import cv2
import moviepy.audio
import moviepy.audio.io
import numpy as np
import mss
import time
import keyboard
import moviepy.video.io.ImageSequenceClip
import pyaudio
import math
from multiprocessing import Process, Manager
import wave

with mss.mss() as sct:
    screen_size = sct.monitors [1]

fps = 10 
FORMAT = pyaudio.paInt16
CHANNELS = 1
RATE = 44100
audio = pyaudio.PyAudio()
CHUNK = 512
RECORD_SECONDS = 20
stop_rec = False

def fetch_frames (stopper, results):
    global frames_list, RECORD_SECONDS, fps, screen_siz
    print('Frames recording started...')
    start_taking_ss = time.time()
    got_image_for_seconds = 0
    images_to_make_video = []
    with mss.mss() as sct:
        while got_image_for_seconds < RECORD_SECONDS:
            if stopper.value:
                break
            frame = np.array(sct.grab(screen_size))
            frame = cv2.cvtColor(frame, cv2.COLOR_RGBA2BGR)
            images_to_make_video.append(frame)
            # out.write(frame)
            got_image_for_seconds+=1/fps
            current_time = time.time()
            if (current_time - start_taking_ss) < got_image_for_seconds: 
                while(time.time()-start_taking_ss < got_image_for_seconds):
                    time.sleep(0.001)
                current_time = time.time()
            
            elif (current_time - start_taking_ss) > got_image_for_seconds: 
                while((time.time()-start_taking_ss) > got_image_for_seconds): 
                    images_to_make_video.append(frame) 
                    # out.write(frame)
                    got_image_for_seconds+=1/fps
            else:
                continue
    
    print('Frame recording stopped')
    results['frames_list'] = images_to_make_video


def fetch_audio(stopper, results):
    global audio_bytes, audio, stop_rec
    stream = audio.open(format=FORMAT, 
                        channels=CHANNELS, 
                        rate=RATE, 
                        input=True, 
                        input_device_index = 1,
                        frames_per_buffer=CHUNK)
    
    Recordframes = []
    print('Audio recording started...')
    i = 0
    while(i < math.ceil(RATE / CHUNK * RECORD_SECONDS)):
        data = stream.read(CHUNK)
        Recordframes.append(data)
        i+=1
        if stopper.value:
            break
    stream.stop_stream()
    stream.close()
    audio.terminate()
    print ("audio recording stopped")
    results['audio_bytes'] = b''.join(Recordframes)


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
    with Manager() as manager:
        results = manager.dict()
        frames_record = multiprocessing.Process(target=fetch_frames, daemon=True, args=(stopper,results,))
        audio_record = multiprocessing.Process(target=fetch_audio, daemon=True, args=(stopper,results,))
        frames_record.start()
        audio_record.start()
        
        # while(True):
        #     if 'audio_bytes' in results and 'frames_list' in results:
        #         print(results.keys())
        #         break
        #     print('waiting')
        #     time.sleep(1)





def stop():
    global stopper
    stopper.value = True  # Signal the process to stop
    print("Button 2 clicked")
    button2.config(state=tk.DISABLED)
    button1.config(state=tk.NORMAL)



if __name__ == '__main__':
    # Create a multiprocessing manager and stopper
    manager = multiprocessing.Manager()
    stopper = manager.Value('b', False)  # 'b' for boolean
    results = manager.dict()
    # Create main window
    root = tk.Tk()
    root.title("Recorder")

    # Create a frame to hold the buttons
    frame = tk.Frame(root)
    frame.pack(pady=20, padx=20)

    # Create buttons
    button1 = tk.Button(frame, text="record", command=record, padx=15, pady=10, state=tk.NORMAL)
    button2 = tk.Button(frame, text="stop", command=stop, padx=15, pady=10, state=tk.DISABLED)

    # Pack buttons one below the other
    button1.pack(side=tk.LEFT, pady=5)
    button2.pack(side=tk.RIGHT, pady=5)

    # Run the main loop
    root.mainloop()
