from langchain.chat_models import ChatOpenAI
from dotenv import load_dotenv

load_dotenv()
chat = ChatOpenAI(model="gpt-3.5-turbo", temperature=0.9)
response = chat("what is the capital of PAkistan?")
print(response.content)


