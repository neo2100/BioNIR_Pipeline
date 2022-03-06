# BioNIR Pipline class 
# Pipline order:
# 1- documentRetrieval (PubMed APIs or BM25+DB)
# 2- preprocessing: (a- sentence splitting b- co-reference resolution 3- Abbreviation resolution 4- sentence simplification)
# 3- embedding (SBERT or BioASQ SBERT)
# 4- pooling (MEAN, MAX, or CLS, hyper parameters)
# 5- ranking (vectorSimilarity)


# define defferent piplines and connect them to evaluators and run tests.# Input: retrievalType (LocalBM25 or PubMed), query, and max number of documents
# Input: pipe types, query and max number of documents and ranked snippets
# Output: a list of ranked documents containing:
## id, directLink, type, text, rank, score

from .documentRetrieval.documentRetrieval import DocumentRetrieval
from .preprocessing.preprocessing import Preprocessing
from .embedding.embedding import Embedding
from .ranking.ranking import Ranking

class Pipe:
    def __init__(self, pipeName, parameters):
        pipeType = pipeName.split(" as ")
        if len(pipeType) < 2:
            return print("ERROR: please use standard pipe names. eg., PubMed as documentRetrieval")
        
        if pipeType[1] == "documentRetrieval":
            self.pipe = DocumentRetrieval(pipeType[0], parameters)
        elif pipeType[1] == "preprocessing":
            self.pipe = Preprocessing(pipeType[0], parameters)
        elif pipeType[1] == "embedding":
            self.pipe = Embedding(pipeType[0], parameters)
        elif pipeType[1] == "ranking":
            self.pipe = Ranking(pipeType[0], parameters)

    def execute(self, input):
        return self.pipe.execute(input)

