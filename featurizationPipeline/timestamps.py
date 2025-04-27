

    
def getTimestamps(segments, timestamps):
    timestamped_segments = []
    timestamps_index = 0
    for segment_dict in segments:
        num_words = len(segment_dict['segment'].split())
        start_time = timestamps[timestamps_index]['time']
        timestamps_index += num_words - 1
        end_time = timestamps[timestamps_index]['time']
        timestamps_index += 1
        timestamped_segments.append({'segment': segment_dict['segment'], 'summary': segment_dict['summary'],
                                     'start_time': start_time, 'end_time': end_time})
                                     
    return timestamped_segments