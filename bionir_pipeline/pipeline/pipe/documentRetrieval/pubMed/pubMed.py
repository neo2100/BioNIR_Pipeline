# Input: query, and max number of documents
# Output: a list of documents containing:
## id, directLink, type, text

from .fetchDocuments import fetchDocuments

class PubMed:

    def __init__(self, parameters):
        # some prepartion
        if 'maxDocumentNumber' in parameters:
            self.maxDocumentNumber = parameters['maxDocumentNumber']
            print("Info: PubMed as document retrieval has been initialized")
        else:
            self.maxDocumentNumber = 10
            print("WARNING: no maxDocumentNumber is provided for PubMed. (default value = 10)")

    def execute(self, input):
        if 'query' in input:
            self.query = input['query']
        else:
            print("ERROR: query is missing in the input for PubMed")

        input['documents'] = fetchDocuments(self.query, self.maxDocumentNumber)
        return input


    #def refineDocuments(self):
