# BioNIR Pipeline
Explainable Neural Information Retrieval in Biomedical Science (BioNIR) _ Information Retrieval Pipeline for BioASQ Task B

It is an ongoing project to create an bio information retrieval in pipeline framework and easy to reconfigure. Please feel free to contact here or in LinkedIn if you are interested to collaborate.


To Do
-----
-   Install package via: pip install -e .
-   Test and run examples in: /bionir_pipeline/examples
-   If you want to use preprocessing from KGen, make sure you have stanfordcoreNLP server up and running more info below in Stanford CoreNLP section.

Pull requests are encouraged!

Stanford CoreNLP
-----
More info about installation and models: https://huggingface.co/stanfordnlp/CoreNLP

You can also directly download the core and extra models from: https://stanfordnlp.github.io/CoreNLP/
To add extra models move them to the root folder of the core.

You can use this command to run the server:
```
java -mx4g -cp "*" edu.stanford.nlp.pipeline.StanfordCoreNLPServer -preload tokenize,ssplit,pos,lemma,ner,depparse,parse,coref -status_port 9000 -port 9000 -timeout 300000
```

References
-----
-   Rossanez, A.; Dos Reis, J. C.; Torres, R. S.; De Ribaupierre, H. KGen: A Knowledge Graph Generator from Biomedical Scientific Literature. BMC Medical Informatics and Decision Making, v. 20, p. 314, 2020.
