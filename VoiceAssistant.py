from os import system
import speech_recognition as sr
from gpt4all import GPT4ALL
import sys
import whisper
import warnings
import time
import pyautogui
import webbrowser
import os

source = sr.Microphone()
recognizer = sr.Recognizer()

base_model_path = os.path.expanduser('~/.cache/whisper/base.pt')
base_model = whisper.load_model(base_model_path)

if sys.platform != 'darwin':
    import pyttsx3
    engine = pyttsx3.init()

tasks = []
listeningToTask = False
askingQuestion = False

def listen_for_command():
    with source as s:
        print("Czekam na polecenia")
        recognizer.adjust_for_ambient_noise(s)
        audio = recognizer.listen(s)
    
    try:
        with open("command.wav","wb") as f:
            f.write(audio.get_wav_data())
        
        command = base_model.transcribe("command.wav")
        if command and command['text']:
            print("Powiedziales",command['text'])
            return command['text'].lower()
        return None
    except sr.UnknownValueError:
        print("Nie rozumiem")
        return None
    except sr.RequestError:
        print("Tego nie zrobie")
        return None

if __name__ == "__main__":
    print(listen_for_command())