# This type is for any miscellaneous pipe that can be benefitial in any layer
# Input : any
# Output: any

from .snippetBeginEndOffset.snippetBeginEndOffset import SnippetBeginEndOffset

class Utility:

    def __init__(self, utilityType, paramaters):
        self.utilityType = utilityType
        if utilityType == "SnippetBeginEndOffset":
            self.utilityPipe = SnippetBeginEndOffset(paramaters)

    def execute(self, input):
        return self.utilityPipe.execute(input)