# Input:  a list of "documents" at least containing: "text"
# Output: a list of "documents" at least containing: "text" and ("sentences" or self.outputName)

from nltk.tokenize import sent_tokenize

class SentenceSplittingByNLTK:

    def __init__(self, parameters):
        # some prepartion
        # outputName
        if 'outputName' in parameters:
            self.outputName = parameters['outputName']
        else:
            self.outputName = 'sentences'
            print(
                "WARNING: no outputName is provided for CoreNLPAnnotator. (default value = 'sentences')")

        print("Info: SentenceSplitting By NLTK has been initialized")

    def execute(self, input):
        if not 'documents' in input:
            print("ERROR: documents is missing in the input for SentenceSplittingByNLTK")
            return input
        
        for document in input['documents']:
            document[self.outputName] = sent_tokenize(document['text'])

        return input


    #def refineDocuments(self):
