from bionir_pipeline import Pipeline

pipeline = Pipeline()


pipeline.push("CoreferenceResolverByKGen as preprocessing", {})
print(pipeline.execute({'documents':[{'text': "Barack Obama was born in Hawaii.  He is the president. Obama was elected in 2008."}]}))

#pipeline.push("AbbreviationResolverByKGen as preprocessing", {})
#print(pipeline.execute({'documents':[{'text': "This is NLP. NLP is so good.This study confirms the high prevalence of PSCI in diverse populations. Prevention strategies are required to reduce the prevalence of PSCI."}]}))