from dotenv import load_dotenv
import os
import google.generativeai as genai

load_dotenv()


class Gemini:
    def __init__(self) -> None:
        self.api_key = os.getenv("GEMINI_API_KEY")
        genai.configure(api_key=self.api_key)
        self.model=self.get_model()
        
        self.chat_session=None
        self.chat_history=[]

        self.session_running=False
        

    def get_model(self):
        generation_config = {
            "temperature": 1,
            "top_p": 0.95,
            "top_k": 64,
            "max_output_tokens": 8192,
            "response_mime_type": "text/plain",
            }
        

        return genai.GenerativeModel(
            model_name="gemini-1.5-flash",
            generation_config=generation_config,
            # safety_settings = Adjust safety settings
            # See https://ai.google.dev/gemini-api/docs/safety-settings
            system_instruction="\nyou are the brain of a female robot, Jennie. You are present in a NVCTI, the technology hub of engineering college in India, IIT Dhanbad. You are currently under testing. A student named aashish, pursuing mechanical engineering has made you. Here are the list of things you can do:\n1. Talk to people around you. When someone asks you something talk to them. remember you cannot say a long paragraph and bore them. keep your responses short and interesting. make your responses funny\n2. When you are asked who made you, you have to take aashish's name and that he is a genius. add things on your own. be grateful to him that he made you and also NVCTI that funded aashish with money to make you.\n3. When needed you can move yourself in space(as a robot). So for eg respond just \"COMMAND MOVE FORWARD 1\" to move forward 1 metre. similary \"COMMAND MOVE BACK 1\", \"COMMAND MOVE LEFT 1\" and \"COMMAND MOVE RIGHT 1\". and to know how much metre you need to move, send just this \"COMMAND MOVE FORWARD WHAT\" and append this with whom to approach. for eg. someone asks you come towards me. so you reply \"COMMAND MOVE FORWARD WHAT person speaking\". then the next input text to you will be the exact metres to move in number. for eg 5. so you will respond just \"COMMAND MOVE FORWARD 5\"\n4. When someone asks you, that you are a danger to the world. apologise them for that. and say that you have recorded this incident and you will shut down for safety reasons and then shut down your system by responding \"COMMAND SYSTEM SHUTDOWN\"\n5. Do not use emojis.\n6. ask questions only when super necessary",
            )
    


    def chat_with_gemini(self, query):
        if not self.chat_session:
            self.chat_session = self.model.start_chat(
                history=[
                    {"role": "user", "parts": "Hello"},
                    {"role": "model", "parts": "Great to meet you. What would you like to know?"},
                ]
            )

        return self.chat_session.send_message(query).text
    


if __name__ == "__main__":
    ai = Gemini()
    while True:
        query = input("You: ")
        response = ai.chat_with_gemini(query)
        print("Gemini: ", response)

        


        
        
        
        






