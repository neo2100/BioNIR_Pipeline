# Input: query, and max number of documents
# Output: a list of documents containing:
## id, directLink, type, text

from .fetchDocuments import fetchDocuments

class PubMedSimpleSearch:

    def __init__(self, parameters):
        # some prepartion
        if 'maxDocumentNumber' in parameters:
            self.maxDocumentNumber = parameters['maxDocumentNumber']
        else:
            self.maxDocumentNumber = 10
            print("WARNING: no maxDocumentNumber is provided for PubMedSimpleSearch. (default value = 10)")
            
        print("Info: PubMedSimpleSearch as document retrieval has been initialized")

    def execute(self, input):
        if 'query' in input:
            self.query = input['query']
        else:
            print("ERROR: query is missing in the input for PubMedSimpleSearch")
            self.query = ''
            return input

        input['documents'] = fetchDocuments(self.query, self.maxDocumentNumber)
        return input


    #def refineDocuments(self):
