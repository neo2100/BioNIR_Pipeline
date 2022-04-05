# Input:  a list of "documents" at least containing: "sentences"
# Output: a list of "documents" at least containing: "text"

from .simplifier import Simplifier

class SimplifierByKGen:

    def __init__(self, parameters):
        # some prepartion
        # no parameter is needed
        print("Info: Simplifier By KGen has been initialized")

    def execute(self, input):
        if not 'documents' in input:
            print("ERROR: documents is missing in the input for SimplifierByKGen")
            return input
        
        for document in input['documents']:
            if not 'sentences' in document:
                print("ERROR: sentences is missing in a document in documents for SimplifierByKGen")
                return input

            document['originalSentences'] = document['sentences'] 
            document['sentences'] = Simplifier(document['sentences']).simplify()

        return input


    #def refineDocuments(self):
