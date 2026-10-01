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
prompt1="hi!"
prompt2="explain time travel in detail"
prompt3="write a 100 words essay on machine learning"

prompts=[prompt1,prompt2,prompt3]

for prompt in prompts:
    message = {
    "role":role,
    "content":prompt
    }
    messages = [message]
    response=client.chat.completions.create(model=model,messages=messages,max_tokens=2000)
    usage=response.usage
    print(f"prompt : {prompt} ---> your tokens :{usage.prompt_tokens}  -->completions tokens :{usage.completion_tokens} --> total token : {usage.total_tokens} finish reasons : {response.choices[0].finish_reason}")


#message = {
#    "role":role,
#    "content":prompt
#}

#messages = [message]

#response=client.chat.completions.create(model=model,messages=messages)

#print(response)

#print('#######################################')

#answer = response.choices[0].message.content
#print(answer)