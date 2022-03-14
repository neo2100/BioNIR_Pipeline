# Input : a list of "rankedSnippets" at least containing: "text", "snippet"
# Input : "queryEmbedded"
# Output: a list of "rankedSnippets" at least containing: "offsetInBeginSection", "offsetInEndSection", "text", "snippet"

class SnippetBeginEndOffset:

    def __init__(self, parameters):
        # parameters initialization
        print("Info: SnippetBeginEndOffset as utility has been initialized")

    def execute(self, input):
        if not 'rankedSnippets' in input:
            print("ERROR: rankedSnippets is missing in the input for SnippetBeginEndOffset")
            return input

        # find offsets
        for snippet in input['rankedSnippets']:
            if not 'text' in snippet:
                print(
                    "ERROR: text is missing in a snippet in documents for SnippetBeginEndOffset")
                return input
            if not 'snippet' in snippet:
                print(
                    "ERROR: snippet is missing in a snippet in documents for SnippetBeginEndOffset")
                return input

            offsetInBeginSection = offsetInEndSection = 0
            offsetInBeginSection = snippet['text'].find(snippet['snippet'])
            offsetInEndSection = len(snippet['snippet']) + offsetInBeginSection

            snippet['offsetInBeginSection'] = offsetInBeginSection
            snippet['offsetInEndSection'] = offsetInEndSection

        return input

    