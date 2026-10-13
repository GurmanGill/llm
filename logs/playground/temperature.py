from openai import OpenAI
from dotenv import load_dotenv
import os

#load env vars
load_dotenv()

client = OpenAI()

def call_open_ai(
        prompt: str,
        temperature: float | None = None,
        max_output_token: int = 300,
        model: str = 'gpt-5.6-luna'
) -> str:

    response = client.responses.create(
        model=model,
        input=prompt,
        temperature=temperature,
        max_output_tokens=max_output_token
    )

    return response.output_text


for temp in [0.0, 0.3, 0.7, 0.9, 1.2]:

    print(call_open_ai('What is apple?'))
    print( '#' * 200)