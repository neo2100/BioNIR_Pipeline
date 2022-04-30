import os
import json
from bionir_pipeline import Evaluator

goldenFileName = 'BioASQ-task10bPhaseB-testset3'
model1FileName = 'BioASQ-task10bPhaseA-testset3_output_basic_mid7'
model2FileName = 'BioASQ-task10bPhaseA-testset3_output_bionirheadone_nn0t_qu_ended'

script_dir = os.path.dirname(__file__)  # <-- absolute dir the script is in
# preparing inputs
goldenQuestions = {}
with open(os.path.join(script_dir, goldenFileName), 'rb') as document_file:
    goldenQuestions = json.load(document_file)['questions']

model1Questions = {}
with open(os.path.join(script_dir, model1FileName), 'rb') as document_file:
    model1Questions = json.load(document_file)['questions']

model2Questions = {}
with open(os.path.join(script_dir, model2FileName), 'rb') as document_file:
    model2Questions = json.load(document_file)['questions']

bioasqTaskBPhaseA = Evaluator("BioasqTaskBPhaseA as metric", {})

output1 = bioasqTaskBPhaseA.execute(
    {'goldenQuestions': goldenQuestions, 'modelQuestions': model1Questions})
output2 = bioasqTaskBPhaseA.execute(
    {'goldenQuestions': goldenQuestions, 'modelQuestions': model2Questions})

for index, model1Question in enumerate(output1['modelQuestions']):
    if 'snippetEvaluation' in model1Question:
        if model1Question['snippetEvaluation']['recall'] != output2['modelQuestions'][index]['snippetEvaluation']['recall']:
            print(index, model1Question["body"], model1Question['snippetEvaluation']['recall'], output2['modelQuestions'][index]['snippetEvaluation']['recall'])

