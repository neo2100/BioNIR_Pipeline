# define defferent piplines and connect them to evaluators and run tests.# Input: retrievalType (LocalBM25 or PubMed), query, and max number of documents
# Output: a list of documents containing:
## id, directLink, type, text

from bionir_pipeline import Pipeline

pipeline = Pipeline()

# NOTE: while pushing pipes, the order is important
pipeline.push("PubMed as documentRetrieval", {"maxDocumentNumber":1})

print(pipeline.execute({"query":"Covid in Iran"}))