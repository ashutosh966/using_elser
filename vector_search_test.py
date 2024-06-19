import pytesseract
import nltk
import nltk.internals
nltk.download('punkt')
from typing import Any,List,Dict
import requests
from pydantic import BaseModel
from unstructured.partition.pdf import partition_pdf
import uuid
from langchain.retrievers.multi_vector import MultiVectorRetriever
from langchain.storage import InMemoryStore
from langchain_community.vectorstores import Chroma
from langchain_core.documents import Document
from langchain_community.embeddings.fastembed import FastEmbedEmbeddings
# Initialize Tesseract OCR path for Windows    
pytesseract.pytesseract.tesseract_cmd = r'C:\Program Files\Tesseract-OCR\tesseract.exe'

# Download required NLTK data
nltk.download('punkt')

class Element(BaseModel):
    type: str
    content: Any

def extract_pdf_elements(path: str):
    return partition_pdf(
        filename=path,
        extract_images_in_pdf=False,
        infer_table_structure=True,
        chunking_strategy="by_title",
        max_characters=4000,
        new_after_n_chars=3800,
        combine_text_under_n_chars=2000,
    )

import json

def process_elements(raw_pdf_elements):
    text_elements = []
    table_elements = []

    for element in raw_pdf_elements:
        if isinstance(element, "unstructured.documents.elements.CompositeElement"):
            # If it's a composite element (likely text), extract the text content
            text_content = extract_text_from_composite(element)
            text_elements.append(text_content)
        elif isinstance(element, unstructured.documents.elements.Table):
            # If it's a table, convert it to JSON format
            table_json = convert_table_to_json(element)
            table_elements.append(table_json)

    return text_elements, table_elements

def extract_text_from_composite(composite_element):
    # Extract text content from the composite element
    return str(composite_element)

def convert_table_to_json(table_element):
    # Convert the table element to JSON format
    table_data = []
    # Your code to extract table data and format it into a JSON structure
    return json.dumps(table_data)

# Example usage:
raw_pdf_elements = []  # Your list of elements extracted from the PDF
text_elements, table_elements = process_elements(raw_pdf_elements)

# Now you have separate lists containing text and table elements
print("Text Elements:")
for text in text_elements:
    print(text)

print("\nTable Elements:")
for table_json in table_elements:
    print(table_json)
