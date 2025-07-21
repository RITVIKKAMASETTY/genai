import os

from groq import Groq
from dotenv import load_dotenv
load_dotenv()
client = Groq(
    api_key=os.environ.get("GROQ_API"),
)
chat_completion = client.chat.completions.create(
    messages=[
        {
            "role": "user",
            "content": "Explain which is greater 9.8 or 9.11",
        }
    ],
    model="llama-3.3-70b-versatile",
)
print(chat_completion)
print(chat_completion.choices[0].message.content)