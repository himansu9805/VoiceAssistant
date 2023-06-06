import os
from bardapi import Bard
from dotenv import load_dotenv

load_dotenv()

token = str(os.getenv("BARD_KEY"))
bard = Bard(token=token)


def get_answer(prompt: str):
    response = bard.get_answer(prompt)
    return response['content']
