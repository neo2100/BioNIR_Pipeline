from nltk.tree import ParentedTree
#from sys import path

#path.insert(0, '../')
#from bionir_pipeline.common.stanfordcorenlp.corenlpwrapper import CoreNLPWrapper

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
                    if sub_tree.left_sibling() and sub_tree.parent():#sub_tree.parent().label() == 'NP' and sub_tree.left_sibling().label() == 'NP':
                        abbrev = ' '.join(sub_tree.leaves()).strip()
                        abbrev = abbrev[abbrev.find('-LRB-') + 5:abbrev.find('-RRB-')].strip()

                        # Modified by Neo2100
                        if abbrev.split().__len__()>1: # assume abbreviations are only one word
                            continue
                        reference = self.ruleBasedReferenceFinder(abbrev, sub_tree.parent().leaves())

                        #left = sub_tree.left_sibling()
                        #reference = ' '.join(left.leaves()).strip()

                        if verbose:
                            print('- {} : {}'.format(abbrev, reference))

                        abbrev_refs[abbrev] = reference
                        if abbrev.endswith('s') and reference.endswith('s'): #Referring to a plural abbreviation? Ouch!
                            abbrev_refs[abbrev[:-1]] = reference[:-1]
            
            # Modified by Neo2100, another way of finding abbrev to complete this method
            possibleReference = []
            for index, token in enumerate(sentence['tokens']):
                if sentence['tokens'].__len__() < index+2:
                    break
                possibleReference.append(token['originalText'])
                if token['word']== "(" and sentence['tokens'][index + 2]['word']==")":
                    abbrev = sentence['tokens'][index + 1]['word']

                    if abbrev in abbrev_refs: # check if already has catched it
                        continue
                    if abbrev.split().__len__()>1: # assume abbreviations are only one word
                        continue
                    
                    reference = self.ruleBasedReferenceFinder(abbrev, possibleReference)

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
                elif token['originalText'] in abbrev_refs:
                    # Modified by Neo2100 to condsider if original text have it
                    resolved_contents += abbrev_refs[token['originalText']] + ' ('+token['originalText']+') '
                else:
                    # Modified by Neo2100, prevent unnessacary space
                    if token['originalText'] in ["i.e.","al.","e.g."]:
                        resolved_contents += token['originalText'] 
                    else:
                        resolved_contents += token['originalText'] + ' '
        # Modified by Neo2100 to add abbreviation beside the resolved one
        for key in abbrev_refs:
            resolved_contents = resolved_contents.replace('{} ( {} ({}) )'.format(abbrev_refs[key], abbrev_refs[key], key), abbrev_refs[key]+ ' ('+key+')')

        return resolved_contents

    # Modified by Neo2100, assumed possibleReference is including parantese
    def ruleBasedReferenceFinder(self, abbrev, possibleReference):
        reference = []
        maxLength = len(abbrev)
        if abbrev.endswith('s'):
            maxLength = maxLength - 1
        
        acceptable = False
        while len(possibleReference) > 0:
            ref = possibleReference.pop()
            if ref in ["-LRB-", "("]:
                acceptable = True
                continue

            if acceptable:
                reference.insert(0, ref)
                maxLength = maxLength - 1
            
            if maxLength == 0:
                break

        return ' '.join(reference).strip()