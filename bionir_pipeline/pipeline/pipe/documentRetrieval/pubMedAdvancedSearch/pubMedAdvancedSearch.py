# Input: query, and max number of documents
# Output: a list of documents containing:
## id, directLink, type, text

import itertools
from .queryParser import QueryParser
from .fetchDocuments import fetchDocuments
from .fetchDocuments import getTotalResultsCount


class PubMedAdvancedSearch:

    def __init__(self, parameters):
        # some prepartion
        if 'maxAroundDocumentNumber' in parameters:
            self.maxAroundDocumentNumber = parameters['maxAroundDocumentNumber']
        else:
            self.maxAroundDocumentNumber = 100
            print(
                "WARNING: no maxAroundDocumentNumber is provided for PubMedAdvancedSearch. (default value = 100)")

        if 'fetchMaxDocumentNumber' in parameters:
            self.fetchMaxDocumentNumber = parameters['fetchMaxDocumentNumber']
        else:
            self.fetchMaxDocumentNumber = 1000
            print(
                "WARNING: no fetchMaxDocumentNumber is provided for PubMedAdvancedSearch. (default value = 1000)")

        self.queryParser = QueryParser()
        print("Info: PubMedAdvancedSearch as document retrieval has been initialized")

    def execute(self, input):
        if 'query' in input:
            self.query = input['query']
        else:
            print("ERROR: query is missing in the input for PubMedAdvancedSearch")
            self.query = ''
            return input

        bestQueryString = self.findBestQueryString()
        input['documents'] = fetchDocuments(
            bestQueryString, self.fetchMaxDocumentNumber)
        return input

    def findBestQueryString(self):
        queryRemovedStopWords = self.queryParser.removeStopWords(self.query)
        queryTokenized = self.queryParser.tokenizer(queryRemovedStopWords, False)
        # return IDFs and words in one dict
        inverseIndex = self.queryParser.inverseOfList(queryTokenized)
        # find all subsets and score them based on IDF average
        allSubsetsScore = {}
        for setSize in range(1, inverseIndex.__len__()+1):
            data = itertools.combinations(inverseIndex, setSize)
            subsets = set(data)
            for subset in subsets:
                score = 0
                for word in subset:
                    score = score + inverseIndex[word]
                score = score / setSize
                allSubsetsScore[subset] = score
        allSubsetsScoreSorted = sorted(
            allSubsetsScore, key=allSubsetsScore.get, reverse=True)
        # Find the first subset with total results count less than max and more than min
        bestQuery = self.query
        minTotalCount = 50000000
        for subset in allSubsetsScoreSorted:
            query = ""
            for word in subset:
                query = query + word + ' '
            totalCount = getTotalResultsCount(query)
            
            if totalCount == 0:
                continue
            if totalCount < self.maxAroundDocumentNumber:
                minTotalCount = totalCount
                bestQuery = query
                break
            if totalCount < minTotalCount:
                minTotalCount = totalCount
                bestQuery = query
                
        return bestQuery
