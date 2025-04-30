from dotenv import load_dotenv
from openai import AzureOpenAI
import os

from clio.summary.summary_model import ApplicationSummary


class OpenAISummariser:
    def __init__(self):
        load_dotenv()
        self.openai_model = os.environ.get("AZURE_OPENAI_MODEL", "gpt-4.1-mini")
        api_version = os.environ.get("OPENAI_API_VERSION", "2024-12-01-preview")
        azure_endpoint = os.environ.get("AZURE_OPENAI_ENDPOINT")
        api_key = os.environ.get("AZURE_OPENAI_KEY")

        # gets the API Key from environment variable AZURE_OPENAI_API_KEY
        self.client = AzureOpenAI(
            api_version=api_version,
            azure_endpoint=azure_endpoint,
            azure_deployment=self.openai_model,
            api_key=api_key,
        )

    def summarise_document(self, document_text: str) -> ApplicationSummary:
        # completion = self.client.chat.completions.create(
        #     model=self.openai_model,
        #     messages=[
        #         {
        #             "role": "system",
        #             "content": "Summarise the outcome of this application and why that outcome was reached. Give your response in the format {'outcome':[outcome],'reason':[reason]}",
        #             "role": "user",
        #             "content": f"Here is the document: {document_text}",
        #         },
        #     ],
        # )
        return {"outcome": "Approved", "reason": "test case."}
