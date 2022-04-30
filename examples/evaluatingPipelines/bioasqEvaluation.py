import os
import json
from bionir_pipeline import Evaluator

goldenFileName = 'BioASQ-task10bPhaseB-testset3'
modelFileName = 'BioASQ-task10bPhaseA-testset3_output_bionirheadone_nn0t_qu_e2_ended'

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
