
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
            if chunk:
                chunks.append(chunk)
            prev_idx = idx

        # Move to next window
        start += input_window

    # Overlap chunks
    overlapped_chunks = []
    for i in range(len(chunks)):
        chunk = chunks[i]
        if i > 0:
            prev_chunk = chunks[i-1]
            overlap_size = int(len(prev_chunk) * overlap_fraction)
            overlap_text = prev_chunk[-overlap_size:]
            chunk = overlap_text + chunk
        overlapped_chunks.append(chunk)

    return chunks
