import PyPDF2
import pdfplumber
import pandas as pd
import json
from elasticsearch import Elasticsearch

def extract_text_from_page(page):
    return page.extract_text()

def extract_tables_from_page(page):
    tables = []
    extracted_tables = page.extract_tables()
    for table in extracted_tables:
        df = pd.DataFrame(table[1:], columns=table[0])
        tables.append(df.to_dict(orient='records'))
    return tables

def index_page_to_elasticsearch(es, index_name, page_number, text, tables):
    document = {
        'page_number': page_number,
        'text': text,
        'tables': tables
    }
    es.index(index=index_name, id=page_number, body=document)

def main(pdf_path, es_host, es_port, index_name):
    # Connect to Elasticsearch
    es = Elasticsearch([{'host': es_host, 'port': es_port,'scheme':'http'}])

    with pdfplumber.open(pdf_path) as pdf:
        for page_number, page in enumerate(pdf.pages, start=1):
            # Extract text and tables
            text = extract_text_from_page(page)
            tables = extract_tables_from_page(page)
            
            # Index the page content to Elasticsearch
            index_page_to_elasticsearch(es, index_name, page_number, text, tables)
    
    print("Indexing complete.")

if __name__ == "__main__":
    pdf_path = r"C:\Users\Ashutosh\Desktop\using_elser\vectorstore_test.pdf"
    es_host = "3.7.32.64"  # Change this to your Elasticsearch host
    es_port = 9200  # Change this to your Elasticsearch port
    index_name = "pdf_content_2"
    
    main(pdf_path, es_host, es_port, index_name)
