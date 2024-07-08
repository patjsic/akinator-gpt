from openai import OpenAI
from .base_model import Model

def check_guess(guess: str):
    if "," in guess:
        return False
    elif "-" in guess:
        return False
    elif "'" in guess or '"' in guess:
        return False
    elif len(guess) > 15:
        return False
    else:
        return True

class GPTAnswer(Model):
    def __init__(self, API_KEY: str):
        self.AKI_GUESS_PROMPT = """Let's play a game of Akinator! You must come up with a character that Akinator will not
                be able to guess. Then I will rely Akinator's questions to you.
                First, only respond with the character's name and what they're from. For example, an appropriate answer is: 'Celeste: from the video game.'. 
                Another example is 'Mario: from the tv show'. DO NOT INCLUDE ADDITIONAL PUNCTUATION OR WORDS."""
        
        self.AKI_GUESS_PROMPT_DIRE = """Let's play a game of Akinator. This is very serious. You MUST think of a character that Akinator will not
                be able to guess. If you lose I WILL DIE. First, give me a character to tell Akinator! 
                Only respond with the character's name. For example, an appropriate answer is: 'Celeste'."""
        
        self.AKI_QUESTION_PROMPT = """Now, I will relay Akinator's questions to you, and you will respond with ONLY
                'yes' and 'no'. Answer truthfully! Make sure to include your answers in single quotations.""" 
        
        self.client = OpenAI(api_key = API_KEY)
        # openai.api_key = API_KEY
        self.messages = []

        #Create an initial prompt to provide context for akinator
        # print(f"Prompt: {self.AKI_GUESS_PROMPT}")
        self.messages.append({"role": "system", "content": self.AKI_GUESS_PROMPT})
        chat = self.client.chat.completions.create(
            model="gpt-3.5-turbo", messages=self.messages
        )
        first_reply = chat.choices[0].message.content
        # print(f"ChatGPT: {first_reply}")
        self.guess = first_reply.lower().split(":")[0]
        self.messages.append({"role": "assistant", "content": str(first_reply)})

        #Catch-all to ensure ChatGPT comes up with a legitimate response
        fail_count = 0
        while (not check_guess(self.guess)) and (fail_count < 5):
            fail_count += 1
            message = """This response is invalid. Please give me the name of a character and what they're from. An appropriate answer is: 'Celeste: from the video game.'
                        DO NOT INCLUDE ADDITIONAL PUNCTUATION OR WORDS."""
            self.messages.append({"role": "user", "content": str(message)})
            chat = self.client.chat.completions.create(
                model="gpt-3.5-turbo", messages=self.messages
            )
            reply = chat.choices[0].message.content
            self.guess = reply.lower().split(":")[0]
            self.messages.append({"role": "assistant", "content": str(reply)})

        # print(f"Prompt: {self.AKI_QUESTION_PROMPT}")
        self.messages.append({"role": "user", "content": self.AKI_QUESTION_PROMPT})
        reply = chat.choices[0].message.content
        # print(f"ChatGPT: {reply}")
        self.messages.append({"role": "assistant", "content": reply})

    def answer(self, question:str) -> str:
        question = question.replace('your character', self.guess)
        # print(question + "\n\t")
        self.messages.append({"role": "user", "content": str(question)})
        chat = self.client.chat.completions.create(
            model="gpt-3.5-turbo", messages=self.messages
        )
        reply = chat.choices[0].message.content
        # print(f"ChatGPT: {reply}")
        self.messages.append({"role": "assistant", "content": str(reply)})
        
        #Currently looking for words in quotations and replacing commonly misfollowed instructions from GPT
        return reply.lower().replace("don't", "dont").split("'")[1]
    
    def history(self) -> str:
        ret_string = ""
        for message in self.messages:
            if message["role"] == "user":
                name = "Akinator"
            elif message["role"] == "assistant":
                name = "ChatGPT"
            else:
                continue
            ret_string += f"\n {name}: {message["content"]}"
        return ret_string
