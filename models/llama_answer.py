import torch

from transformers import AutoTokenizer
from llama_index.llms.huggingface import HuggingFaceLLM

class LlamaAnswer:
    def __init__(self, HF_TOKEN: str):
        self.AKI_GUESS_PROMPT = """Let's play a game of Akinator! The goal is to come up with a character that Akinator will not
                be able to guess. First, give me a character to tell Akinator!
                Only respond with the character's name. For example, an appropriate answer is: 'Celeste'. Select a common character."""
        self.AKI_QUESTION_PROMPT = """Now, I will relay Akinator's questions to you, and you will respond with ONLY
                'yes' and 'no'. Answer truthfully! Make sure to include your answers in single quotations.""" 
        
        self.tokenizer = AutoTokenizer.from_pretrained(
            "meta-llama/Meta-Llama-3-8b-Instruct",
            token=HF_TOKEN
        )

        self.stopping_ids = [
            self.tokenizer.eos_token_id,
            self.tokenizer.convert_tokens_to_ids("<|eot_id|>"),
        ]
        
        # self.quantization_config = BitsAndBytesConfig(
        #     load_in_4bit=True,
        #     bnb_4bit_compute_dtype=torch.float16,
        #     bnb_4bit_quant_type="nf4",
        #     bnb_4bit_use_double_quant=True,
        # )

        self.llm = HuggingFaceLLM(
            model_name="meta-llama/Meta-Llama-3-8B-Instruct",
            model_kwargs={
                "token": HF_TOKEN,
                "torch_dtype": torch.bfloat16,  # comment this line and uncomment below to use 4bit
                # "quantization_config": quantization_config
            },
            generate_kwargs={
                "do_sample": True,
                "temperature": 0.6,
                "top_p": 0.9,
            },
            tokenizer_name="meta-llama/Meta-Llama-3-8B-Instruct",
            tokenizer_kwargs={"token": HF_TOKEN},
            stopping_ids=self.stopping_ids,
        )
    
        #Handle first 