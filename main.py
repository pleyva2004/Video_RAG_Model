from featurizationPipeline.chunking import quality_focused_chunking

from openai import OpenAI
from dotenv import load_dotenv
import os





def main():
    load_dotenv()
    client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))
    with open("./dataPipeline/data/transcripts/testONE.txt", "r") as f:
        text = f.read()
    chunks = quality_focused_chunking(client, text)
    for chunk in chunks:
        print(chunk)
        print("-"*100)



if __name__ == "__main__":
    main()