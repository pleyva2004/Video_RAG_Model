from mongoFunctions import MongoRetrieve

def retrieveTranscripts():
    transcripts = {}
    data = MongoRetrieve()
    for d in data:
        transcripts[d['video_name']] = d['transcript']
    return transcripts

