import os
import requests
import openai
import json
from dotenv import load_dotenv


def segmentText(transcript):
    return temp # at bottom of file
    
    print('creating segments')

    segments = []

    api_token = createAPIToken()

    words = transcript.split()
    num_words = len(words)
    leftover_response = {'summary': '', 'segment': ''}
    i = 0

    while i < num_words:
        curr_text = leftover_response['segment']
        word_count = len(leftover_response['segment'].split())

        while i < num_words and word_count < 1500:
            curr_text += (' ' if curr_text else '') + words[i]
            i += 1
            word_count += 1

        llm_response = callLLM(api_token, curr_text)

        if i < num_words:
            leftover_response = llm_response.pop()

        segments += llm_response
    
    return segments

def createAPIToken():
    load_dotenv()  # Load .env environment variables
    api_token = os.getenv("HUGGINGFACE_API_TOKEN")  # Add your Hugging Face token to your .env
    # api_token = "copy_api_token_here"
    return api_token  # The "client" here is just the token

def callLLM(api_token, transcript):
    API_URL = "https://api-inference.huggingface.co/models/google/flan-t5-base"
    headers = {
        "Authorization": f"Bearer {api_token}"
    }

    system_prompt = (
        "Segment the following text into semantically similar segments no more than 300 words each.\n"
        "Return your output as valid JSON.\n"
        "Specifically, return a list of dictionaries. Each dictionary must contain exactly two keys:\n"
        "1. 'summary' — a summary of the segment (maximum ten words).\n"
        "2. 'segment' — the segment text itself.\n"
        "Your entire response must be valid JSON without any extra text, explanations, comments, or formatting.\n"
        """Example:
        [
        {"summary": "Introduction", "segment": "This section introduces the problem..."},
        {"summary": "Explanation of methods", "segment": "Here we describe the methodology..."}
        ]"""
        "One segment must pick up from where the previous segment left off.\n"
        "The segments should not overlap each other.\n"
        "It is absolutely required that no segment contains more than 300 words. "
        "Under no circumstances may this limit be exceeded. If a segment is longer than 300 words, your response is invalid.\n"
        "Double-check your output. If any segment exceeds 300 words, start over.\n"
        "It is absolutely required that none of the input text is skipped. "
        "Under no circumstances may text be skipped. If text is skipped, your response is invalid.\n"
        "Double-check your output. If any text was skipped, start over.\n"
        "Do not modify the text other than segmenting it.\n"
        "Here is the text to segment:\n"
    )

    input_text = system_prompt + transcript

    payload = {"inputs": input_text}

    try:
        response = requests.post(API_URL, headers=headers, json=payload)
        response.raise_for_status()
        content = response.json()

        # Handle case where Hugging Face returns a dictionary with 'error'
        if isinstance(content, dict) and "error" in content:
            print(f"API returned an error: {content['error']}")
            return None

        # Flan-T5 will return a list of generated text outputs (string)
        generated_text = content[0]['generated_text']
        try:
            return json.loads(generated_text)
        except json.JSONDecodeError as decode_error:
            print("Failed to parse JSON. Here's the raw response:\n")
            print(generated_text)
            print(f"\nJSON error: {decode_error}")
            return None

    except requests.exceptions.RequestException as e:
        print(f"Error during Hugging Face API call: {e}")
        return None

'''
for Groq llama-3.3-70b-versatile
def createClient():
    load_dotenv()  # This loads variables from .env into the environment
    
    # Create a Groq client using OpenAI SDK
    client = openai.OpenAI(
        api_key=os.getenv("GROQ_API_KEY"),  # or replace with your key as a string
        base_url="https://api.groq.com/openai/v1"  # Groq's API endpoint
    )
    return client


def callLLM(client, transcript):
    system_prompt = (
        "You are an AI agent trained to semantically segment text.\n"
        "Return your output as valid JSON.\n"
        "Specifically, return a list of dictionaries. Each dictionary must contain exactly two keys:\n"
        "1. 'summary' — a summary of the segment (maximum ten words).\n"
        "2. 'segment' — the segment text itself.\n"
        "Your entire response must be valid JSON without any extra text, explanations, comments, or formatting.\n"
        "One segment must pick up from where the previous segment left off.\n"
        "The segments should not overlap each other.\n"
        "It is absolutely required that no segment contains more than 300 words. "
        "Under no circumstances may this limit be exceeded. If a segment is longer than 300 words, your response is invalid.\n"
        "Double-check your output. If any segment exceeds 300 words, start over.\n"
        "It is absolutely required that none of the input text is skipped. "
        "Under no circumstances may text be skipped. If text is skipped, your response is invalid.\n"
        "Double-check your output. If any text was skipped, start over.\n"
        "Do not modify the text other than segmenting it.\n"
    )

    try:
        response = client.chat.completions.create(
            model="llama-3.3-70b-versatile",  # Groq currently supports LLaMA 3 70B
            messages=[
                {"role": "system", "content": system_prompt},
                {"role": "user", "content": transcript}
            ],
            temperature=0.2
        )
        content = response.choices[0].message.content

        try:
            return json.loads(content)
        except json.JSONDecodeError as decode_error:
            print("Failed to parse JSON. Here's the raw response:\n")
            print(content)  # Print the response
            print(f"\nJSON error: {decode_error}")
            return None

    except Exception as e:
        print(f"Error during Groq API call: {e}")
        return None
'''
temp = [
    {
        "summary": "Classification task introduction",
        "segment": "we have seen earlier the regression problem where we have effectively to model a conditional probability distribution at the output of our predictor now we actually switching to a new task it's a classification task where again we will solve this task using The Vaping block diagram again we will need to model our predictor with a conditional probability distribution but in classification our Target variables are distinct and discrete random variables rather than continues"
    },
    {
        "summary": "Radar problem use case",
        "segment": "so in this kind of setting I'll motivate the classification task with a simple use case is actually going to be called the radar problem and we'll that's what we will start with next in this setting the use case the application we will see is a well-known application back in the Second World War the Battle of England was W primarily from the erection of these towers this was actually called the radar Towers whose job is was to transmit a signal towards the France where from France the Nazi airplanes were coming in to bomb London"
    },
    {
        "summary": "Radar system description",
        "segment": "and the every time that the this waveform was impinging into some large object on the sky like a plane it was returning back into what we call the radar receiver and there was kind of a human operator over there in on the on each kind of Tower with an access to a kind of a telephone device over there and every time that there was a strong return of a strong signal that was received in the radar kind of a receiver antenna it was he was calling London and millions of people were well the sirens were sounding and millions of people were actually running to the tubes stations to tube stations to save their lives"
    }
]
