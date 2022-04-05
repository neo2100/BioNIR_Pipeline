# Input:  a list of "documents" at least containing: "text", "annotated"
# Output: a list of "documents" at least containing: "text", "originalText"

from .abbrevresolver import AbbrevResolver


class AbbreviationResolverByKGen:

    def __init__(self, parameters):
        # some prepartion
        # no parameter is needed
        print("Info: AbbreviationResolver By KGen has been initialized")

    def execute(self, input):
        if not 'documents' in input:
            print(
                "ERROR: documents is missing in the input for AbbreviationResolverByKGen")
            return input

        for document in input['documents']:
            if not 'text' in document:
                print(
                    "ERROR: text is missing in a document in documents for AbbreviationResolverByKGen")
                return input
            if not 'annotated' in document:
                print(
                    "ERROR: annotated is missing in a document in documents for AbbreviationResolverByKGen")
                return input

            if not 'originalText' in document:
                document['originalText'] = document['text']

            document['text'] = AbbrevResolver(document['annotated']).resolve()

        return input

    # def refineDocuments(self):
