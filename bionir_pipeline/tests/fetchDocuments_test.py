from pymed import PubMed
pubmed = PubMed(tool="BioNIR_Pipeline", email="mohammad_sh2100@yahoo.com")
results = pubmed.query("Some query", max_results=1)

for article in results:
    print(article.title)
    print(article.abstract)
    print(article.pubmed_id)

# URL: https://pubmed.ncbi.nlm.nih.gov/<pubmed_id>/