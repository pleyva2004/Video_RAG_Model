from openai import OpenAI


def suggest_contextual_breaks(client, text, model="gpt-4-turbo"):

    prompt = f"""
You are an expert at structuring educational lectures for retrieval.

Given an unpunctuated lecture transcript, segment it into natural, coherent chunks where each chunk covers exactly one major idea, concept explanation, or formula derivation.

Chunking Rules:
- Prefer semantic boundaries over fixed size.
- Avoid splitting mid-mathematical explanation.
- Allow chunk size to vary based on the depth of the idea.
- If possible, use natural transition cues like "now let's discuss," "moving on," "in general," "recall that."

Output:
- Split the text into numbered chunks,.
- Each chunk should contain a complete thought or derivation.

Text:
{text}

"""

    response = client.chat.completions.create(
        model=model,
        messages=[
            {"role": "system", "content": "You are a world-class transcript segmentation expert."},
            {"role": "user", "content": prompt}
        ],
        temperature=0
    )

    output = response.choices[0].message.content.strip()

    # Parse output
    # output = output.replace('[', '').replace(']', '').split(',')
    # split_indices = [int(idx.strip()) for idx in output if idx.strip().isdigit()]
    
    return output

def apply_overlap(chunks, overlap_fraction):

    overlapped_chunks = []
    for i in range(len(chunks)):
        chunk = chunks[i]
        if i > 0:
            prev_chunk = chunks[i-1]
            overlap_size = int(len(prev_chunk) * overlap_fraction)
            overlap_text = prev_chunk[-overlap_size:]
            # Move forward to the next space, so we don't start in the middle of a word
            while overlap_text and overlap_text[0] != " " and len(overlap_text) > 0:
                overlap_text = overlap_text[1:]
            chunk = overlap_text[1:] + chunk
        overlapped_chunks.append(chunk)
    return overlapped_chunks

def fix_end_of_chunk(chunk, text):
    if not chunk:  # Handle empty string case
        return chunk
        
    # If chunk doesn't end with a space, we're in the middle of a word
    # Find the next space to complete the word
    if chunk[-1] != " ":
        # Find the next space in the text after our current position
        next_space = text.find(" ", len(chunk))
        if next_space != -1:  # If we found a space
            # Take everything up to and including the space
            chunk = text[:next_space + 1]
        else:
            # If no space found, take the whole text
            chunk = text
            
    return chunk
    
def getTimestamps(segments, timestamps):
    timestamps_index = 0
    timestamp_list = []
    for segment in segments:
        num_words = len(segment.split())
        start_time = timestamps[timestamps_index][0]
        timestamps_index += num_words - 1
        end_time = timestamps[timestamps_index][0]
        timestamps_index += 1
        timestamp_list.append((start_time, end_time))
                                     
    return timestamp_list

def quality_focused_chunking(client, text, timestamps, j):
    """
    Full quality-focused chunking pipeline.
    """
    return_chunks = []
    start = 0

    chunks = suggest_contextual_breaks(client, text).split("\n")

    for chunk in chunks:
        print(chunk)
        print(100*'-')
        if chunk == "":
            chunks.remove(chunk)

    return_chunks = [chunks[i] for i in range(len(chunks)) if i % 2]
    # return_chunks = chunks

    with open(f"./assets/chunks/chunks_{j}.txt", "w") as f:
        for chunk in return_chunks:
            f.write(chunk + "\n")

    # Get timestamps
    timestamps = getTimestamps(return_chunks, timestamps)

    with open(f"./assets/chunk_timestamps/chunks_{j}_timestamped.txt", "w") as f:
        for i in range(len(return_chunks)):
            f.write(f"{timestamps[i][0]} - {timestamps[i][1]} : {return_chunks[i]}\n")

    # # Overlap chunks
    # overlapped_chunks = apply_overlap(chunks, overlap_fraction)

    return return_chunks, timestamps
