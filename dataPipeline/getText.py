import re

def getTimestamps(vtt_path):
    word_list = []

    with open(vtt_path, 'r', encoding='utf-8') as f:
        lines = f.readlines()
    
    first_word_time_pattern = re.compile(r'(\d{2}:\d{2}:\d{2}.\d{3}) -->')
    timestamp_pattern = re.compile(r'<(\d{2}:\d{2}:\d{2}.\d{3})><c>([^<]*)</c>')
    first_word_pattern = re.compile(r'^([^<]*)<')

    words_to_remove = ['um','uh']

    first_word_time = None
    prev_word = ''
    for line in lines:
        first_word_time_match = first_word_time_pattern.findall(line)
        if len(first_word_time_match) != 0:
            first_word_time = first_word_time_match[0]

        timestamp_matches = timestamp_pattern.findall(line)
        if len(timestamp_matches) != 0:
            first_word = first_word_pattern.findall(line)[0]

            first_word = first_word.strip()

            if first_word not in words_to_remove and first_word != prev_word:
                word_list.append({"time": first_word_time, "word": first_word})
                prev_word = first_word

            for time_str, word in timestamp_matches:
                word = word.strip()
                if word not in words_to_remove and word != prev_word:
                    word_list.append({"time": time_str, "word": word})
                    prev_word = word


    return word_list

def getTranscript(timestamps):
    transcript = ''
    for timestamped_word in timestamps:
        transcript += (' ' if transcript else '') + str(timestamped_word['word'])
    return transcript
