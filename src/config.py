import os
from dotenv import load_dotenv
from openai import AzureOpenAI

# Load variables from .env file
load_dotenv()

# Azure OpenAI Credentials
ENDPOINT = "https://foundry-ai-prd-eus2-01.cognitiveservices.azure.com/"
MODEL_NAME = "gpt-4o-mini"
DEPLOYMENT = "gpt-4o-mini"
SUBSCRIPTION_KEY = os.getenv("AZUREAIAPIKEY")
API_VERSION = "2024-12-01-preview"

# Global client instance
if not SUBSCRIPTION_KEY:
    raise ValueError("GoodModel environment variable is missing from .env file.")

client = AzureOpenAI(
    api_version=API_VERSION,
    azure_endpoint=ENDPOINT,
    api_key=SUBSCRIPTION_KEY,
)
