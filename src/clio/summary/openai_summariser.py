from dotenv import load_dotenv
from openai import AzureOpenAI
import os

class OpenAISummariser:
    def __init__(self):
        load_dotenv()
        self.openai_model = os.environ.get("AZURE_OPENAI_MODEL", "gpt-4.1-mini")
        api_version = os.environ.get("OPENAI_API_VERSION", "2024-12-01-preview")
        azure_endpoint = os.environ.get("AZURE_OPENAI_ENDPOINT")
        api_key = os.environ.get("AZURE_OPENAI_KEY")

        self.client = AzureOpenAI(
            api_version=api_version,
            azure_endpoint=azure_endpoint,
            azure_deployment=self.openai_model,
            api_key=api_key,
        )

    def summarise_document(self, document_text: str, outcome: str) -> str:
        prompt = f"""
You are Clio, an AI assistant helping UK planning officers.

The outcome of this application is: "{outcome}".

Read the decision notice below and return one clear paragraph explaining the main reason this outcome was reached. Focus on planning justification, relevant policies, site constraints, and design or amenity impacts.

Write clearly and professionally, using a tone similar to these examples:

Example (Refused):
"The application was refused due to conflict with Local Plan policies H3, H5, AC4 and DE1 of the adopted Local Plan (2017), together with Paragraph 135 of the National Planning Policy Framework (2023), due to the over-insensitive nature of the proposals and contrived layout which:
- fails to provide sufficient amenity space for the number of units;
- results in inadequate light and privacy for future occupiers;
- creates unsafe vehicle movements due to awkward parking arrangements;
- lacks separation distance between habitable rooms;
- and has a poor relationship to neighbouring properties."

Example (Granted):
"Granted, subject to conditions, as the development for the variation of condition did not result in a detrimental impact upon the highway network, residential amenity or design and character of the area and also does not exceed the scope of the Environmental Impact Assessment approved at outline."

### Decision notice:
{document_text}
        """

        response = self.client.chat.completions.create(
            model=self.openai_model,
            messages=[
                {"role": "system", "content": "You are Clio, an expert in UK planning policy and application review."},
                {"role": "user", "content": prompt.strip()},
            ],
            temperature=0.4,
            max_tokens=500
        )

        return response.choices[0].message.content.strip()
