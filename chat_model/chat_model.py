import os
import sys
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from autogen_ext.models.openai import OpenAIChatCompletionClient
from config.constants import MODEL_OPENAI
from dotenv import load_dotenv


load_dotenv()
def get_model_client():
    api_key = os.getenv("OPENAI_API_KEY")
    try:
        model_client = OpenAIChatCompletionClient(
            model= MODEL_OPENAI,
            api_key= api_key
        )
    except Exception as e:
        print(f"Exception: {e}")
    return model_client


# get_model_client()