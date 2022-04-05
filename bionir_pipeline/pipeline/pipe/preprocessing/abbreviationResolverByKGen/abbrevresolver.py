from nltk.tree import ParentedTree
#from sys import path

#path.insert(0, '../')
from bionir_pipeline.common.stanfordcorenlp.corenlpwrapper import CoreNLPWrapper

class AbbrevResolver:

    __contents = ''

    def __init__(self, annotated):
        # Modified by Neo2100, extract coreNLP for perforamnce
        self.annotated = annotated

    def resolve(self, verbose=False):
        if verbose:
            print('Looking for abbreviations and their occurences - please wait, as it may take a while ...')
        return self.__stanford_resolve_abbrevs(verbose)

    def __stanford_resolve_abbrevs(self, verbose=False):
        if verbose:
            print('Using Stanford parser')

        # Modified by Neo2100, extract coreNLP for perforamnce
        # nlp = CoreNLPWrapper()
        # annotated = nlp.annotate(self.__contents, properties={'annotators': 'tokenize, ssplit, pos, lemma, ner, parse'})

        abbrev_refs = {}
        for sentence in self.annotated['sentences']:
            parsed = sentence['parse'].replace('\n', '')
            parse_tree = ParentedTree.fromstring(parsed)
            for sub_tree in parse_tree.subtrees():
                if sub_tree.label() == 'PRN':
                    # Modified by Neo2100 as it doesn't work for several examples
                    if True:#sub_tree.parent().label() == 'NP' and sub_tree.left_sibling().label() == 'NP':
                        abbrev = ' '.join(sub_tree.leaves()).strip()
                        abbrev = abbrev[abbrev.find('-LRB-') + 5:abbrev.find('-RRB-')].strip()

                        left = sub_tree.left_sibling()
                        reference = ' '.join(left.leaves()).strip()

                        if verbose:
                            print('- {} : {}'.format(abbrev, reference))

                        abbrev_refs[abbrev] = reference
                        if abbrev.endswith('s') and reference.endswith('s'): #Referring to a plural abbreviation? Ouch!
                            abbrev_refs[abbrev[:-1]] = reference[:-1]

        resolved_contents = ''
        for sentence in self.annotated['sentences']:
            for token in sentence['tokens']:
                if token['word'] in abbrev_refs:
                    # Modified by Neo2100 to add abbreviation beside the resolved one
                    resolved_contents += abbrev_refs[token['word']] + ' ('+token['word']+') '
                else:
                    resolved_contents += token['originalText'] + ' '
        # Modified by Neo2100 to add abbreviation beside the resolved one
        for key in abbrev_refs:
            resolved_contents = resolved_contents.replace('{} ( {} ({}) )'.format(abbrev_refs[key], abbrev_refs[key], key), abbrev_refs[key]+ ' ('+key+')')

        return resolved_contents

