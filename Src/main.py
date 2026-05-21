import os
from openai import AzureOpenAI
from dotenv import load_dotenv
from db import tables, InsertingData,getting_username_password,delting_eveything
from transformers import AutoModelForSequenceClassification, AutoTokenizer, pipeline

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

prompt = "I am going to the  paris"

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
    if call == "injection":
        print("Donot try to be smart ass")
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