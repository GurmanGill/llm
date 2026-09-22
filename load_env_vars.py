from dotenv import load_dotenv
import os

load_dotenv()

#Test OpenAIKey
openai_key = os.getenv('OPENAI_API_KEY')
print(openai_key)