# Input:  a list of "documents" at least containing: "text"
# Output: a list of "documents" at least containing: "text" + "annotated"

from bionir_pipeline.common.stanfordcorenlp.corenlpwrapper import CoreNLPWrapper

class CoreNLPAnnotator:

    def __init__(self, parameters):
        # some prepartion
        # properties
        if 'properties' in parameters:
            self.properties = parameters['properties']
        else:
            self.properties = {'annotators': 'tokenize, ssplit, pos, lemma, ner, parse, coref', 'coref.algorithm': 'neural', 'coref.neural.greedyness': '0.51'}
            print(
                "WARNING: no properties is provided for CoreNLPAnnotator. (default value = {'annotators': 'tokenize, ssplit, pos, lemma, ner, parse, coref', 'coref.algorithm': 'neural', 'coref.neural.greedyness': '0.51'})")

        print("Info: CoreNLPAnnotator has been initialized")

    def execute(self, input):
        if not 'documents' in input:
            print("ERROR: documents is missing in the input for CoreNLPAnnotator")
            return input
        
        nlp = CoreNLPWrapper()
        for document in input['documents']:
            document['annotated'] = nlp.annotate(document['text'], properties=self.properties)

        return input
