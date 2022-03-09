# Input : a list of "documents" at least containing: "sentencesEmbedded"
# Input : "queryEmbedded"
# Output: a list of "rankedDocuments" at least containing: "score", "id", "text", "directLink" and "type"
# Output: a list of "rankedSnippets" at least containing: "score", "id", "text", "snippet", "directLink" and "type"

from .vectorSimilarity.vectorSimilarity import VectorSimilarity

class Ranking:

    def __init__(self, rankingType, paramaters):
        self.rankingType = rankingType
        if rankingType == "VectorSimilarity":
            self.rankingPipe = VectorSimilarity(paramaters)

    def execute(self, input):
        return self.rankingPipe.execute(input)