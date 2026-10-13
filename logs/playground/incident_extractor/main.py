from openai import OpenAI
from dotenv import load_dotenv
from models import Incident
from pprint import pp 
import os

#Load .env variables
load_dotenv()

#Create client
client = OpenAI(
    base_url=os.getenv('ollama_local_baseurl'),
    api_key=os.getenv('ollama_local_api_key')
)

#Incident
incident_text = """
The customer_ingestion pipeline failed at 03:42.

silver_transform failed because Spark could not
resolve the customer_type column.
"""

#Schema
schema = Incident.model_json_schema()

tests = [
    """
    The customer_ingestion pipeline failed at 03:42.

    silver_transform failed because Spark could not
    resolve the customer_type column.
    """,

    """
    customer_ingestion failed last night.
    """,

    """
    Monitoring says customer_ingestion succeeded.
    The incident ticket says customer_ingestion failed.
    """,

    """
    Something went wrong last night.
    """,
]

#Logic

for incident_text in tests:
    response = client.chat.completions.create(
        model = 'deepseek-r1:14b',
        messages=[
            {
                "role": "system",
                "content": """
    You extract pipeline incident information.

    Rules:
    - Do not invent missing information.
    - If failed_task is unknown, return null.
    - If error_type is unknown, return null.
    - Put unknown fields in missing_information.
    - Evidence must come from the supplied incident text.
    """,
            },
            {
                "role": "user",
                "content": incident_text,
            },
        ],
        response_format={
            "type": "json_schema",
            "json_schema": {
                "name": "incident",
                "schema": schema,
            }
        }
    )

    raw_response = response.choices[0].message.content
    # print(f'RAW_RESPONSE: {raw_response}')

    #Validate Answer
    try:
        incident = Incident.model_validate_json(raw_response)
        print('\nVALIDATED OBJECT:')
        print(incident)
    except Exception as exc:
        print("Invalid model output:", exc)