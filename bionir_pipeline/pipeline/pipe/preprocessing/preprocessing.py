# Preprocessing class is to define which preprocessing pipes we want to put together

from .sentenceSplittingByNLTK.sentenceSplittingByNLTK import SentenceSplittingByNLTK

class Preprocessing:

    def __init__(self, preprocessingType, paramaters):
        self.preprocessingType = preprocessingType
        if preprocessingType == "SentenceSplittingByNLTK":
            self.preprocessingPipe = SentenceSplittingByNLTK(paramaters)

    def execute(self, input):
        return self.preprocessingPipe.execute(input)