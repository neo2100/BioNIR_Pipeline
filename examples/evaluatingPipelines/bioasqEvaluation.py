import os
import json
from bionir_pipeline import Evaluator

goldenFileName = 'BioASQ-task10bPhaseB-testset2'
modelFileName = 'BioASQ-task10bPhaseA-testset2_output_BM25_base'

script_dir = os.path.dirname(__file__)  # <-- absolute dir the script is in
# preparing inputs
goldenQuestions = {}
with open(os.path.join(script_dir, goldenFileName), 'rb') as document_file:
    goldenQuestions = json.load(document_file)['questions']

modelQuestions = {}
with open(os.path.join(script_dir, modelFileName), 'rb') as document_file:
    modelQuestions = json.load(document_file)['questions']

bioasqTaskBPhaseA = Evaluator("BioasqTaskBPhaseA as metric", {})

output = bioasqTaskBPhaseA.execute(
    {'goldenQuestions': goldenQuestions, 'modelQuestions': modelQuestions})

print(output['evaluation'])
