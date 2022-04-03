# Input : a list of "goldenQusetions" including documents and snippets
# Input : a list of "modelQusetions" including documents and snippets
# Output: evaluation including: precision,	recall,	f_measure,	map,	gmap

class BioasqTaskBPhaseA:

    def __init__(self, parameters):
        # parameters initialization
        print("Info: BioasqTaskBPhaseA as evaluation metric has been initialized")

    def execute(self, input):
        if not 'goldenQuestions' in input:
            print("ERROR: goldenQuestions is missing in the input for BioasqTaskBPhaseA")
            return input
        if not 'modelQuestions' in input:
            print("ERROR: modelQuestions is missing in the input for BioasqTaskBPhaseA")
            return input

        # calculate scores
        self.evaluation = {'documents': {'precision': 0, 'recall': 0, 'f_measure': 0, 'map': 0, 'gmap': 0},
                           'snippets': {'precision': 0, 'recall': 0, 'f_measure': 0, 'map': 0, 'gmap': 0}}

        meanPRF = self.meanPRFDocuments(
            input['goldenQuestions'], input['modelQuestions'])
        self.evaluation['documents']['precision'] = meanPRF['precision']
        self.evaluation['documents']['recall'] = meanPRF['recall']
        self.evaluation['documents']['f_measure'] = meanPRF['f_measure']

        meanPRF = self.meanPRFSnippets(
            input['goldenQuestions'], input['modelQuestions'])
        self.evaluation['snippets']['precision'] = meanPRF['precision']
        self.evaluation['snippets']['recall'] = meanPRF['recall']
        self.evaluation['snippets']['f_measure'] = meanPRF['f_measure']

        input['evaluation'] = self.evaluation
        return input

    def meanPRFDocuments(self, goldenQuestions, modelQuestions):
        totalPrecision = totalFMeasure = totalRecall = 0
        count = goldenQuestions.__len__()
        for index, goldenQuestion in enumerate(goldenQuestions):
            truePositives = falsePositives = falseNegative = 0
            for document in goldenQuestion['documents']:
                if document in modelQuestions[index]['documents']:
                    truePositives = truePositives + 1
                else:
                    falseNegative = falseNegative + 1
            for document in modelQuestions[index]['documents']:
                if document not in goldenQuestion['documents']:
                    falsePositives = falsePositives + 1

            precision = truePositives/(truePositives+falsePositives)
            recall = truePositives/(truePositives+falseNegative)
            if precision != 0:
                fMeasure = (2*precision*recall)/(precision+recall)
            else:
                fMeasure = 0
            totalPrecision += precision
            totalRecall += recall
            totalFMeasure += fMeasure

            #if recall==0:
            #    print(index, recall, goldenQuestion["body"])
            modelQuestions[index]['documentEvaluation'] = {'precision': precision, 'recall': recall, 'f_measure': fMeasure}

        return {'precision': (totalPrecision/count), 'recall': (totalRecall/count),
                'f_measure': (totalFMeasure/count)}

    def meanPRFSnippets(self, goldenQuestions, modelQuestions):
        totalPrecision = totalFMeasure = totalRecall = 0
        count = goldenQuestions.__len__()
        for index, goldenQuestion in enumerate(goldenQuestions):
            sameCharacterSize = modelCharacterSize = goldenCharacterSize = 0

            # golden size and same size
            for goldenSnippet in goldenQuestion['snippets']:
                goldenCharacterSize += len(goldenSnippet['text'])
                # same size
                for modelSnippet in modelQuestions[index]['snippets']:
                    if modelSnippet['beginSection'] == goldenSnippet['beginSection'] and modelSnippet['document'] == goldenSnippet['document']:
                        if 'offsetInBeginSection' in modelSnippet:
                            if modelSnippet['offsetInBeginSection']>goldenSnippet['offsetInBeginSection']:
                                sameSize = goldenSnippet['offsetInEndSection']-modelSnippet['offsetInBeginSection']
                            else:
                                sameSize = modelSnippet['offsetInEndSection']-goldenSnippet['offsetInBeginSection']
                            if sameSize> 0:
                                sameCharacterSize += sameSize
                        else: # if no offsetInBeginSection / risky evaluation just valid for basic model
                            if modelSnippet['text'] in goldenSnippet['text']:
                                sameCharacterSize += len(modelSnippet['text'])

                        # model size
            for snippet in modelQuestions[index]['snippets']:
                modelCharacterSize += len(snippet['text'])

            precision = sameCharacterSize/(modelCharacterSize)
            recall = sameCharacterSize/(goldenCharacterSize)

            if precision != 0:
                fMeasure = (2*precision*recall)/(precision+recall)
            else:
                fMeasure = 0
            totalPrecision += precision
            totalRecall += recall
            totalFMeasure += fMeasure

            #if recall==0:
            #    print(index,recall, goldenQuestion["body"])
            
            modelQuestions[index]['snippetEvaluation'] = {'precision': precision, 'recall': recall, 'f_measure': fMeasure}

        return {'precision': (totalPrecision/count), 'recall': (totalRecall/count),
                'f_measure': (totalFMeasure/count)}

    def rankDocumentsBasedOnRankedSnippets(self):
        rankedDocuments = []
        for snippet in self.allSnippets:
            if snippet['directLink'] not in rankedDocuments:
                rankedDocuments.append(snippet['directLink'])
        return rankedDocuments
