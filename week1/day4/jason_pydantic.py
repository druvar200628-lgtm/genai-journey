import os
import json
from dotenv import load_dotenv
from groq import Groq
from pydantic import BaseModel

load_dotenv()
my_api_key=os.getenv("GROQ_API_KEY")
if not my_api_key:
    raise ValueError("api error")

client=Groq(api_key=my_api_key)
model="openai/gpt-oss-20b"

class Ticket(BaseModel):
    name:str
    email:str
    issue:str

schema=Ticket.model_json_schema()

response_format = {
    "type":"json_object"
}

system_prompt = f"""
Extract the personal information from the ticket based on this schema and give me an json output. {schema}
"""

message_sys = {
    "role":"system",
    "content":system_prompt
}

tect="hello my name is dhruva. I have purchased iphone which is not working at all. My address is delhi.my email is ghdgdg@gamil.com. My contact number is 5469763790"

prompt=f"this is customer ticket please extract the personal information from this {tect}"

message = {
    "role":"user",
    "content":prompt
}

messages = [message_sys,message]

response=client.chat.completions.create(model=model,messages=messages,response_format=response_format)
answer = response.choices[0].message.content
print(answer)

raw_json=answer
data_file=json.loads(raw_json)
ticket = Ticket(**data_file)

print(ticket.name)
print(ticket.email)
print(ticket.issue)