# Input: a list of 'documents' at least containing: 'sentences'
# Output: a list of "documents" at least containing: "sentences" and "sentencesEmbedded"
# Output: "query" and "queryEmbedded"

from .sbert.sbert import SBERT
from .bioasqBert.bioasqBert import BioASQBERT
from .bioasqHead.bioasqHead import BioASQHead

class Embedding:

    def __init__(self, embeddingType, paramaters):
        self.embeddingType = embeddingType
        if embeddingType == "SBERT":
            self.embeddingPipe = SBERT(paramaters)
        elif embeddingType == "BioASQBERT":
            self.embeddingPipe = BioASQBERT(paramaters)
        elif embeddingType == "BioASQHead":
            self.embeddingPipe = BioASQHead(paramaters)

    def execute(self, input):
        return self.embeddingPipe.execute(input)