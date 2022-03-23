# Input:  a list of "documents" at least containing: "text"
# Output: a list of "documents" at least containing: "text"

from .abbrevresolver import AbbrevResolver

class AbbreviationResolverByKGen:

    def __init__(self, parameters):
        # some prepartion
        # no parameter is needed
        print("Info: AbbreviationResolver By KGen has been initialized")

    def execute(self, input):
        if not 'documents' in input:
            print("ERROR: documents is missing in the input for AbbreviationResolverByKGen")
            return input
        
        for document in input['documents']:
            document['text'] = AbbrevResolver(document['text']).resolve()

        return input


    #def refineDocuments(self):
