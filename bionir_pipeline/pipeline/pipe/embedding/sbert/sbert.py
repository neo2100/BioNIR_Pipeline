# Parameters: modelName -> the name of SBERT model to be usesd
# Input:  a query and a list of "documents" at least containing: "sentences"
# Output: a list of "documents" at least containing: "sentences" and "sentencesEmbedded"
# Output: "query" and "queryEmbedded"

# INFO: for more infor about the models: https://www.sbert.net/docs/pretrained_models.html

from sentence_transformers import SentenceTransformer

class SBERT:

    def __init__(self, parameters):
        # some prepartion
        if 'modelName' in parameters:
            self.modelName = parameters['modelName']
        else:
            self.modelName = "sentence-transformers/multi-qa-mpnet-base-cos-v1"
            print("WARNING: no modelName is provided for SBERT. (default value = sentence-transformers/multi-qa-mpnet-base-cos-v1)")

        self.model = SentenceTransformer(self.modelName)    
        print("Info: SBERT as embedding has been initialized")

    def execute(self, input):
        if not 'query' in input:
            print("ERROR: query is missing in the input for SBERT")
            return input

        input['queryEmbedded'] = self.model.encode(input['query'])

        if not 'documents' in input:
            print("ERROR: dpcuments is missing in the input for SBERT")
            return input

        for document in input['documents']:
            if not 'sentences' in document:
                print("ERROR: sentences is missing in a document in documents for SBERT")
                return input

            document['sentencesEmbedded'] = self.model.encode(document['sentences'])

        return input


    #def refineDocuments(self):
