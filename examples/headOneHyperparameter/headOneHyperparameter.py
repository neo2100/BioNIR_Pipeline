# define defferent piplines and connect them to evaluators and run tests.
# A minimum pipeline is including: a documentRetrieval, a sentenceSplitting, an embedding, and a ranking pipe

# Bioasq-basic: maxAroundDocumentNumber': 500, 'fetchMaxDocumentNumber': 1500, 'maxDocumentNumber': 100
# Bioasq-basic-mid2: maxAroundDocumentNumber': 700, 'fetchMaxDocumentNumber': 2500, 'maxDocumentNumber': 200 (Test1)
# Bioasq-basic-mid3: maxAroundDocumentNumber': 700, 'fetchMaxDocumentNumber': 2500, 'maxDocumentNumber': 100
# Bioasq-basic-mid4: maxAroundDocumentNumber': 500, 'fetchMaxDocumentNumber': 1500, 'maxDocumentNumber': 50
# Bioasq-basic-mid5: maxAroundDocumentNumber': 500, 'fetchMaxDocumentNumber': 1500, 'maxDocumentNumber': 25
# Bioasq-basic-mid6: maxAroundDocumentNumber': 500, 'fetchMaxDocumentNumber': 1500, 'maxDocumentNumber': 75
# Bioasq-basic-mid7: maxAroundDocumentNumber': 500, 'fetchMaxDocumentNumber': 1500, 'maxDocumentNumber': 125 (Test2) (svectorSimilarity-> docs only from best 10 snippests)

from bionir_pipeline import Pipeline
import os
import json
inputFileName = 'BioASQ-task10bPhaseA-testset4'


pipeline = Pipeline()

# NOTE: while pushing pipes, the order is important
pipeline.push("PubMedAdvancedSearch as documentRetrieval", {
              'maxAroundDocumentNumber': 500, 'fetchMaxDocumentNumber': 5000})
pipeline.push("MiddleBM25 as documentRetrieval", {'maxDocumentNumber': 100})
pipeline.push("SentenceSplittingByNLTK as preprocessing", {'outputName': 'sentences'})
pipeline.push("BioASQHeadOne as embedding", { 'modelName': "bionirheadone_nn0_qu_Interval_10.pt"})
#pipeline.push("SentencesScored as ranking", {
#              'metricName': "dot-product", 'maxDocumentNumber': 10, 'maxSnippetNumber': 10})
#pipeline.push("VectorSimilarity as ranking", {
#              'metricName': "dot-product", 'maxDocumentNumber': 10, 'maxSnippetNumber': 10})
#pipeline.push("SnippetBeginEndOffset as utility", {})
#pipeline.push("RankingBM25 as ranking", {'maxDocumentNumber': 10})

# preparing inputs
questions = []
script_dir = os.path.dirname(__file__)  # <-- absolute dir the script is in
abs_file_path = os.path.join(script_dir, inputFileName)
with open(abs_file_path, 'rb') as document_file:
    questions = json.load(document_file)['questions']
    document_file.close()

# saving outputs in a file
script_dir = os.path.dirname(__file__)  # <-- absolute dir the script is in
abs_file_path = os.path.join(script_dir, (inputFileName+'_output_basic'))

# executing pipeline and generate outputs
outputOfQuestions = []
for index in range(0,questions.__len__()):
    question = questions[index]
    print("starting pipeline for: ", index, question['body'])
    output = pipeline.execute({'query': question['body']})

    outputOfQuestions.append({
        'queryEmbedded': question['queryEmbedded'],
        'sentencesEmbedded': question['sentencesEmbedded'],
        'sentencesScored': question['sentencesScored'],
        'id': question['id'],
        'type': question['type'],
        'body': question['body'],
    })

# evaluation per lambda

from bionir_pipeline import Evaluator
goldenFileName = 'BioASQ-task10bPhaseB-testset3'
goldenQuestions = {}
with open(os.path.join(script_dir, goldenFileName), 'rb') as document_file:
    goldenQuestions = json.load(document_file)['questions']

bioasqTaskBPhaseA = Evaluator("BioasqTaskBPhaseA as metric", {})

for alpha in range(0,1,0.01):
    pipeline2 = Pipeline()
    pipeline2.push("HybridScore as ranking", {
                  'metricName': "dot-product", 'maxDocumentNumber': 10, 'maxSnippetNumber': 10, 'alpha':alpha})
    pipeline2.push("SnippetBeginEndOffset as utility", {})

    modelQuestions = []
    for index in range(0,outputOfQuestions.__len__()):
        question = outputOfQuestions[index]
        #print("starting pipeline for: ", index, question['body'])
        output = pipeline2.execute({'queryEmbedded': question['queryEmbedded'],'sentencesEmbedded': question['sentencesEmbedded'],'sentencesScored': question['sentencesScored']})
        snippets = []
        if 'rankedSnippets' in output:
            for snippet in output['rankedSnippets']:
                snippets.append({
                    'beginSection': snippet['type'],
                    'endSection': snippet['type'],
                    'text': snippet['snippet'],
                    'document': snippet['directLink'],
                    'offsetInBeginSection': snippet['offsetInBeginSection'],
                    'offsetInEndSection': snippet['offsetInEndSection']
                })
        documents = []
        if 'rankedDocuments' in output:
            documents = output['rankedDocuments']

        modelQuestions.append({
            'documents': documents,
            'snippets': snippets,
            'id': question['id'],
            'type': question['type'],
            'body': question['body'],
        })


    output = bioasqTaskBPhaseA.execute(
        {'goldenQuestions': goldenQuestions, 'modelQuestions': modelQuestions})
    print(alpha, output['evaluation'])
# saving outputs in a file
# script_dir = os.path.dirname(__file__)  # <-- absolute dir the script is in
#abs_file_path = os.path.join(script_dir, (inputFileName+'_output'))
# with open(abs_file_path, 'w', encoding='utf-8') as document_file:
#    json.dump({'questions': outputQuestions},
#              document_file, ensure_ascii=False, indent=4)
