# define defferent piplines and connect them to evaluators and run tests.

# A minimum pipeline is including: a documentRetrieval, a sentenceSplitting, an embedding, and a ranking pipe

from bionir_pipeline import Pipeline

pipeline = Pipeline()

# NOTE: while pushing pipes, the order is important
pipeline.push("PubMed as documentRetrieval", {'maxDocumentNumber': 1})
pipeline.push("SentenceSplittingByNLTK as preprocessing", {})
pipeline.push("SBERT as embedding", {
              'modelName': "sentence-transformers/multi-qa-mpnet-base-cos-v1"})

print(pipeline.execute({'query': "Covid in Iran"}))
