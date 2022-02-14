# BioNIR Pipline class 
# Pipline order:
# 1- documentRetrieval (PubMed APIs or BM25+DB)
# 2- preprocessing: (a- sentence splitting b- co-reference resolution 3- Abbreviation resolution 4- sentence simplification)
# 3- embedding (SBERT or BioASQ SBERT)
# 4- pooling (MEAN, MAX, or CLS hyper parameters)
# 5- ranking (sorting)


# define defferent piplines and connect them to evaluators and run tests.# Input: retrievalType (LocalBM25 or PubMed), query, and max number of documents
# Input: pipe types, query and max number of documents and ranked snippets
# Output: a list of ranked documents containing:
## id, directLink, type, text, rank, score

# NOTE: while pushing pipes, the order is important

from .pipe.pipe import Pipe

class Pipeline:

    def __init__(self):
        self.pipeline = {}

    def execute(self, input):
        for pipe in self.pipeline.items():
            output = pipe[1].execute(input)
            input = output
        return output

    def push(self, pipeName, parameters):
        self.pipeline[pipeName] = Pipe(pipeName, parameters)

    def pop(self, pipeName):
        self.pipeline.pop(pipeName)

    def clear(self):
        self.pipeline.clear()
