# Input: retrievalType (LocalBM25 or PubMed), query, and parameters: maxDocumentNumber
# Output: a list of documents containing:
## id, directLink, type, text

from .localBM25.localBM25 import LocalBM25
from .pubMed.pubMed import PubMed

class DocumentRetrieval:

    def __init__(self, retrievalType, paramaters):
        self.retrievalType = retrievalType
        if retrievalType == "LocalBM25":
            self.retrievalPipe = LocalBM25(paramaters)
        elif retrievalType == "PubMed":
            self.retrievalPipe = PubMed(paramaters)

    def execute(self, input):
        return self.retrievalPipe.execute(input)