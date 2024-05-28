import re
import json
from groq import Groq

# Load API key from config.json
with open("config.json", "r") as file:
    config = json.load(file)

GROQ_API_KEY = config["GROQ_API_KEY"]

client = Groq(api_key=GROQ_API_KEY)

def generate_summary(prompt, model_name):
    chat_completion = client.chat.completions.create(
        messages=[{"role": "user", "content": prompt}],
        model=model_name,
    )
    summary = chat_completion.choices[0].message.content
    return re.sub(r"Here is a concise summary of the text: ", "", summary)
