# BioNIR Pipline class 
# Pipline order:
# 1- documentRetrieval (PubMed APIs or BM25+DB)
# 2- preprocessing: (a- sentence splitting b- co-reference resolution 3- Abbreviation resolution 4- sentence simplification)
# 3- embedding (SBERT or BioASQ SBERT)
# 4- pooling (MEAN, MAX, or CLS hyper parameters)
# 5- ranking (sorting)