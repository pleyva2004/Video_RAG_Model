def writeTimestamps(timestamps, file_path):
    with open(file_path, 'w') as file:
        for timestamped_word in timestamps:
            file.write(f'{timestamped_word['time']} {timestamped_word['word']}\n')

def writeTranscript(timestamps, file_path):
    with open(file_path, 'w') as file:
        for timestamped_word in timestamps:
            file.write(f"{timestamped_word['word']} ")

def writeTimestampedSegments(timestamped_segments, file_path):
    with open(file_path, 'w') as file:
        for timestamped_segment in timestamped_segments:
            file.write(f"{timestamped_segment['start_time']} - {timestamped_segment['end_time']} | {timestamped_segment['summary']}\n"
                       f"{timestamped_segment['segment']}\n\n")
