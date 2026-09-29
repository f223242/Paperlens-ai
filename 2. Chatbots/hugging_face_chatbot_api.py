from langchain_huggingface import ChatHuggingFace, HuggingFaceEndpoint
from dotenv import load_dotenv
import os

load_dotenv()

# Get token from environment or pass directly
token = os.getenv('huggingface_api_key')

llm=HuggingFaceEndpoint(
    repo_id='TinyLlama/TinyLlama-1.1B-Chat-v1.0',
    task='text-generation',
    huggingfacehub_api_token=token,
    temperature=0.7,
    max_new_tokens=256
)

model = ChatHuggingFace(llm=llm)
result=model.invoke("What is the capital of Pakistan?")
print(result.content)