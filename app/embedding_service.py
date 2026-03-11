import os
import requests
from dotenv import load_dotenv

load_dotenv()

HF_TOKEN = os.getenv("HF_TOKEN")
MODEL_ID = "sentence-transformers/all-MiniLM-L6-v2"
API_URL = f"https://router.huggingface.co/hf-inference/models/{MODEL_ID}/pipeline/feature-extraction"


class HFEmbeddings:
    def __init__(self, api_url, token=None):
        self.api_url = api_url
        self.headers = {"Authorization": f"Bearer {token}"} if token else {}

    def encode(self, texts):
        if isinstance(texts, str):
            texts = [texts]

        response = requests.post(
            self.api_url,
            headers=self.headers,
            json={"inputs": texts, "options": {"wait_for_model": True}}
        )

        if response.status_code != 200:
            raise Exception(f"HF API Error: {response.text}")

        return response.json()


    embeddings_model = HFEmbeddings(API_URL, HF_TOKEN)


    def get_embeddings():
        return embeddings_model