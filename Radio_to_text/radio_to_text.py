import socket
import numpy as np
import speech_recognition as sr
import time
import datetime
import matplotlib.pyplot as plt
import sounddevice as sd

#Allows for multiple streams 
user_input = input("Enter a port number:")

UDP_IP = "127.0.0.1"
UDP_PORT = int(user_input)
BUFFER_SIZE = 1024  

r = sr.Recognizer()
sample_rate = 16000  

sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
sock.bind((UDP_IP, UDP_PORT))

print(f"Listening for audio on UDP {UDP_IP}:{UDP_PORT}...")
#Collect multiple chunks of audio data 
data_chunks = np.array([], dtype=np.float32)

while True:
    data, addr = sock.recvfrom(BUFFER_SIZE)
    if not data:
        print("No data in buffer...")
        continue
    ct = datetime.datetime.now()
    #print(f"{ct} Size of data: {len(data)}")
    # Convert float32 samples to int16 PCM for SpeechRecognition
    audio_float = np.frombuffer(data, dtype=np.float32)
    data_chunks = np.concatenate((data_chunks, audio_float))
    if len(data_chunks) > (BUFFER_SIZE * 100):
        #### DEBUG FEATURES ####    
        #sd.play(data_chunks, samplerate=sample_rate)
        #sd.wait() 

        # plt.figure(figsize=(10, 4))
        # plt.plot(data_chunks, color='blue')
        # plt.title("Received Audio Waveform")
        # plt.xlabel("Sample Number")
        # plt.ylabel("Amplitude (float32)")
        # plt.grid(True)
        # plt.tight_layout()
        # plt.show()
        
        # user_in = input("Enter or q:")
        # if user_in.strip().lower() == 'q':
        #     break
        # else:
        #### END DEBUG ####
        audio_int16 = np.int16(data_chunks * 32767)

        audio_data = sr.AudioData(audio_int16.tobytes(), sample_rate, 2)  # 16-bit PCM

        try:
            text = r.recognize_google(audio_data, language="fi-FI")
            print(f"{ct} Recognized: {text}")
            data_chunks = np.array([], dtype=np.float32)
        except sr.UnknownValueError:
            #print(f"{ct} Could not understand audio chunk.")
            data_chunks = np.array([], dtype=np.float32)
        except sr.RequestError as e:
            print(f"{ct} STT service error: {e}")
            data_chunks = np.array([], dtype=np.float32)
    #else:
        #print(f"{ct} Collecting data, Current size {len(data_chunks)}")
