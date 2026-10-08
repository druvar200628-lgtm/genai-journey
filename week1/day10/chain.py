import os
from pathlib import Path
from time import sleep
from dotenv import load_dotenv
from groq import Groq
import re

load_dotenv()
my_api_key=os.getenv("GROQ_API_KEY")

if not my_api_key:
    raise ValueError("API key kaha hai bhai")

client=Groq(api_key=my_api_key)
model="openai/gpt-oss-120b"

JD = """
We are hearing back end python developer.

Requirements:
- Strong python
-Fast api or DJango
-postgreSQL
- Docker
-aws
-REST API's
- 2+ years of experience
"""

RESUME ="""
name: Dhruva R

Experience:
3 years as a software developer.

Skills:
python, FastAPI , MySQL ,Docker,
REST APIs , Git

Projects:
Built of food delivery backend using fastapi And mysql.

Deployed applications using docker.

"""

def ask_llm(system_prompt,user_prompt):
    sys_msg = {
        "role":"system",
        "content": system_prompt
    }
    user_msg = {
        "role":"user",
        "content":user_prompt
    }
    messages=[user_msg,sys_msg]

    response=client.chat.completions.create(model=model,messages=messages)
    answer = response.choices[0].message.content
    return answer

def resume_extract():
    system_prompt=f"""
    You are a professional HR assisstant . extract the skill from the candidate resume provided.
    Only return the skills  no other information. Don not invent any skill yourself 
    """

    user_prompt=f"""
    Extract the skills from this resume
    {RESUME}
    """

    return ask_llm(system_prompt,user_prompt)

def JD_resume_extract():
    system_prompt=f"""
    You are a professional HR assisstant . extract the skill from the JOb description provided.
    Only return the skills  no other information. Don not invent any skill yourself 
    """

    user_prompt=f"""
    Extract the skills from this JD
    {JD}
    """

    return ask_llm(system_prompt,user_prompt)

def match(candidate,jd):
    system_prompt=f"""
    You are a professional HR assisstant.  compare the skills and skill required in the JD and produce a final score 
    between 1 and 100. also produce short verdict wheather the candidate is afir for the role 
    """
    user_prompt=f"""
    compare and match the skills

    JD:
    {jd}

    condidate:
    {candidate}
    """

    return ask_llm(system_prompt,user_prompt)

candidate = resume_extract()
sleep(2)
jd = JD_resume_extract()
sleep(2)
score = match(candidate,jd)

print(score)

