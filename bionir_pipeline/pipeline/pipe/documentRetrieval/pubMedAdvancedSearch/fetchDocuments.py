# URL: http://www.ncbi.nlm.nih.gov/pubmed/<pubmed_id>/
# NOTE: update pymed with this bug fixed one: pip install -e git://github.com/iacopy/pymed.git@fork-fixes#egg=pymed

from pymed import PubMed

pubmed = PubMed(tool="BioNIR_Pipeline", email="mohammad_sh2100@yahoo.com")


def getTotalResultsCount(query):
    return pubmed.getTotalResultsCount(query)


def fetchDocuments(query, maxDocumentNumber):
    allDocs = pubmed.query(query, max_results=maxDocumentNumber)
    # create single docs including only pubmed_id, plus title or abstarct
    singleDocs = []
    for index, article in enumerate(allDocs):
        # Sometimes article['pubmed_id'] contains list separated with comma - take first pubmedId in that list - thats article pubmedId
        pubmedId = article.pubmed_id.partition('\n')[0]
        singleDocs.append({'id': str(index*2) + '-' + pubmedId+'-TI', 'text': article.title,
                          'directLink': "http://www.ncbi.nlm.nih.gov/pubmed/"+pubmedId+"/", 'type': "title"})
        if(article.abstract):
            singleDocs.append({'id': str(index*2+1) + '-' + pubmedId+'-AB', 'text': article.abstract,
                              'directLink': "http://www.ncbi.nlm.nih.gov/pubmed/"+pubmedId+"/", 'type': "abstract"})

    return singleDocs
