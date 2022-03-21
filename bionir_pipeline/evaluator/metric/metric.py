# Input : a list of "goldenQusetions" including documents and snippets
# Input : a list of "modelQusetions" including documents and snippets
# Output: evaluation including metric specific values

from .bioasq.bioasqTaskBPhaseA import BioasqTaskBPhaseA

class Metric:

    def __init__(self, metricType, paramaters):
        self.metricType = metricType
        if metricType == "BioasqTaskBPhaseA":
            self.metricPipe = BioasqTaskBPhaseA(paramaters)

    def execute(self, input):
        return self.metricPipe.execute(input)