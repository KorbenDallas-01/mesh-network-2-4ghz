import speech_recognition as sr
from gtts import gTTS
import pygame
import os
import time


def listen_for_command():
    """Records audio from microphone and converts to text."""
    r = sr.Recognizer()
    with sr.Microphone() as source:
        print("Listening...")
        audio = r.listen(source)

    try:
        user_input = r.recognize_google(audio)
        print(f"You said: {user_input}")
        return user_input
    except sr.UnknownValueError:
        print("Could not understand audio")
        return None
    except sr.RequestError as e:
        print(f"Error with speech recognition service: {e}")
        return None


def speak_response(text):
    """Converts text to speech and plays it."""
    try:
        tts = gTTS(text=text, lang='en')
        tts.save("response.mp3")
        pygame.mixer.init()
        pygame.mixer.music.load("response.mp3")
        pygame.mixer.music.play()
        while pygame.mixer.music.get_busy():
            pygame.time.Clock().tick(10)
        os.remove("response.mp3")  # Clean up the audio file
    except Exception as e:
        print(f"Error with text-to-speech: {e}")