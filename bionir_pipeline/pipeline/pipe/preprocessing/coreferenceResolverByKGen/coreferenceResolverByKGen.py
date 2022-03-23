# Input:  a list of "documents" at least containing: "text"
# Output: a list of "documents" at least containing: "text"

from .corefresolver import CorefResolver

class CoreferenceResolverByKGen:

    def __init__(self, parameters):
        # some prepartion
        # no parameter is needed
        print("Info: CoreferenceResolver By KGen has been initialized")

    def execute(self, input):
        if not 'documents' in input:
            print("ERROR: documents is missing in the input for CoreferenceResolverByKGen")
            return input
        
        for document in input['documents']:
            document['text'] = CorefResolver(document['text']).resolve()

        return input


    #def refineDocuments(self):
