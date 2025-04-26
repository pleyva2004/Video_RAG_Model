from extractName import extractName
from getText import getTimestamps, getTranscript
from getVttPaths import getVttPaths
from createSegment import createSegment
from mongoFunctions import MongoInsert, MongoRetrieve, MongoDeleteAll

segments = []

vtt_paths = getVttPaths()

for vtt_path in vtt_paths:
    timestamps = getTimestamps(vtt_path)
    transcript = getTranscript(timestamps)
    
    video_name = extractName(vtt_path)

    segment = createSegment(transcript, timestamps, video_name)
    segments.append(segment)

MongoInsert(segments)

'''
print('from mongo:')
data = MongoRetrieve()
for d in data:
    print()
    print(d['video_name'])
    print(d['transcript'][:100])
    print(d['timestamps'][:100])

print('deleting...')
MongoDeleteAll()

print('verifying deleted:')
data = MongoRetrieve()
for d in data:
    print('here')
print('bye')
'''
