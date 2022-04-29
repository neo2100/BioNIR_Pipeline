# define defferent piplines and connect them to evaluators and run tests.

# A minimum pipeline is including: a documentRetrieval, a sentenceSplitting, an embedding, and a ranking pipe

from bionir_pipeline import Pipeline

pipeline = Pipeline()

# NOTE: while pushing pipes, the order is important
#pipeline.push("PubMedSimpleSearch as documentRetrieval", {'maxDocumentNumber': 2})
pipeline.push("PubMedAdvancedSearch as documentRetrieval", {'maxAroundDocumentNumber': 500,'fetchMaxDocumentNumber':5000})
pipeline.push("MiddleBM25 as documentRetrieval", {'maxDocumentNumber': 100})
#pipeline.push("SentenceSplittingByNLTK as preprocessing", {'outputName': 'originalSentences'})
#pipeline.push("CoreNLPAnnotator as preprocessing", {'properties':{'annotators': 'tokenize, ssplit, pos, lemma, ner, parse, coref', 'coref.algorithm': 'neural', 'coref.neural.greedyness': '0.51'}})
#pipeline.push("CoreferenceResolverByKGen as preprocessing", {})
#pipeline.push("AbbreviationResolverByKGen as preprocessing", {})
pipeline.push("SentenceSplittingByNLTK as preprocessing", {'outputName': 'sentences'})
#pipeline.push("SBERT as embedding", {
#              'modelName': "sentence-transformers/multi-qa-mpnet-base-cos-v1"})

#pipeline.push("BioASQHead as embedding", { 'modelName': "bionirhead_nn0_qu_Interval_10.pt"})
pipeline.push("BioASQHeadOne as embedding", { 'modelName': "bionirheadone_nn0_qu_Interval_10.pt"})
pipeline.push("SentencesScored as ranking", {
              'metricName': "dot-product", 'maxDocumentNumber': 10, 'maxSnippetNumber': 10})
#pipeline.push("VectorSimilarity as ranking", {
#              'metricName': "dot-product", 'maxDocumentNumber': 10, 'maxSnippetNumber': 10})
#pipeline.push("SnippetBeginEndOffset as utility", {})
#pipeline.push("RankingBM25 as ranking", {'maxDocumentNumber': 10})

#print(pipeline.execute({'query': "Covid in Iran"}))
output = pipeline.execute({'query': "List clinical phenotypes and molecular genetic features of patients with KMT2B-related disorders"})
#for document in output['documents']:
#    print(document['id'])#== "73-29720240-AB":
        #print(document['text'])
    
    
#for snippet in output['rankedSnippets']:
#    print("score: " + str(snippet["score"]) + ", id: " + str(snippet["id"]) + ", snippet: " + snippet['snippet']
#     + ", offsetInBeginSection: " + str(snippet['offsetInBeginSection'])
#      + ", offsetInEndSection: " + str(snippet['offsetInEndSection']))
print(output['rankedDocuments'])
