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
inputFileName = 'BioASQ-task10bPhaseA-testset1'


pipeline = Pipeline()

# NOTE: while pushing pipes, the order is important
pipeline.push("PubMedAdvancedSearch as documentRetrieval", {
              'maxAroundDocumentNumber': 500, 'fetchMaxDocumentNumber': 5000})
#pipeline.push("MiddleBM25 as documentRetrieval", {'maxDocumentNumber': 125})
#pipeline.push("SentenceSplittingByNLTK as preprocessing", {'outputName': 'originalSentences'})
#pipeline.push("CoreNLPAnnotator as preprocessing", {'properties':{'annotators': 'tokenize, ssplit, pos, lemma, ner, parse, coref', 'coref.algorithm': 'neural', 'coref.neural.greedyness': '0.51'}})
#pipeline.push("CoreferenceResolverByKGen as preprocessing", {})
#pipeline.push("AbbreviationResolverByKGen as preprocessing", {})
#pipeline.push("SentenceSplittingByNLTK as preprocessing", {'outputName': 'sentences'})
#pipeline.push("SBERT as embedding", {
#              'modelName': "sentence-transformers/multi-qa-mpnet-base-cos-v1"})
#pipeline.push("VectorSimilarity as ranking", {
#              'metricName': "dot-product", 'maxDocumentNumber': 10, 'maxSnippetNumber': 10})
#pipeline.push("SnippetBeginEndOffset as utility", {})
pipeline.push("RankingBM25 as ranking", {'maxDocumentNumber': 10})

# preparing inputs
questions = []
script_dir = os.path.dirname(__file__)  # <-- absolute dir the script is in
abs_file_path = os.path.join(script_dir, inputFileName)
with open(abs_file_path, 'rb') as document_file:
    questions = json.load(document_file)['questions']
    document_file.close()

# saving outputs in a file
script_dir = os.path.dirname(__file__)  # <-- absolute dir the script is in
abs_file_path = os.path.join(script_dir, (inputFileName+'_output_BM25_base'))

# executing pipeline and generate outputs
outputQuestions = []
for index in range(0,questions.__len__()):
    question = questions[index]
    print("starting pipeline for: ", index, question['body'])
    output = pipeline.execute({'query': question['body']})
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

    outputQuestions.append({
        'documents': documents,
        'snippets': snippets,
        'id': question['id'],
        'type': question['type'],
        'body': question['body'],
    })

    # saving outputs in a file    
    with open(abs_file_path, 'w', encoding='utf-8') as document_file:
        json.dump({'questions': outputQuestions},
                  document_file, ensure_ascii=False, indent=4)

# saving outputs in a file
# script_dir = os.path.dirname(__file__)  # <-- absolute dir the script is in
#abs_file_path = os.path.join(script_dir, (inputFileName+'_output'))
# with open(abs_file_path, 'w', encoding='utf-8') as document_file:
#    json.dump({'questions': outputQuestions},
#              document_file, ensure_ascii=False, indent=4)
