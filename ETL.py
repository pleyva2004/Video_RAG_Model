from dataPipeline import upload_to_mongoDB, getVttPaths, MongoRetrieve
from featurizationPipeline import upload_to_qdrant
def start():

    # Assume the data is already in the data/rawData folder
    print("Starting Data Pipeline...")
    upload_to_mongoDB()
    print("Data Pipeline completed successfully.")

    # Get the data from the MongoDB
    print("Getting data from MongoDB...")
    data = MongoRetrieve()
    print("Data retrieved successfully.")

    # Start Featurization Pipeline
    print("Starting Featurization Pipeline...")
    upload_to_qdrant()
    print("Featurization Pipeline completed successfully.")

