import pytesseract
import nltk
import nltk.internals
nltk.download('punkt')
from typing import Any
import requests
from pydantic import BaseModel
from unstructured.partition.pdf import partition_pdf
import uuid
from langchain.retrievers.multi_vector import MultiVectorRetriever
from langchain.storage import InMemoryStore
from langchain_community.vectorstores import Chroma
from langchain_core.documents import Document
from langchain_community.embeddings.fastembed import FastEmbedEmbeddings
import platform

# if platform.system() != "Windows":
#     import pwd  # Only import pwd if not on Windows

pytesseract.pytesseract.tesseract_cmd = r'C:\Program Files\Tesseract-OCR\tesseract.exe'

def raw_pdf_element():
    path = r'C:\Users\Ashutosh\Desktop\using_elser\vectorstore_test.pdf'
    raw_pdf_elements = partition_pdf(
        filename=path,
        extract_images_in_pdf=False,
        infer_table_structure=True,
        chunking_strategy="by_title",
        max_characters=4000,
        new_after_n_chars=3800,
        combine_text_under_n_chars=2000,
        image_output_dir_path=path,
    )
    print(raw_pdf_elements)
    return raw_pdf_elements

def dict_to_store_count(raw_pdf_elements):
    category_counts = {}

    for element in raw_pdf_elements:
        category = str(type(element))
        if category in category_counts:
            category_counts[category] += 1
        else:
            category_counts[category] = 1

    unique_categories = set(category_counts.keys())
    print(category_counts)

def count_by_category(raw_pdf_elements):
    class Element(BaseModel):
        type: str
        text: Any
    categorized_elements = []
    for element in raw_pdf_elements:
        if "unstructured.documents.elements.Table" in str(type(element)):
            categorized_elements.append(Element(type="table", text=str(element)))
        elif "unstructured.documents.elements.CompositeElement" in str(type(element)):
            categorized_elements.append(Element(type="text", text=str(element)))

    table_elements = [e for e in categorized_elements if e.type == "table"]
    print(len(table_elements))

    text_elements = [e for e in categorized_elements if e.type == "text"]
    print(len(text_elements))
    return table_elements, text_elements

def using_mistral(text):
    API_URL = "https://api-inference.huggingface.co/models/mistralai/Mixtral-8x7B-Instruct-v0.1"
    API_TOKEN = "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"

    headers = {"Authorization": f"Bearer {API_TOKEN}"}

    prompt = f"[INST] You are a helpful assistant. Your task is to summarize tables and text. Give a concise summary of {text} the tables and texts [/INST]"

    max_new_tokens = 1000
    payload = {"parameters": {"max_new_tokens": max_new_tokens}, "inputs": prompt}

    response = requests.post(API_URL, headers=headers, json=payload)

    try:
        data = response.json()
        generated_text = data[0]['generated_text']

        prompt_index = generated_text.find('[/INST]')
        if prompt_index != -1:
            generated_text = generated_text[prompt_index + len('[/INST]'):]
        print(generated_text)
        return generated_text
    except Exception as e:
        print("Error decoding response:", e)
        print("Response content:", response.content)
        return None

def storing_in_vectorstore(text_summaries, table_summaries):
    vectorstore = Chroma(collection_name="summaries", embedding_function=FastEmbedEmbeddings())
    store = InMemoryStore()
    id_key = "doc_id"

    retriever = MultiVectorRetriever(
        vectorstore=vectorstore,
        docstore=store,
        id_key=id_key,
    )

    filtered_text_summaries = [summary for summary in text_summaries if summary is not None]
    filtered_table_summaries = [summary for summary in table_summaries if summary is not None]

    doc_ids_text = [str(uuid.uuid4()) for _ in filtered_text_summaries]
    summary_texts = [
        Document(page_content=s, metadata={id_key: doc_ids_text[i]})
        for i, s in enumerate(filtered_text_summaries)
    ]
    retriever.vectorstore.add_documents(summary_texts)
    retriever.docstore.mset(list(zip(doc_ids_text, filtered_text_summaries)))

    doc_ids_table = [str(uuid.uuid4()) for _ in filtered_table_summaries]
    summary_tables = [
        Document(page_content=s, metadata={id_key: doc_ids_table[i]})
        for i, s in enumerate(filtered_table_summaries)
    ]
    retriever.vectorstore.add_documents(summary_tables)
    retriever.docstore.mset(list(zip(doc_ids_table, filtered_table_summaries)))

    return retriever

if __name__ == "__main__":
    raw_element = raw_pdf_element()
    print("--------------------------------------------------------")
    dict_to_store_count(raw_element)
    table_elements, text_elements = count_by_category(raw_element)
    for element in table_elements:
        print(element)
    
    # text_summaries = [using_mistral(element) for element in text_elements]
    # table_summaries = [using_mistral(element) for element in table_elements]
    # retriever = storing_in_vectorstore(text_summaries, table_summaries)

    # retrieved_docs = retriever.invoke("substance whose pH is greater than 5?")
    # print(retrieved_docs)
