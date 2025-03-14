import requests
import pandas as pd
from typing import List, Tuple, Optional

def fetch_papers(query: str) -> List[dict]:
    base_url = "https://pubmed.ncbi.nlm.nih.gov/api/query"
    response = requests.get(f"{base_url}?term={query}&format=abstract")
    
    if response.status_code != 200:
        raise Exception("Failed to fetch data from PubMed API")
    
    papers = response.json().get('result', [])
    return papers

def filter_papers(papers: List[dict]) -> List[dict]:
    filtered_papers = []
    for paper in papers:
        authors = paper.get('authors', [])
        non_academic_authors = []
        company_affiliations = []
        
        for author in authors:
            affiliation = author.get('affiliation', '')
            if 'pharmaceutical' in affiliation.lower() or 'biotech' in affiliation.lower():
                non_academic_authors.append(author['name'])
                company_affiliations.append(affiliation)
        
        if non_academic_authors:
            filtered_papers.append({
                'PubmedID': paper['id'],
                'Title': paper['title'],
                'Publication Date': paper['pub_date'],
                'Non-academic Author(s)': ', '.join(non_academic_authors),
                'Company Affiliation(s)': ', '.join(company_affiliations),
                'Corresponding Author Email': paper.get('corresponding_author_email', '')
            })
    
    return filtered_papers

def save_to_csv(papers: List[dict], filename: str) -> None:
    df = pd.DataFrame(papers)
    df.to_csv(filename, index=False)