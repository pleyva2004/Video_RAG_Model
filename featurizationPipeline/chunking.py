from openai import OpenAI


def suggest_contextual_breaks(client, text, model="gpt-4-turbo"):

    prompt = f"""
You are an expert at structuring lecture transcripts for semantic retrieval.

Given the following transcription (with no punctuation), 
identify natural points where a conceptual shift occurs — **where one rich idea is completed and a new one begins**.

- Prioritize **depth and semantic coherence**.
- **Do not** split mechanically by size.
- Chunks can vary in length — that's okay.
- Your goal is to create **the richest, most coherent idea chunks** possible.
- Return the character indices **at which the text should be split**.

Raw Text:
{text}

Respond ONLY with a list of integer indices, like: [500, 980, 1543]
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
    output = output.replace('[', '').replace(']', '').split(',')
    split_indices = [int(idx.strip()) for idx in output if idx.strip().isdigit()]
    
    return split_indices

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
    for segment_dict in segments:
        num_words = len(segment_dict['segment'].split())
        start_time = timestamps[timestamps_index]['time']
        timestamps_index += num_words - 1
        end_time = timestamps[timestamps_index]['time']
        timestamps_index += 1
        timestamp_list.append((start_time, end_time))
                                     
    return timestamp_list

def quality_focused_chunking(client, text, input_window=4000, overlap_fraction=0.2,):
    """
    Full quality-focused chunking pipeline.
    """
    chunks = []
    start = 0

    while start < len(text):
        window = text[start:start + input_window]

        # LLM suggests natural splits
        split_points = suggest_contextual_breaks(client, window)

        prev_idx = 0
        for idx in split_points:
            chunk = window[prev_idx:idx].strip()
            fixed_chunk = fix_end_of_chunk(chunk, text)
            if fixed_chunk:
                chunks.append(fixed_chunk)
            prev_idx = idx

        # Move to next window
        start += input_window

    with open("chunks_non_overlapped.txt", "w") as f:
        for chunk in chunks:
            f.write(chunk + "\n")

    # Get timestamps
    timestamps = getTimestamps(chunks, timestamps)

    # Overlap chunks
    overlapped_chunks = apply_overlap(chunks, overlap_fraction)

    return overlapped_chunks, timestamps
