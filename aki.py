import os
import argparse
import akipy
import multiprocessing as mp

from tqdm import tqdm
from keys import OPENAI_API
from models.user import UserAnswer
from models.gpt_answer import GPTAnswer

def get_answer(question: str, model: object) -> str:
    ret = model.answer(question)
    return ret

def aki_loop(model_type: str = "user", game_idx: int = 0) -> None:
    """Manages the gpt->akinator loop logic
    """
    aki = akipy.Akinator()
    aki.start_game()

    count = 0

    if model_type == "user":
        model = UserAnswer()
    elif model_type == "gpt":
        model = GPTAnswer(API_KEY=OPENAI_API)
    else:
        raise ValueError("Model argument not recognized. Please choose one of ['user', 'gpt']")

    while not aki.win and count < 5:
        #Can currently keep calling akinator
        try:
            answer = aki.answer(get_answer(aki.question, model))
            count = 0
        except:
            print("Invalid Answer")
            count += 1
    
    if model_type == "gpt":
        #Create log directory if doesn't exist
        if not os.path.exists("logs"):
            os.makedirs("logs")
        
        with open(os.path.join("logs", f"log_{game_idx}.txt"), "w") as file:
            log = model.history() + "\n" + f"answer: {aki.name_proposition}" + f"\n guess: {model.guess}"
            file.write(log)

    print(f"Aki guess: {aki.name_proposition}")
    print(f"Aki description: {aki.description_proposition}")

if __name__=="__main__":
    num_processes = 100

    for i in tqdm(range(num_processes)):
        aki_loop(model_type="gpt", game_idx=i)
