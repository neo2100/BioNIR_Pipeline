# Input: a list of 'documents' at least containing: 'sentences'
# Output: a list of documents containing:
## id, directLink, type, text

from .sbert.sbert import SBERT

class Embedding:

    def __init__(self, embeddingType, paramaters):
        self.embeddingType = embeddingType
        if embeddingType == "SBERT":
            self.embeddingPipe = SBERT(paramaters)

    def execute(self, input):
        return self.embeddingPipe.execute(input)