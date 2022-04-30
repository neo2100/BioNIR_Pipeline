# Input : a list of "documents" at least containing: "sentencesEmbedded"
# Input : "queryEmbedded"
# Output: a list of "rankedDocuments" at least containing: "score", "id", "text", "directLink" and "type"
# Output: a list of "rankedSnippets" at least containing: "score", "id", "text", "snippet", "directLink" and "type"

from .vectorSimilarity.vectorSimilarity import VectorSimilarity
from .rankingBM25.rankingBM25 import RankingBM25
from .sentencesScored.sentencesScored import SentencesScored
from .hybridScore.hybridScore import HybridScore

class Ranking:

    def __init__(self, rankingType, paramaters):
        self.rankingType = rankingType
        if rankingType == "VectorSimilarity":
            self.rankingPipe = VectorSimilarity(paramaters)
        elif rankingType == "RankingBM25":
            self.rankingPipe = RankingBM25(paramaters)
        elif rankingType == "SentencesScored":
            self.rankingPipe = SentencesScored(paramaters)
        elif rankingType == "HybridScore":
            self.rankingPipe = HybridScore(paramaters)

    def execute(self, input):
        return self.rankingPipe.execute(input)