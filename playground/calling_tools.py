from openai import OpenAI
from ollama import chat
from dotenv import load_dotenv
import os
import json
from pprint import pprint

#Load env vars
load_dotenv()

#Create client
client = OpenAI(
    base_url=os.getenv('ollama_local_baseurl'),
    api_key=os.getenv('ollama_local_api_key')
)

#Tools
def get_pipeline_status(pipeline: str) -> str:

    """Get the latest status of a pipeline."""

    print(f"TOOL_CALLED: get_pipeline_status()")

    pipelines = {
        "customer_ingestion": {
            "status": "FAILED",
            "failed_task": "silver_transform"
        },
        "sales_ingestion": {
            "status": "SUCCESS",
            "failed_task": None
        }
    }

    return pipelines.get(
        pipeline,
        {"error": "Pipeline not found"}
    )

def get_pipeline_logs(pipeline: str) -> dict:
    """Get recent error logs for a pipeline."""

    print(f"TOOL_CALLED: get_pipeline_logs()")

    logs = {
        "customer_ingestion": [
            "Starting silver_transform",
            "Cannot resolve column customer_type",
            "Task failed"
        ]
    }

    return {
        "pipeline": pipeline,
        "logs": logs.get(pipeline, [])
    }

#Tools registery
tool_registry = {
    'get_pipeline_status' : get_pipeline_status,
    'get_pipeline_logs' : get_pipeline_logs
}

#Query
question = 'What is the captial of canada?'
question = 'Why did the customer_ingestion failed?'
question = 'Restart customer_ingestion'
messages=[
        {
            "role": "user",
            "content": (
                question
            )
        }
    ]

#Logic
response = chat(
    model="qwen3.5:4b",
    messages=messages,
    tools=[get_pipeline_status, get_pipeline_logs],
)

messages.append(response.message)
# print(response.message.tool_calls)

#Tool call 
for tool_call in response.message.tool_calls or []:

    #Tool name and arguments
    name = tool_call.function.name
    arguments = tool_call.function.arguments

    # print(tool_registry)
    #Check against present tools
    if tool_call.function.name not in tool_registry:
        raise ValueError('Unexpected tool')

    result = tool_registry[name](
        **arguments
    )

    messages.append(
        {
            'role': 'tool',
            'tool_name': tool_call.function.name,
            'content': json.dumps(result)
        }
    )

second_response = chat(
    model="qwen3.5:4b",
    messages=messages,
    tools=[get_pipeline_status],
)

pprint(second_response.message)