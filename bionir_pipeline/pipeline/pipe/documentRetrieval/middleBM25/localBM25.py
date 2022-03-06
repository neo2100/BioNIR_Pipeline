# ref: https://github.com/xianchen2/Text_Retrieval_BM25/blob/master/document_retrieval.ipynb
import pickle
import re
from nltk.stem import PorterStemmer 
import math
import os
from .documentParser import DocumentParser

class LocalBM25:
    b = 0.75
    k = 1.2

    def __init__(self):
        # some prepartion
        self.refDocuments = []
        script_dir = os.path.dirname(__file__) #<-- absolute dir the script is in
        rel_path = "db/db_singledocs.list"
        abs_file_path = os.path.join(script_dir, rel_path)
        with open(abs_file_path, 'rb') as document_file:
            self.refDocuments = pickle.load(document_file)

        self.refDocumentsParsed = DocumentParser(self.refDocuments, 'value')
        # BM25
        self.avgdl = self.refDocumentsParsed.avgdl
        self.idf = self.refDocumentsParsed.idf

    def rankDocuments(self, query, documents):
        self.queryDocumentsParsed = DocumentParser(documents, 'text')
        self.file_to_terms = self.queryDocumentsParsed.file_to_terms
        self.regdex = self.queryDocumentsParsed.regdex
        self.invertedIndex = self.queryDocumentsParsed.invertedIndex
        self.dl = self.queryDocumentsParsed.dl

        self.total_score  = self.BM25scores(self.queryParser(query))
        
        return self.ranked_docs()
    
    def queryParser(self, query):
        q = query.lower()
        #subsitute all non-word characters with whitespace
        pattern = re.compile('\W+')
        q = pattern.sub(' ', q)
        # split text into words (tokenized list for a document)
        q = q.split()
        # stemming words
        stemmer = PorterStemmer()
        q = [stemmer.stem(w) for w in q ]
        return q

    def get_score (self,filename,qlist):
        '''
        filename: filename
        qlist: termlist of the query 
        output: the score for one document
        '''
        score = 0
        #print('filename: ' + filename)
        for w in qlist:
            if w not in self.file_to_terms[filename]:
                continue
            #print('the word: '+ w)
            wc = len(self.invertedIndex[w][filename])
            score += self.idf[w] * ((wc)* (self.k+1)) / (wc + self.k * 
                                                         (1 - self.b + self.b * self.dl[filename] / self.avgdl))
            #print(score)
        return score


    def BM25scores(self,qlist):
        '''
        output: a dictionary with filename as key, score as value
        '''
        total_score = {}
        for doc in self.file_to_terms.keys():
            total_score[doc] = self.get_score(doc,qlist)
        return total_score


    def ranked_docs(self):
        ranked_docs = sorted(self.total_score.items(), key=lambda x: x[1], reverse=True)
        return ranked_docs