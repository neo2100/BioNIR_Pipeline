# ref: https://github.com/xianchen2/Text_Retrieval_BM25/blob/master/document_retrieval.ipynb
import pickle
import re
from nltk.stem import PorterStemmer 
from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize
import math
import os

class QueryParser:

    def __init__(self):
        # some prepartion
        self.stop_words = set(stopwords.words('english'))
        self.documents = []
        script_dir = os.path.dirname(__file__) #<-- absolute dir the script is in
        rel_path = "db/db_singledocs.list"
        abs_file_path = os.path.join(script_dir, rel_path)
        with open(abs_file_path, 'rb') as document_file:
            self.documents = pickle.load(document_file)
        # BM25
        self.tf = {}
        self.df = {}
        self.file_to_terms = self.process_files()
        self.regdex = self.regular_index(self.file_to_terms)
        self.invertedIndex = self.inverted_index()
        self.dltable = self.docLtable()
        self.dl = self.docLen()
        self.avgdl = self.avgdocl()
        self.N = self.doc_n()
        self.idf = self.inverse_df()

    def tokenizer(self, sentence: str, doStemmer = True):
        q = sentence.lower()
        #subsitute all non-word characters with whitespace
        pattern = re.compile('\W+')
        q = pattern.sub(' ', q)
        # split text into words (tokenized list for a document)
        q = q.split()
        # stemming words
        if doStemmer:
            stemmer = PorterStemmer()
            q = [stemmer.stem(w) for w in q ]

        return q

    def removeStopWords(self, sentence):
        word_tokens = word_tokenize(sentence)
        filtered_sentence = [w for w in word_tokens if not w.lower() in self.stop_words]
        return ' '.join(filtered_sentence)

    # return IDFs and words in one dict
    def inverseOfList(self, list):
        stemmer = PorterStemmer()
        inverseDict = {}
        for w in list:
            wStemmed = stemmer.stem(w)
            if wStemmed in self.idf:
                inverseDict[w] = self.idf[wStemmed]
            else:
                inverseDict[w] = 10 # <-- default high value for rare items
        return inverseDict


# From BM25 functions
    def process_files(self):
        '''
        input: filenames
        output: a dictionary keyed by filename, and with values of its term list
        '''
        file_to_terms = {}

        for doc in self.documents:
            #read the whole text of a file into a single string with lowercase
            file_to_terms[doc["id"]] = doc["value"].lower()
            #subsitute all non-word characters with whitespace
            pattern = re.compile('\W+')
            file_to_terms[doc["id"]] = pattern.sub(' ', file_to_terms[doc["id"]])
            # split text into words (tokenized list for a document)
            file_to_terms[doc["id"]] = file_to_terms[doc["id"]].split()
            # stemming words
            stemmer = PorterStemmer()
            file_to_terms[doc["id"]] = [stemmer.stem(w) for w in file_to_terms[doc["id"]] ]
              
        return file_to_terms

    def doc_n(self):
        '''
        return the number of docs in the collection
        '''
        return len(self.file_to_terms)


    def index_one_file(self, termlist):
        '''
        input: termlist of one document.
        map words to their position for one document
        output: a dictionary with word as key, position as value.
        '''
        fileIndex = {}
        for index,word in enumerate(termlist):
            if word in fileIndex.keys():
                fileIndex[word].append(index)
            else:
                fileIndex[word] = [index]

        return fileIndex

    def regular_index(self,termlists):
        '''
        input: output of process_files(filenames)
        output: a dictionary. key: filename, value: a dictionary with word as key, position as value  
        '''
        regdex = {}

        for filename in termlists.keys():
            regdex[filename] = self.index_one_file(termlists[filename])

        return regdex


    def inverted_index(self):
        '''
        input： output of make_indexes function.
        output: dictionary. key: word, value: a dictionary keyed by filename with values of term position for that file.
        '''
        total_index = {}
        regdex = self.regdex

        for filename in regdex.keys():
            
            self.tf[filename] = {}

            for word in regdex[filename].keys():
                # tf dict key: filename, value: dict key is word, value is count
                self.tf[filename][word] = len(regdex[filename][word])
                
                if word in self.df.keys():
                    # df dict key: word, value: counts of doc containing that word
                    self.df[word] += 1
                else:
                    self.df[word] = 1

                if word in total_index.keys():
                    if filename in total_index[word].keys():
                        total_index[word][filename].extend(regdex[filename][word])
                    else:
                        total_index[word][filename] = regdex[filename][word]
                else:
                    total_index[word] = {filename: regdex[filename][word]}

        return total_index

    def docLtable(self):
        '''
        output: dict, key:word, value:dict(key: number of docs contaiing that word, value:total_freq)
        '''
        dltable = {}
        for w in self.invertedIndex.keys():	
            total_freq = 0
            for file in self.invertedIndex[w].keys():
                total_freq += len(self.invertedIndex[w][file])
            
            dltable[w] = {len(self.invertedIndex[w].keys()):total_freq}
        
        return dltable


    def docLen(self):
        '''
        return a dict, key: filename, value: document length
        '''
        dl = {}
        for doc in self.documents:
            dl[doc["id"]]=len(self.file_to_terms[doc["id"]])
        return dl

    def avgdocl(self):
        sum = 0
        for file in self.dl.keys():
            sum += self.dl[file]
        avgdl = sum/len(self.dl.keys())
        return avgdl

    def inverse_df(self):
        '''
        output: inverse doc freq with key:word, value: idf
        '''
        idf = {}
        for w in self.df.keys():
            # idf[w] = math.log((self.N - self.df[w] + 0.5)/(self.df[w] + 0.5))
            idf[w] = math.log((self.N +1 )/self.df[w])
        return idf
        