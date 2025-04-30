from openai import AzureOpenAI
from pydantic import BaseModel
from dotenv import load_dotenv
import os

load_dotenv()

openai_model = os.environ.get("AZURE_OPENAI_MODEL", "gpt-4.1-mini")
api_version = os.environ.get("OPENAI_API_VERSION", "2024-12-01-preview")
azure_endpoint = os.environ.get("AZURE_OPENAI_ENDPOINT")
api_key = os.environ.get("AZURE_OPENAI_KEY")

client = AzureOpenAI(api_version=api_version,
            azure_endpoint=azure_endpoint,
            azure_deployment=openai_model,
            api_key=api_key,)

# First upload the file
with open("data/PLANNING_APPLICATION.pdf", "rb") as f:
    file = client.files.create(
        file=f,
        purpose="assistants"
    )

# Then use the file in the chat
response = client.chat.completions.create(
    model=openai_model,
    messages=[
        {
            "role": "system",
            "content": """You are a helpful planning consultant. Check the application for the following criteria:
            - Is the application complete?
            - Is the application valid?
            - Is the application compliant with the planning policy?
            - Is the application compliant with the planning law?
            - Is the application compliant with the planning regulations?
            """
        },
        {
            "role": "user",
            "content": "Please analyze the attached PDF file and provide a summary of the application.",
            "file_ids": [file.id]
        }
    ]
)

# Print the response content
print(response.choices[0].message.content)