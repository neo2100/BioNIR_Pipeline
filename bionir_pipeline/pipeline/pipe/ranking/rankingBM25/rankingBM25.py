# Input: query, and max number of documents
# Output: a list of documents containing:
## id, directLink, type, text


from .localBM25 import LocalBM25


class RankingBM25:

    def __init__(self, parameters):
        # some prepartion
        if 'maxDocumentNumber' in parameters:
            self.maxDocumentNumber = parameters['maxDocumentNumber']
        else:
            self.maxDocumentNumber = 10
            print(
                "WARNING: no maxDocumentNumber is provided for LocalBM25. (default value = 10)")

        self.BM25Model = LocalBM25()
        print("Info: RankingBM25 as ranking has been initialized")

    def execute(self, input):
        if 'query' in input:
            self.query = input['query']
        else:
            print("ERROR: query is missing in the input for RankingBM25")
            return input
        if 'documents' not in input:
            print("ERROR: documents is missing in the input for RankingBM25")
            return input

        if input['documents'].__len__() == 0:
            print("WARNING: no document found in the documents for RankingBM25")
            return input

        rankedDocuments = self.BM25Model.rankDocuments(
            self.query, input['documents'])
        # sort documents based on ranking scores
        input['rankedDocuments'] = [next(document['directLink'] for document in input['documents'] if document["id"]
                                   == rankedDocuments[x][0]) for x in range(0, min(self.maxDocumentNumber, rankedDocuments.__len__()))]
        return input
