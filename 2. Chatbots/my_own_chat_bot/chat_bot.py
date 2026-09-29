from langchain_huggingface import HuggingFaceEndpoint
from dotenv import load_dotenv
import os
from langchain.messages import HumanMessage,SystemMessage,AiMessage

load_dotenv()

token = os.getenv("huggingface_api_key")

llm = HuggingFaceEndpoint(
    repo_id="TinyLlama/TinyLlama-1.1B-Chat-v1.0",
    task="conversational",   # fixed
    huggingfacehub_api_token=token,
    temperature=0.7,
    max_new_tokens=256
)
chat_histroy=[
    SystemMessage(content="You are a helpful assistant.")
]

while True:
    user_input = input("You: ")
    chat_histroy.append(HumanMessage(content=user_input))
    if user_input.lower() == "exit":
        print("Chat ended.")
        break

    result = llm.invoke(chat_histroy)
    chat_histroy.append(AiMessage(content=result))

    print("AI:", result)