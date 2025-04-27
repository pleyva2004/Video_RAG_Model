from featurizationPipeline.chunking import quality_focused_chunking

from openai import OpenAI
from dotenv import load_dotenv
import os

load_dotenv()

client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))


print("Reading transcript...")
with open("./assets/eFgkZKhNUdM.txt", "r") as f:
    text = f.read()

print("Chunking...")
chunks = quality_focused_chunking(client, text)

for chunk in chunks:
    print(chunk)
    print("--------------------------------")