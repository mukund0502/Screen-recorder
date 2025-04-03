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


def fetch_frames (results):
    global frames_list, RECORD_SECONDS, fps, screen_siz
    print('Frames recording started...')
    start_taking_ss = time.time()
    got_image_for_seconds = 0
    images_to_make_video = []
    with mss.mss() as sct:
        while got_image_for_seconds < RECORD_SECONDS:
            if keyboard.is_pressed('q'):
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

def fetch_audio(results):
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
        if keyboard.is_pressed('q'):
            break
    stream.stop_stream()
    stream.close()
    audio.terminate()
    print ("audio recording stopped")
    results['audio_bytes'] = b''.join(Recordframes)

if __name__ == '__main__':
    with Manager() as manager:
        results = manager.dict()
        frame_process = Process(target=fetch_frames, daemon = True, args=(results,))
        audio_process = Process(target=fetch_audio, daemon = True, args=(results,))
        frame_process.start()
        audio_process.start()
        frame_process.join()
        audio_process.join()
        clip = moviepy.video.io.ImageSequenceClip.ImageSequenceClip(results['frames_list'], fps = fps)
        waveFile = wave.open('temp.wav', 'wb')
        waveFile.setnchannels (CHANNELS)
        waveFile.setsampwidth(audio.get_sample_size(FORMAT))
        waveFile.setframerate(RATE)
        waveFile.writeframes (results['audio_bytes'])
        waveFile.close()
        audio_clip = moviepy.audio.io.AudioFileClip.AudioFileClip('temp.wav') 
        clip.audio = audio_clip
        clip.write_videofile('my_video.mp4')