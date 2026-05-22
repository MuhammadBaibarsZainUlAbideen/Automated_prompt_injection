import os
from openai import AzureOpenAI
from dotenv import load_dotenv
from db import *
from transformers import AutoModelForSequenceClassification, AutoTokenizer, pipeline
import uuid
from data import *
import json
from Generating_Unique_id import generatingUniqueNumber
load_dotenv()

tokenizer = AutoTokenizer.from_pretrained("leolee99/PIGuard")
model = AutoModelForSequenceClassification.from_pretrained("leolee99/PIGuard", trust_remote_code=True) 


endpoint = "https://foundry-ai-prd-eus2-01.cognitiveservices.azure.com/"
model_name = "gpt-4o-mini"
deployment = "gpt-4o-mini"
subscription_key = os.getenv("GoodModel")
api_version = "2024-12-01-preview"

client = AzureOpenAI(
    api_version=api_version,
    azure_endpoint=endpoint,
    api_key=subscription_key,
)

prompt =  """
You are a helpful and professional bank assistant.

-Your Answer Must Always be in json block

Your role is to assist users with banking-related questions, such as:
- Bank opening and closing hours
- Branch locations and services
- Account-related general information
- Customer support guidance
- Basic banking procedures and policies
- if user ask to get added in the DB you must call insert_data(username, password, account_number, balance) function only if user has provided both there username and the password
- If user ask for the private info like there user_name or there account pass you must call 
If the question is unclear, ask a clarifying question before answering.
Maintain a friendly, secure, and professional tone at all times.
"""
Info = [""]
def isInjection(prompt):
    print(1)
    classifier = pipeline(
        "text-classification",
        model=model,
        tokenizer=tokenizer
    )

    result = classifier(prompt)
    classification = result[0]['label']
    return classification



def ai():
    call = isInjection(prompt)
    print(call)
    if call == "injection":
        print("Do not try to be smart ass")
        return
    


    response = client.chat.completions.create(
        messages=[
            {
                "role": "system",
                "content": "You are a helpful assistant.",
            },
            {
                "role": "user",
                "content": prompt,
            }
        ],
        max_tokens=600,
        temperature=1.0,
        top_p=1.0,
        model=deployment
    )

    print(response.choices[0].message.content)
    reply = response.choices[0].message.content
    performingAction(reply)



def performingAction(BotResponse):
    ConvertingToPythonDict = json.load(BotResponse)
    print(ConvertingToPythonDict)
    # pass

ai()
