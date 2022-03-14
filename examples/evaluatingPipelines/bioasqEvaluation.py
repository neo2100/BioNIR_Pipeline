import os
import json
from bionir_pipeline import Evaluator

goldenFileName = 'BioASQ-task10bPhaseB-testset1'
modelFileName = 'BioASQ-task10bPhaseA-testset1_output_BioNIR_Basic'

# preparing inputs
goldenQuestions = {}
script_dir = os.path.dirname(__file__)  # <-- absolute dir the script is in
abs_file_path = os.path.join(script_dir, goldenFileName)
with open(abs_file_path, 'rb') as document_file:
    goldenQuestions = json.load(document_file)['questions']
    document_file.close()

modelQuestions = {}
script_dir = os.path.dirname(__file__)  # <-- absolute dir the script is in
abs_file_path = os.path.join(script_dir, modelFileName)
with open(abs_file_path, 'rb') as document_file:
    modelQuestions = json.load(document_file)['questions']
    document_file.close()

bioasqTaskBPhaseA = Evaluator("BioasqTaskBPhaseA as metric", {})

output = bioasqTaskBPhaseA.execute(
    {'goldenQuestions': goldenQuestions, 'modelQuestions': modelQuestions})

print(output['evaluation'])
