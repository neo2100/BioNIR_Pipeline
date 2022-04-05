#from sys import path

#path.insert(0, '../')
#from bionir_pipeline.common.stanfordcorenlp.corenlpwrapper import CoreNLPWrapper

class CorefResolver:

    __contents = ''

    def __init__(self, annotated):
        # Modified by Neo2100, extract coreNLP for perforamnce
        self.annotated = annotated

    def resolve(self, verbose=False):
        if verbose:
            print('Resolving coreferences - please wait, as it may take a while ...')
        return self.__stanford_coref(verbose)

    def __stanford_coref(self, verbose=False):
        if verbose:
            print('Using Stanford corefs')

        # Modified by Neo2100, extract coreNLP for perforamnce
        # nlp = CoreNLPWrapper()
        # annotated = nlp.annotate(self.__contents, properties={'annotators': 'tokenize, ssplit, pos, lemma, ner, parse, coref', 'coref.algorithm': 'neural', 'coref.neural.greedyness': '0.51'})

        return self.__rebuild_contents(self.annotated['sentences'], self.__eval_corefs(self.annotated['corefs'], verbose))

    def __eval_corefs(self, json_corefs, verbose=False):
        corefs = {}

        for k, chain in json_corefs.items():
            if len(chain) > 1:
                if verbose:
                    print('Chain key: {}'.format(k))

                for r in chain:
                    if r['isRepresentativeMention']:
                        if verbose:
                            print('- Representative: {} - {}[{} {}]'.format(r['text'], r['sentNum'], r['startIndex'], r['endIndex']))

                        representative = r['text']

                for m in chain:
                    if not m['isRepresentativeMention']:
                        if verbose:
                            print('-- mention: {} - {}[{} {}]'.format(m['text'], m['sentNum'], m['startIndex'], m['endIndex']))

                        corefs['{}:{},{}'.format(m['sentNum'], m['startIndex'], m['endIndex'])] = representative.strip()

        return corefs

    def __replace(self, s_index, token, corefs):
        t_index = token['index']

        for key in corefs.keys():
            if key.startswith(str(s_index) + ':'):
                s, coref_range = key.strip().split(':', 1)
                coref_range_start, coref_range_end = coref_range.strip().split(',', 1)

                if t_index in range(int(coref_range_start), int(coref_range_end)):

                    if t_index == int(coref_range_start):
                        return corefs[key]

                    return ''

        return None

    def __rebuild_contents(self, json_sentences, corefs):
        resolved = ''
        s_index = 0
        for sentences in json_sentences:
            s_index += 1
            for token in sentences['tokens']:
                replacement = self.__replace(s_index, token, corefs)

                if replacement is None:
                    resolved += token['originalText'] + ' '
                elif not replacement is '':
                    # Modified by Neo2100, extract coreNLP for perforamnce (keep changes in annotated)
                    token['originalText'] = replacement
                    resolved += replacement + ' '

        return resolved

