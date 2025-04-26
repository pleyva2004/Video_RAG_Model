from getQuery import getQuery
#from searchQdrant import enhance_search_and_rerank
from llmEngineering.enhance import enhanceQuery


raw_user_query = getQuery()

enhanced_queries = enhanceQuery(raw_user_query)
print('enhanced queries')
print(enhanced_queries)

primary_query_text = enhanced_queries[0]  # Use the first enhanced query for reranking
print()
print('primary query')
print(primary_query_text)

'''
results = enhance_search_and_rerank(raw_user_query, collection_name="your_collection", top_k=20, threshold=0.7)

if results is not None:
    for result in results:
        print(f"Object ID: {result['object_id']}")
        print(f"Score: {result['score']}")
        print(f"Payload: {result['payload']}")
        print("------------------------")
'''
