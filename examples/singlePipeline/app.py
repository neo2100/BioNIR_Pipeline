# define defferent piplines and connect them to evaluators and run tests.

# A minimum pipeline is including: a documentRetrieval, a sentenceSplitting, an embedding, and a ranking pipe

from bionir_pipeline import Pipeline

pipeline = Pipeline()

# NOTE: while pushing pipes, the order is important
#pipeline.push("PubMedSimpleSearch as documentRetrieval", {'maxDocumentNumber': 2})
pipeline.push("PubMedAdvancedSearch as documentRetrieval", {'maxAroundDocumentNumber': 500,'fetchMaxDocumentNumber':2})
#pipeline.push("SentenceSplittingByNLTK as preprocessing", {})
#pipeline.push("SBERT as embedding", {
#              'modelName': "sentence-transformers/multi-qa-mpnet-base-cos-v1"})
#pipeline.push("VectorSimilarity as ranking", {
#              'metricName': "dot-product", 'maxDocumentNumber': 2, 'maxSnippetNumber': 10})

#print(pipeline.execute({'query': "Covid in Iran"}))
output = pipeline.execute({'query': "What is the function of lncRNA?"})
#print(output)
#for snippet in output['rankedSnippets']:
#    print("score: " + str(snippet["score"]) + ", id: " + str(snippet["id"]) + ", snippet: " + snippet['snippet'])
