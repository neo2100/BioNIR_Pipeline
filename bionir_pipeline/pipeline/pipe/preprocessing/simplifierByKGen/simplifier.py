from sys import path

#path.insert(0, '../')
from bionir_pipeline.common.isimp.isimpwrapper import iSimpWrapper

class Simplifier:

    __contents_stack = None

    def __init__(self, sentences):
        # Modified by Neo2100 to give splitted sentences
        self.__contents_stack = sentences

    def simplify(self, verbose):
        simplified_contents = []

        isimp = iSimpWrapper()
        while len(self.__contents_stack) > 0:
            sentence = self.__contents_stack.pop()
            if verbose:
                print('- sentence: {}'.format(sentence))

            annotated = isimp.run_isimp(sentence, verbose)
            simplified_contents.insert(0, isimp.generate_simpler_sentences(annotated)) # insert at the beginning
        # Modified by Neo2100 to send back the seperated sentences
        return simplified_contents
