# Input: query, and max number of documents
# Output: a list of documents containing:
## id, directLink, type, text


class LocalBM25:

    def __init__(self, parameters):
        # some prepartion
        if 'maxDocumentNumber' in parameters:
            self.maxDocumentNumber = parameters['maxDocumentNumber']
        else:
            self.maxDocumentNumber = 10
            print("WARNING: no maxDocumentNumber is provided for LocalBM25. (default value = 10)")

    def execute(self, input):
        if 'query' in input:
            self.query = input['query']
        else:
            print("ERROR: query is missing in the input for LocalBM25")

        return [{'id':"asd", 'direcLink':"http://", 'type':"abstract", 'text':"something"}]