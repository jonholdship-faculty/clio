from openai import AzureOpenAI
from pydantic import BaseModel
from dotenv import load_dotenv
import os
import PyPDF2

load_dotenv()

openai_model = os.environ.get("AZURE_OPENAI_MODEL", "gpt-4.1-mini")
api_version = os.environ.get("OPENAI_API_VERSION", "2024-12-01-preview")
azure_endpoint = os.environ.get("AZURE_OPENAI_ENDPOINT")
api_key = os.environ.get("AZURE_OPENAI_KEY")

client = AzureOpenAI(api_version=api_version,
            azure_endpoint=azure_endpoint,
            azure_deployment=openai_model,
            api_key=api_key,)

# Extract text from PDF
def extract_text_from_pdf(pdf_path):
    text = ""
    with open(pdf_path, "rb") as f:
        pdf_reader = PyPDF2.PdfReader(f)
        for page in pdf_reader.pages:
            text += page.extract_text()
    return text

# Extract text from the PDF
pdf_text = extract_text_from_pdf("data/PLANNING_APPLICATION.pdf")

# Use the extracted text in the chat
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
            - Is the application compliant with the planning guidance?
            - Is the application compliant with the planning conditions?
            - Is the application compliant with the planning permission?
            - Is the application compliant with the planning appeal?
            - Is the application compliant with the planning enforcement?
            - Is the application compliant with the planning appeal?

            Here are some of the restrictions that apply to the application:
            - The application must be within the curtilage of the property.
            - The application must be within the site boundaries.
            - The application must be within the planning zone.
            - The application must be within the planning permission.
            - The application must be within the planning appeal.
            - The application must be within the planning enforcement.
            - The application must be within the planning appeal.
            - All materials must be from the local forest.
            - Allowed post codes are SW19, SW20.

            Add a ✅ or ❌ to each criterion. Provide a summary list of the criteria and the result.
            """
        },
        {
            "role": "user",
            "content": f"Please analyze the following planning application text and provide a summary:\n\n{pdf_text}"
        }
    ]
)

# Print the response content
print(response.choices[0].message.content)