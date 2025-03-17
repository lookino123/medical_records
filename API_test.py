import os
import dotenv
import openai

dotenv.load_dotenv()

OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
OPENAI_ORG_ID = os.getenv("OPENAI_ORG_ID")  
CH_API_KEY = os.getenv("CH_API_KEY")

client = openai.OpenAI(api_key=OPENAI_API_KEY, organization=OPENAI_ORG_ID)

try:
    response = client.chat.completions.create(
        model="gpt-4o-mini",
        messages=[{"role": "system", "content": "Test API access"}]
    )
    print("API is working:", response)
except Exception as e:
    print("Error:", e)


try:
    l = client.models.list()
    for model in l:
        print(model.id)   
            
except openai.AuthenticationError:
    print("OpenAI API key is NOT valid.")
else:
    print("OpenAI API key is valid.")
