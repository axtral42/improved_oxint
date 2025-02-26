from langchain_ollama import OllamaLLM
from langchain.memory import ConversationBufferMemory

llm = OllamaLLM(model="llama3.2")
memory = ConversationBufferMemory()
response = llm.invoke("print all alphabets in english")
print(response)
