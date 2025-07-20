from openai import OpenAI
from dotenv import load_dotenv
import os

load_dotenv()

client = OpenAI(
  api_key = os.getenv("OPENAI_API_KEY"),
  organization = os.getenv("OPENAI_ORG_ID"),
  project = os.getenv("OPENAI_PROJECT_ID"),
  timeout= 30,
)
model = "gpt-4.1"
role = open("prompt-draft.txt",'r').read()

def promt_llm(prompt=role,user_input="",model=model):  
  res = client.chat.completions.create(
      model=model,
      messages=[{'role':'system','content':prompt},
                  {"role": "user", "content":user_input}]
      )

  result = res.choices[0].message.content

  return(result)
