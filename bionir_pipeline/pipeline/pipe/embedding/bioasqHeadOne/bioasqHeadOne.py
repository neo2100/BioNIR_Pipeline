# Parameters: modelName -> the name of BioASQBERT model to be usesd
# Input:  a query and a list of "documents" at least containing: "sentences"
# Output: a list of "documents" at least containing: "sentences" and "sentencesEmbedded"
# Output: "query" and "queryEmbedded"

# INFO: for more infor about the models: https://www.sbert.net/docs/pretrained_models.html

import os
from transformers import AutoTokenizer, AutoModel
import torch
from torch.nn import functional as F
from .models.bionirHeads import LstmNet

class BioASQHeadOne:

    def __init__(self, parameters):
        # some prepartion
        if 'modelName' in parameters:
            self.modelName = parameters['modelName']
        else:
            self.modelName = "bionirheadone_nn0_qu_Interval_10.pt"
            print("WARNING: no modelName is provided for BioASQBERT. (default value = bionirheadone_nn0_qu_Interval_10.pt)")

        script_dir = os.path.dirname(__file__)  # <-- absolute dir the script is in
        self.modelPath = os.path.join(script_dir, 'models' ,self.modelName)
        #self.tokenizer = BertTokenizer.from_pretrained(self.checkpoint)
        #self.model = AutoModel.from_pretrained(self.checkpoint)   
        checkpoint = torch.load(self.modelPath, map_location='cpu')
        self.tokenizer = AutoTokenizer.from_pretrained('sentence-transformers/multi-qa-mpnet-base-cos-v1')
        self.model = AutoModel.from_pretrained('sentence-transformers/multi-qa-mpnet-base-cos-v1')
        #load the head
        self.headModel = LstmNet(2*768, 96, 32, 1)
        self.headModel.load_state_dict(checkpoint)
        print("Info: BioASQBERT as embedding has been initialized")

    def execute(self, input):
        if not 'query' in input:
            print("ERROR: query is missing in the input for BioASQBERT")
            return input

        input['queryEmbedded'] =  self.encode(input['query']).view(-1, 1, 768)
        #input['queryEmbedded'] =  self.headModel(input['queryEmbedded'].view(-1, 1, 768))
        
        if not 'documents' in input:
            print("ERROR: dpcuments is missing in the input for BioASQBERT")
            return input

        for document in input['documents']:
            if not 'sentences' in document:
                print("ERROR: sentences is missing in a document in documents for BioASQBERT")
                return input

            document['sentencesEmbedded'] = self.encode(document['sentences']).view(-1, 1, 768)
            document['sentencesScored'] = []
            for sentenceEmbedded in document['sentencesEmbedded']:
                document['sentencesScored'].append( 1 -
                    self.headModel(torch.cat((input['queryEmbedded'],sentenceEmbedded.view(-1, 1, 768)),-1)))

        return input



    #Encode text
    def encode(self, texts):
        # Tokenize sentences
        encoded_input = self.tokenizer(texts, padding=True, truncation=True, return_tensors='pt')
        # Compute token embeddings
        with torch.no_grad():
            model_output = self.model(**encoded_input, return_dict=True)
        # Perform pooling
        embeddings = self.mean_pooling(model_output, encoded_input['attention_mask'])
        # Normalize embeddings
        embeddings = F.normalize(embeddings, p=2, dim=1)
        return embeddings

    #Mean Pooling - Take average of all tokens
    def mean_pooling(self, model_output, attention_mask):
        token_embeddings = model_output.last_hidden_state #First element of model_output contains all token embeddings
        input_mask_expanded = attention_mask.unsqueeze(-1).expand(token_embeddings.size()).float()
        return torch.sum(token_embeddings * input_mask_expanded, 1) / torch.clamp(input_mask_expanded.sum(1), min=1e-9)
