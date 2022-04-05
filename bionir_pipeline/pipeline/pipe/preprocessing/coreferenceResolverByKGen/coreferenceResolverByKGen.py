# Input:  a list of "documents" at least containing: "text", "annotated"
# Output: a list of "documents" at least containing: "text", "originalText"

from .corefresolver import CorefResolver


class CoreferenceResolverByKGen:

    def __init__(self, parameters):
        # some prepartion
        # no parameter is needed
        print("Info: CoreferenceResolver By KGen has been initialized")

    def execute(self, input):
        if not 'documents' in input:
            print(
                "ERROR: documents is missing in the input for CoreferenceResolverByKGen")
            return input

        for document in input['documents']:
            if not 'text' in document:
                print(
                    "ERROR: text is missing in a document in documents for CoreferenceResolverByKGen")
                return input
            if not 'annotated' in document:
                print(
                    "ERROR: annotated is missing in a document in documents for CoreferenceResolverByKGen")
                return input

            if not 'originalText' in document:
                document['originalText'] = document['text']

            document['text'] = CorefResolver(document['annotated']).resolve()

        return input

    # def refineDocuments(self):
