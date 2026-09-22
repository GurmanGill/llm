from openai import OpenAI
import ollama
from dotenv import load_dotenv
import logging
import os

#set logging
# 1. You MUST configure the minimum level explicitly
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s'
)

#load env
load_dotenv()

#client
client = OpenAI()

#context logs + documentation
docs = ''
with open('./docs/pipeline_docs.txt', 'r') as file:
    docs = file.read()

logs = ''
with open('./logs/pipeline_logs.txt', 'r') as file:
    logs = file.read()

context = docs + logs
logging.info('#' * 150)
logging.info(f'Context: {context}')
logging.info('#' * 150)

#Prompt
prompt = 'Why did customer_ingestion fail?'
prompt = """
Relevant documentation:
customer_type was renamed to customer_category.

OLD DOCUMENT — deprecated:
customer_type is the correct production column.
Source: legacy_runbook
Status: DEPRECATED
Updated: 2024

Relevant log:
Cannot resolve column customer_type.

Question:
Why did customer_ingestion fail?
"""

#call to action
response = client.responses.create(
    model = os.getenv('MODEL'),
    input = prompt,
    max_output_tokens = 100
)

print(response.output_text)

# print()
# #Manual text
# prompt = 'context' + context + 'Question: why did customer_ingestion fail'
# prompt = """
# Relevant documentation:
# customer_type was renamed to customer_category.

# OLD DOCUMENT — deprecated:
# customer_type is the correct production column.
# Source: legacy_runbook
# Status: DEPRECATED
# Updated: 2024

# Relevant log:
# Cannot resolve column customer_type.

# Question:
# Why did customer_ingestion fail?
# """

# #Test with ollama
# response = ollama.generate(
#     model='qwen:1.8b',
#     prompt = prompt
# )

# print(response.response)
