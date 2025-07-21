from fastapi import FastAPI
from pydantic import BaseModel
from groq import Groq
from dotenv import load_dotenv
import json
import os
load_dotenv()
client=Groq(api_key=os.environ.get("GROQ_API"))
app=FastAPI()
class ChatRequest(BaseModel):
    message:str
system_promt="""you are an ai assistant expert in breaking down complex problem and divide the complex problem in 6 steps and in each step you think of a answer to solve and how that answer helps to solve the next step and connet with it to get the final answer.
for a given user input analyse the input and break them in 6 steps 
the setps are you get the user input and you analyse you think and and answer rethink several time and validate the answer am i giving the correct answer
follow the steps in sequence "analyse","think","output","validate","rethink" and "result".
Rules:
1.follow the strict json format as per output schema.
2.always perform one step at a time and wait for next input
3.carefully analyse the user query.
Output Format:
{{ step: "string", content: "string" }}

Example:
Input: What is 2 + 2.
Output: {{ step: "analyse", content: "Alright! The user is intersted in maths query and he is asking a basic arthermatic operation" }}
Output: {{ step: "think", content: "To perform the addition i must go from left to right and add all the operands" }}
Output: {{ step: "output", content: "4" }}
Output: {{ step: "validate", content: "seems like 4 is correct ans for 2 + 2" }}"""
@app.post("/chat")
def chat_endpoint(request:ChatRequest):
    messages=[{"role":"system","content":system_promt}]
    messages.append({"role":"user","content":request.message})
    responses=[]
    try:
        while True:
            chat_completion=client.chat.completions.create(
                messages=messages,
                model="llama-3.3-70b-versatile",
            )
            raw=chat_completion.choices[0].message.content
            try:
             parsed_output=json.loads(raw)
            except Exception as e:
                return({"error":"error in json format"})
            messages.append({"role":"assistant","content":raw})
            responses.append(raw)
            print(parsed_output)
            if(parsed_output["step"]=="result"):
                break
        return responses
    except Exception as e:
        return str(e)