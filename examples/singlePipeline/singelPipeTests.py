from bionir_pipeline import Pipeline

pipeline = Pipeline()

#pipeline.push("CoreNLPAnnotator as preprocessing", {'properties':{'annotators': 'tokenize, ssplit, pos, lemma, ner, parse, coref', 'coref.algorithm': 'neural', 'coref.neural.greedyness': '0.51'}})
#pipeline.push("CoreferenceResolverByKGen as preprocessing", {})

pipeline.push("SentenceSplittingByNLTK as preprocessing", {'outputName': 'sentences'})
#pipeline.push("BioASQHead as embedding", { 'modelName': "bionirhead_nn0_qu_Interval_10.pt"})
pipeline.push("BioASQHeadOne as embedding", { 'modelName': "bionirheadone_nn0_qu_Interval_10.pt"})
print(pipeline.execute({'query': 'who is he?','documents':[{'text': "Barack Obama was born in Hawaii.  He is the president. Obama was elected in 2008."}]}))

#pipeline.push("AbbreviationResolverByKGen as preprocessing", {})
#print(pipeline.execute({'documents':[{'text': "This is NLP. NLP is so good.This study confirms the high prevalence of PSCI in diverse populations. Prevention strategies are required to reduce the prevalence of PSCI."}]}))