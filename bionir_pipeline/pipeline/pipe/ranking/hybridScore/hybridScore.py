# Parameters: metricName -> one of these: {"dot-product"}
# Input : a list of "documents" at least containing: "sentencesScored" and "sentences"
# Input : "queryEmbedded"
# Output: a list of "rankedDocuments" at least containing: "score", "id", "text", "directLink" and "type"
# Output: a list of "rankedSnippets" at least containing: "score", "id", "text", "snippet", "directLink" and "type"

class HybridScore:

    def __init__(self, parameters):
        # parameters initialization
        # metricName
        if 'metricName' in parameters:
            self.metricName = parameters['metricName']
        else:
            self.metricName = "dot-product"
            print(
                "WARNING: no metricName is provided for SentencesScored. (default value = dot-product)")
        # maxDocumentNumber
        if 'maxDocumentNumber' in parameters:
            self.maxDocumentNumber = parameters['maxDocumentNumber']
        else:
            self.maxDocumentNumber = 1
            print(
                "WARNING: no maxDocumentNumber is provided for SentencesScored. (default value = 1)")
        # maxDocumentNumber
        if 'alpha' in parameters:
            self.alpha = parameters['alpha']
        else:
            self.alpha = 1
            print(
                "WARNING: no alpha is provided for SentencesScored. (default value = 1)")
        # maxSnippetNumber
        if 'maxSnippetNumber' in parameters:
            self.maxSnippetNumber = parameters['maxSnippetNumber']
        else:
            self.maxSnippetNumber = 1
            print(
                "WARNING: no maxSnippetNumber is provided for SentencesScored. (default value = 1)")

        self.allSnippets = []
        #self.model = SentenceTransformer(self.modelName)
        print("Info: SentencesScored as rankning has been initialized")

    def execute(self, input):
        if not 'queryEmbedded' in input:
            print("ERROR: queryEmbedded is missing in the input for SentencesScored")
            return input
        if not 'documents' in input:
            print("ERROR: documents is missing in the input for SentencesScored")
            return input

        # make a list of all snippets and calculate the scores
        self.allSnippets = []
        for document in input['documents']:
            if not 'sentencesScored' in document:
                print(
                    "ERROR: sentencesScored is missing in a document in documents for SentencesScored")
                return input
            if not 'sentences' in document:
                print(
                    "ERROR: sentences is missing in a document in documents for SentencesScored")
                return input

            for index, sentenceScored in enumerate(document['sentencesScored']):
                if 'originalText' in document:
                    text = document['originalText']
                else:
                    text = document['text']

                if 'originalSentences' in document and document['originalSentences'].__len__() > index:
                    snippet = document['originalSentences'][index]
                else:
                    snippet = document['sentences'][index]

                self.allSnippets.append({
                    'score': self.dotProductSimilarity(input['queryEmbedded'], input['sentencesEmbedded'][index])+ sentenceScored*self.alpha,
                    'snippet': snippet,
                    'id': document['id'],
                    'text': text,
                    'directLink': document['directLink'],
                    'type': document['type'],
                })

        # sort the snippets
        self.allSnippets.sort(key=lambda x: x['score'], reverse=True)

        input['rankedSnippets'] = self.allSnippets[0:self.maxSnippetNumber]
        input['rankedDocuments'] = self.rankDocumentsBasedOnRankedSnippets()[0:self.maxDocumentNumber]

        return input

    def dotProductSimilarity(self, queryEmbedded, sentenceEmbedded):
        # a = numpy.dot(A,B) for Python before 3.5
        # a = A @ B for Python 3.5 and above
        score = queryEmbedded @ sentenceEmbedded
        return score

    def rankDocumentsBasedOnRankedSnippets(self):
        rankedDocuments = []
        for snippet in self.allSnippets[0:self.maxSnippetNumber]:
            if snippet['directLink'] not in rankedDocuments:
                rankedDocuments.append(snippet['directLink'])
        return rankedDocuments
