from extractName import extractName
from getText import getTimestamps, getTranscript
from getVttPaths import getVttPaths
from writeText import writeTimestamps, writeTranscript, writeTimestampedSegments
from augmentSegments import timestampSegments, addVideoToSegments
from segmentText import segmentText
from mongoFunctions import MongoInsert, MongoRetrieve, MongoDeleteAll

vtt_paths = getVttPaths()

for vtt_path in vtt_paths:
    timestamps = getTimestamps(vtt_path)
    transcript = getTranscript(timestamps)
    
    video_name = extractName(vtt_path)

    # if video_name != 'eQ6UE968Xe4':
    #     continue

    text_segments = segmentText(transcript)
    # print(text_segments)
    timestamped_segments = timestampSegments(text_segments, timestamps)
    finalized_segments = addVideoToSegments(video_name, timestamped_segments)

    MongoInsert(timestamped_segments)

    timestamped_segments_path = 'data/timestampedSegments/' + video_name + '.txt'
    writeTimestampedSegments(timestamped_segments, timestamped_segments_path)
    '''
    timestamp_path = 'data/timestamps/' + video_name + '.txt'
    writeTimestamps(timestamps, timestamp_path)

    transcript_path = 'data/transcripts/' + video_name + '.txt'
    writeTranscript(timestamps, transcript_path)
    '''

print('from mongo:')
data = MongoRetrieve()
for d in data:
    print(d)

print('deleting...')
MongoDeleteAll()

print('verifying deleted:')
data = MongoRetrieve()
for d in data:
    print(d)
