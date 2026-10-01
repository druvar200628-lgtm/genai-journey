import os
from pathlib import Path
from dotenv import load_dotenv
from groq import Groq

load_dotenv()

my_api_key=os.getenv("GROQ_API_KEY")

if not my_api_key:
    raise ValueError("api error")

client=Groq(api_key=my_api_key)
model="openai/gpt-oss-20b"

role="user"
prompt="suggest me the name for my cloth company"

message_sys = {
    "role":"system",
    "content":"you are my brand manager who suggest name for my food company. name should be in one word. suggest only one name"
}

message = {
    "role":role,
    "content":prompt
}

messages = [message_sys,message]

#temperature by default is zero meaning safe and range should be in o,2
response=client.chat.completions.create(model=model,messages=messages,temperature=0)

#print(response)

print('#######################################')

answer = response.choices[0].message.content
print(answer)