import time
from helpers.face_vision import Face
from helpers.speech import Speech
from helpers.generative_ai import Gemini

from helpers.communication import send_update_to_admin

import threading, os


class Jennie:
    def __init__(self):
        self.start_camera_server_process()
        
        self.face = Face()
        self.speech = Speech(self.callback_speech_text_input)
        self.gemini = Gemini()

    #function to be called when this object is deleted
    def __del__(self):
        print("Brain Stopped")

    
    def start_camera_server_process(self):
        def run():
            os.system("python3.10 helpers/camera_server.py")
        
        server_process = threading.Thread(target=run, args=())
        server_process.start()
        time.sleep(3)



    
    def callback_speech_text_input(self, query):
        print(query)
        self.respond_gemini(query)

    
    def respond_gemini(self, query):
        response = self.gemini.chat_with_gemini(query)
        say_this = self.parse_gemini_response(response)
        print("Gemini:", say_this)
        self.speech.text_to_speech_google(say_this)
        print("done")

    
    def parse_gemini_response(self, text):
        #parse system commands in gemini response
        #todo
        return text

    

    
if __name__ == "__main__":
    jennie = Jennie()
    print("Initiated brain")
    # while True: