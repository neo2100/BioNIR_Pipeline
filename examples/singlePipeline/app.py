# define defferent piplines and connect them to evaluators and run tests.

# A minimum pipeline is including: a documentRetrieval, a sentenceSplitting, an embedding, and a ranking pipe

from bionir_pipeline import Pipeline

pipeline = Pipeline()

# NOTE: while pushing pipes, the order is important
#pipeline.push("PubMedSimpleSearch as documentRetrieval", {'maxDocumentNumber': 2})
pipeline.push("PubMedAdvancedSearch as documentRetrieval", {'maxAroundDocumentNumber': 500,'fetchMaxDocumentNumber':1500})
pipeline.push("MiddleBM25 as documentRetrieval", {'maxDocumentNumber': 100})
pipeline.push("SentenceSplittingByNLTK as preprocessing", {})
pipeline.push("SBERT as embedding", {
              'modelName': "sentence-transformers/multi-qa-mpnet-base-cos-v1"})
pipeline.push("VectorSimilarity as ranking", {
              'metricName': "dot-product", 'maxDocumentNumber': 10, 'maxSnippetNumber': 10})
pipeline.push("SnippetBeginEndOffset as utility", {})

#print(pipeline.execute({'query': "Covid in Iran"}))
output = pipeline.execute({'query': "Which factor is inhibited by Milvexian?"})
#print(output)
for snippet in output['rankedSnippets']:
    print("score: " + str(snippet["score"]) + ", id: " + str(snippet["id"]) + ", snippet: " + snippet['snippet']
     + ", offsetInBeginSection: " + str(snippet['offsetInBeginSection'])
      + ", offsetInEndSection: " + str(snippet['offsetInEndSection']))
print(output['rankedDocuments'])
