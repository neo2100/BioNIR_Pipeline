# Input: retrievalType (LocalBM25 or PubMed), query, and parameters: maxDocumentNumber
# Output: a list of documents containing:
## id, directLink, type, text

from .middleBM25.middleBM25 import MiddleBM25
from .pubMedAdvancedSearch.pubMedAdvancedSearch import PubMedAdvancedSearch
from .pubMedSimpleSearch.pubMedSimpleSearch import PubMedSimpleSearch

class DocumentRetrieval:

    def __init__(self, retrievalType, paramaters):
        self.retrievalType = retrievalType
        if retrievalType == "MiddleBM25":
            self.retrievalPipe = MiddleBM25(paramaters)
        elif retrievalType == "PubMedAdvancedSearch":
            self.retrievalPipe = PubMedAdvancedSearch(paramaters)
        elif retrievalType == "PubMedSimpleSearch":
            self.retrievalPipe = PubMedSimpleSearch(paramaters)

    def execute(self, input):
        return self.retrievalPipe.execute(input)