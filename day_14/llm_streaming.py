from dotenv import load_dotenv
from langchain_groq import ChatGroq

load_dotenv()

model = ChatGroq(
    model="openai/gpt-oss-120b",
    temperature=0
)
response = model.stream(
    "Explain what an AI agent is in simple words."
)
print("\nAI Response:\n")

for chunk in response:

    print(
        chunk.content,
        end="",
        flush=True
    )


print("\n")