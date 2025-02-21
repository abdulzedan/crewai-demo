#!/usr/bin/env python
from openai import AzureOpenAI
import os
from dotenv import load_dotenv

# Load environment variables from the .env file in the project root.
load_dotenv()

client = AzureOpenAI(
    api_key=os.getenv("AZURE_API_KEY"),
    api_version=os.getenv("AZURE_API_VERSION", "2024-06-01"),
    azure_endpoint=os.getenv("AZURE_OPENAI_ENDPOINT"),
    max_retries=3
)

response = client.chat.completions.create(
    model=os.getenv("AZURE_DEPLOYMENT_NAME", "gpt-4o"),
    messages=[
        {
            "role": "system",
            "content": "Answer the query directly. Example: Input 'What is 2+2?' → Output 'Final Answer: 4'."
        },
        {
            "role": "user",
            "content": "What is the capital of France?"
        }
    ],
    temperature=0.1,
    max_tokens=150
)

print("LLM Response:", response.choices[0].message.content)
