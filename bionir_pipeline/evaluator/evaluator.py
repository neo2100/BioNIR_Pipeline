# Evaluator class is to take a pipline and evaluate it with a given dataset and an evaluation metric

from .metric.metric import Metric

class Evaluator:
    def __init__(self, evaluatorName, parameters):
        evaluatorType = evaluatorName.split(" as ")
        if len(evaluatorType) < 2:
            return print("ERROR: please use standard evaluator names. eg., BioasqTaskBPhaseA as metric")
        
        if evaluatorType[1] == "metric":
            self.evaluator = Metric(evaluatorType[0], parameters)

    def execute(self, input):
        return self.evaluator.execute(input)

