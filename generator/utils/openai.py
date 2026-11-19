
import os
from openai import OpenAI
import certifi
from dotenv import load_dotenv
load_dotenv()
os.environ["SSL_CERT_FILE"] = certifi.where()

client = OpenAI(
    api_key=os.getenv("OPENAI_API_KEY"),
    base_url=os.getenv("BASE_URL"),
)

def get_openai_response(prompt: str) -> str:
    response = client.chat.completions.create(
        model="mistral-7b-instruct",
        messages=[{"role": "user", "content": prompt}],
        temperature=0,
    )
    return response.choices[0].message.content.strip()