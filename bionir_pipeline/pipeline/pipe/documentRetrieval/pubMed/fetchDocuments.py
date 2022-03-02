# URL: http://www.ncbi.nlm.nih.gov/pubmed/<pubmed_id>/

from pymed import PubMed

pubmed = PubMed(tool="BioNIR_Pipeline", email="mohammad_sh2100@yahoo.com")

def fetchDocuments(query, maxDocumentNumber):
    allDocs = pubmed.query(query, max_results=maxDocumentNumber)

    # create single docs including only pubmed_id, plus title or abstarct
    singleDocs = []
    for index, article in enumerate(allDocs):
        singleDocs.append({'id': str(index*2) + '-' + article.pubmed_id+'-TI', 'text': article.title,
                          'directLink': "http://www.ncbi.nlm.nih.gov/pubmed/"+article.pubmed_id+"/", 'type': "title"})
        singleDocs.append({'id': str(index*2+1) + '-' + article.pubmed_id+'-AB', 'text': article.abstract,
                          'directLink': "http://www.ncbi.nlm.nih.gov/pubmed/"+article.pubmed_id+"/", 'type': "abstract"})

    return singleDocs
