#!/usr/bin/env python3

# NOTE: this example requires PyAudio because it uses the Microphone class

import time
import pyttsx3

import speech_recognition as sr
from gtts import gTTS
from io import BytesIO
import pygame

class Speech:
    def __init__(self, callback_function_returns_text):
        self.r = sr.Recognizer()
        self.m = sr.Microphone()
        with self.m as source:
            self.r.adjust_for_ambient_noise(source)  # we only need to calibrate once, before we start listening
        self.stop_listening = None
        self.start_listening()
        self.callback_function = callback_function_returns_text


        #text to speech
        self.tts_offline_engine = pyttsx3.init()   #has 2 voices in windows

        pygame.init()
        pygame.mixer.init()

    def callback(self, recognizer, audio):
        # received audio data, now we'll recognize it using Google Speech Recognition
        try:
            # for testing purposes, we're just using the default API key
            # to use another API key, use `r.recognize_google(audio, key="GOOGLE_SPEECH_RECOGNITION_API_KEY")`
            # instead of `r.recognize_google(audio)`
            # print("Google Speech Recognition thinks you said " + recognizer.recognize_google(audio))
            print("[Transcribing mic data]")
            transcribed_text =  recognizer.recognize_google(audio)
            self.callback_function(transcribed_text)
        except sr.UnknownValueError:
            print("Google Speech Recognition could not understand audio")
            return ""
        except sr.RequestError as e:
            print("Could not request results from Google Speech Recognition service; {0}".format(e))
            return ""

    def start_listening(self):
        print("Starting mic")
        self.stop_listening = self.r.listen_in_background(self.m, self.callback)
    
    #This function won't probably be used
    def stop_listening(self):
        self.stop_listening(wait_for_stop=False)


    def text_to_speech_google(self, text):
        mp3_fo=BytesIO()
        tts=gTTS(text, lang='en')
        tts.write_to_fp(mp3_fo)
        mp3_fo.seek(0)
        pygame.mixer.music.load(mp3_fo, 'mp3')
        pygame.mixer.music.play()
        # time.sleep(5)
    
    #offline TTS
    def say(self, text):
        text = "hello"
        self.tts_offline_engine.say(text)
        self.tts_offline_engine.runAndWait()
        print("said")

        

if __name__ == "__main__":
    s = Speech()
    s.text_to_speech_offline("hello you")
    # print(s.tts_offline_engine.getProperty('voices'))