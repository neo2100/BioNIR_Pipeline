# Preprocessing class is to define which preprocessing pipes we want to put together

from .sentenceSplittingByNLTK.sentenceSplittingByNLTK import SentenceSplittingByNLTK
from .abbreviationResolverByKGen.abbreviationResolverByKGen import AbbreviationResolverByKGen

class Preprocessing:

    def __init__(self, preprocessingType, paramaters):
        self.preprocessingType = preprocessingType
        if preprocessingType == "SentenceSplittingByNLTK":
            self.preprocessingPipe = SentenceSplittingByNLTK(paramaters)
        elif preprocessingType == "AbbreviationResolverByKGen":
            self.preprocessingPipe = AbbreviationResolverByKGen(paramaters)

    def execute(self, input):
        return self.preprocessingPipe.execute(input)