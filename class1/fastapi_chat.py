from fastapi import FastAPI
from pydantic import BaseModel
from groq import Groq
from dotenv import load_dotenv
import os
load_dotenv()
client=Groq(api_key=os.environ.get("GROQ_API"))
app=FastAPI()
#request schema
class ChatRequest(BaseModel):
    message:str

@app.post("/chat")
def chat_endpoint(request:ChatRequest):
    try:
        chat_completion=client.chat.completions.create(
            messages=[
                {
                    "role":"user",
                    "content":request.message
                }
            ],
            model="llama-3.3-70b-versatile",
        )
        return chat_completion.choices[0].message.content
    except Exception as e:
        return str(e)