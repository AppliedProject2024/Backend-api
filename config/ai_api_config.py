from openai import OpenAI
import os

#initialise OpenAI client
client = OpenAI(
    #set API key from environment variable
    api_key = os.getenv("OPENAI_API_KEY")
)

#function to call OpenAI API
def Ai_call_api(prompt):
    try:
        #send prompt to OpenAI API using o3-mini model
        response = client.chat.completions.create(
            model="o3-mini",
            #set prompt and role
            messages=[{"role": "system", "content": prompt}],
        )
        #return response
        return response.choices[0].message.content
    except Exception as e:
        print(f"error: {e}")
        return "error"