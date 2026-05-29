from dotenv import load_dotenv
import os
from openai import OpenAI
load_dotenv()
client = OpenAI()



response = client.responses.create(
    model="gpt-5.5",
    input="сколько кругов кровообращение у рыб"
)

print(response.output_text)