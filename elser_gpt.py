import os
import openai
from elasticsearch import Elasticsearch
import requests
from datetime import datetime,date,time
import uuid
import time
import requests
import logging
# openai.api_key = os.environ['openai_api']
# model = "gpt-3.5-turbo-0301"

# Connect to Elastic Cloud cluster
def es_connect():
    es = Elasticsearch([{'scheme':'http','host':"3.7.32.64",'port':9200}])
    # es_cloud_id='CRPF-Demo:YXAtc291dGgtMS5hd3MuZWxhc3RpYy1jbG91ZC5jb20kMGM2ODg2NTM0ZGJjNDUyY2EyY2RmOTM4ZjRiYmI4MzEkZjNmMjJkN2Y3MWNiNDQxOThjNDUxZjA4OWEwOGY0ZDQ='
    # es_user='costa1'
    # es_pass='R3al@2023'
    # es = Elasticsearch(cloud_id=es_cloud_id, 
    #                 basic_auth=(es_user, es_pass)
    #                 )
    print(es.ping)
    return es

# Search ElasticSearch index and return body and URL of the result
def Search_Docs(query, username):
    response = es.search(
        index="teamsyncfirstn",
        body={
            "query": {
                "bool": {
                    "must": [
                        {"match": {"username": username}},  # Filter by username
                        {
                            "bool": {
                                "should": [
                                    {
                                        "text_expansion": {
                                            "text_embedding": {
                                                "model_text": query,
                                                "model_id": ".elser_model_2",
                                            }
                                        }
                                    }
                                ]
                            }
                        }
                    ]
                }
            },
            "_source": ["text", "pageNo", "fId", "username", "tables"]  # Include table data
        }
    )
    
    return response['hits']['hits']


def search_documents_gpt(query_text, user_name):
    """
    Search documents in Elasticsearch based on the provided query and filter the answer directly from the text.
    """
    hits = Search_Docs(query_text, user_name)
    print(hits)
    if not hits:
        return []
    
    max_score = hits[0]["_score"]
    print(max_score)
    temp = [i["_score"] for i in hits]
    print(temp)
    username = hits[0]["_source"].get("username", "")
    print(username)
    search_results = []
    if max_score > 3:
        text = hits[0]["_source"].get("text", "")
        table_data = hits[0]["_source"].get("tables", "")
        
        page_no = hits[0]["_source"].get("pageNo", "")
        file_id = hits[0]["_source"].get("fId", "")
        print(file_id)
        print(page_no)
        
        combined_text = above_and_below_pagedata(text, int(page_no), file_id)
        
        
        search_results = [{"text": combined_text},{"table_data":table_data}]
        
        file_list = []
        for hit in hits:
            score = hit["_score"]
            relative_score = (score / max_score) * 100
            username = hit["_source"].get("username", "")
            file_name = hit["_source"].get("fileName", "")
            page_no = hit["_source"].get('pageNo', "")
           
            if (score > 5) and (file_name not in file_list):
                file_id = hit["_source"].get("fId", "")
                
                file_list.append(file_name)
                search_results.append({"fId": file_id, "score": relative_score, "filename": file_name, "page_no": page_no})
        print(file_list)
    else: 
        return search_results
    
    return search_results

def search_documents(query, user_name):
    """
    Search documents in Elasticsearch based on the provided query.
    """
    hits = Search_Docs(query,user_name)
    
    search_results = []
    if not hits:
        return []
    max_score = hits[0]["_score"]
    file_list=[]
    for hit in hits:
        score = hit["_score"]
        relative_score = (score / max_score) * 100
        username = hit["_source"].get("username", "")
        fileid = hit["_source"].get("fId")
        if (relative_score > 60) and (username == user_name) and ((fileid not in file_list)):
            file_list.append(fileid)
            search_results.append({"fId": fileid, "score": score})
    
    return search_results
def above_and_below_pagedata(text, page_no, file_id):
    page_no_below = page_no + 1
    below_page_text = Data_By_pageno(page_no_below, file_id)
    
    if below_page_text is not None:
        below_page_text = below_page_text['text'][0]
    else:
        below_page_text = ''
    
    if page_no != 1:
        page_no_above = page_no - 1
        above_page_text = Data_By_pageno(page_no_above, file_id)
        
        if above_page_text is not None:
            above_page_text = above_page_text['text'][0]
        else:
            above_page_text = ''
        return above_page_text + text + below_page_text
    else:
        page_no_above = page_no + 2
        below_page_text_2 = Data_By_pageno(page_no_above, file_id)
        
        if below_page_text_2 is not None:
            below_page_text_2 = below_page_text_2['text'][0]
        else:
            below_page_text_2 = ''
        return text + below_page_text + below_page_text_2


def Data_By_pageno(page_no, fid):
    match = es.search(
        index='teamsyncfirstn',
        body={
            "size": 1,
            "query": {
                "bool": {
                    "must": [
                        {"match": {"pageNo": page_no}},
                        {"match": {"fId": fid}}
                    ]
                }
            },
            "script_fields": {
                "text": {
                    "script": "params['_source']['text']"
                }
            }
        }
    )
    
    if match['hits']['hits']:
        details = match['hits']['hits']
        
        return details[0]["fields"]


def Data_By_FID(f_id,query):
    response = es.search(
        index="test-teamsyncfirstn",
        body={
            "query": {
                "bool": {
                    "must": [
                        {"match": {"fId":f_id}},  # Filter by fid
                        {
                            "bool": {
                                "should": [
                                    {
                                        "text_expansion": {
                                            "text_embedding": {
                                                "model_text": query,
                                                "model_id": ".elser_model_2",
                                            }
                                        }
                                    }
                                ]
                            }
                        }
                    ]
                }
            }
        }
    )
    
    
    if response['hits']['hits']:
        return response['hits']['hits']
        
    
def store_data_history(search_results,query_text,username,chat_id):
    text_data=search_results[0]['text']
    current_datetime = datetime.now()


    doc={
        "query":query_text,
        "text":text_data,
        "username":username,
        "date_time":current_datetime,
        "chat_id":chat_id
        
    }
    es.index(index="gpt_history",document=doc)
    print('indexing successful')

def retrieve_data_history(username,chat_id):
    query = {
        "query": {
            "bool": {
                "must": [
                    {"match": {"username": username}},
                    {"match": {"chat_id": chat_id}}
                ]
            }
        }
    }
    response=es.search(index="gpt_history",body=query)
    hits=response["hits"]["hits"]
    lst=[]
    for hit in hits:
        query_text=hit["_source"]["query"]
        text=hit["_source"]["text"]
        lst.append({"text":text,"query":query_text})
    return lst



def create_chat_id():   # api to create a chat id ,whenever a new chat is created a  chat id is associated with it 
    unique_id = str(uuid.uuid1())
    print(unique_id)
    chat_id=unique_id
    print(chat_id)
    return chat_id
def query_phi3(payload, retries=5, wait=70):
    API_URL = "https://api-inference.huggingface.co/models/microsoft/Phi-3-mini-4k-instruct"
    API_TOKEN = "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"
    headers = {"Authorization": f"Bearer {API_TOKEN}"}

    for _ in range(retries):
        response = requests.post(API_URL, headers=headers, json=payload)
        try:
            data = response.json()
            if "error" in data and "loading" in data["error"]:
                logging.warning(f"Model is loading, retrying in {wait} seconds...")
                time.sleep(wait)
                continue
            generated_text = data[0]['generated_text']
            prompt_index = generated_text.find('[/INST]')
            if prompt_index != -1:
                generated_text = generated_text[prompt_index + len('[/INST]'):]
            return generated_text
        except Exception as e:
            print("Error decoding response:", e)
            print("Response content:", response.content)
            return None

def query_mistral(payload):
    API_URL = "https://api-inference.huggingface.co/models/mistralai/Mixtral-8x7B-Instruct-v0.1"
    API_TOKEN = "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"

    headers = {"Authorization": f"Bearer {API_TOKEN}"}

    response = requests.post(API_URL, headers=headers, json=payload)
    
    try:
        data = response.json()
        
        generated_text = data[0]['generated_text']
       
        
        # Find the index of the first occurrence of '[/INST]'
        prompt_index = generated_text.find('[/INST]')
        # Extract the text after the prompt
        if prompt_index != -1:
            generated_text = generated_text[prompt_index + len('[/INST]'):]
            
        return generated_text
    except Exception as e:
        print("Error decoding response:", e)
        print("Response content:", response.content)
        return None

def truncate_text(text, max_tokens):
    tokens = text.split()
    if len(tokens) <= max_tokens:
        return text

    return ' '.join(tokens[:max_tokens])


def using_mistral(text,query_text,tables):
    negResponse = "I'm unable to answer the question based on the information I have."
    #prompt=f"[INST] You are a helpful Q&A assistant.Your task is to answer this question:{query_text} As accurately as possible,The response Only using the information from this text:{text} ,If the answer is not contained in the text then reply with {negResponse} Response [/INST]" 
    prompt = f"[INST] You are a helpful Q&A assistant. Your task is to answer this question: {query_text}.Use only the information from this text: {text}.and tables:{tables}Provide the answer strictly in HTML format, If the answer is not contained in the text, reply with {negResponse}. Response [/INST]"

    max_new_tokens=1000
    max_token=15000
    input_tokens=max_token-max_new_tokens
    text=truncate_text(prompt,input_tokens)
    
    data = query_mistral({"parameters":{"max_new_tokens":max_new_tokens},"inputs": text})
    return data

def using_phi3(text,query_text):
    input_token=800
    truncated_text=truncate_text(text,input_token)
    
    negResponse = "I'm unable to answer the question based on the information I have."
    prompt = f"""<|system|>
                You have been provided with the context and a question, try to find out the answer to the question only using the context information . If the answer to the question is not found within the context,{negResponse} return  as the response.<|end|>
                <|user|>
                Context:
                {truncated_text}

                Question: {query_text}<|end|>
                <|assistant|>"""
    data = query_phi3({"parameters":{"max_new_tokens":500},"inputs": prompt})
    return data

def extract_text_after_assistant(response_text):
    if response_text is None:
        return "No response from the model."
    assistant_index = response_text.find("<|assistant|>")
    if assistant_index != -1:
        truncated_answer = response_text[assistant_index + len("<|assistant|>"):]
        return truncated_answer.strip()
    return "I'm unable to answer the question based on the information I have"



def truncate_after_html(html_string):
    # Find the index of "</html>"
    end_index = html_string.find("</html>")
    if end_index != -1:
        # Truncate the string after "</html>"
        truncated_html = html_string[:end_index + len("</html>")]
        return truncated_html.strip()  # Remove leading/trailing whitespaces
    else:
        return html_string

def truncate_after_text(text, delimiter):
    # Find the index of the delimiter
    end_index = text.find(delimiter)
    if end_index != -1:
        # Truncate the string after the delimiter
        truncated_text = text[:end_index]
        return truncated_text.strip()  # Remove leading/trailing whitespaces
    else:
        return text


def extracting_from_multiple_files(fid1,fid2,query):
    hits1=Data_By_FID(fid1,query)
    print(hits1)
    text1=hits1[0]["_source"].get("text","")
    table_data1=hits1[0]["_source"].get("tables","")
    hits2=Data_By_FID(fid2,query)
    print(hits2)
    text2=hits2[0]["_source"].get("text","")
    table_data2=hits1[0]["_source"].get("tables","")

    
    return [{"text": text1+"\n"+ text2,"table_data1":table_data1 ,"table_data2":table_data2}]


                                                                                                                                                                                                                                                                                                                                 
    
if __name__ == "__main__":
    es = es_connect()
    print(es.ping())
    query_text = 'outcome of meeting held between central minister and farmers'
    username = "1207"

    search_results = search_documents_gpt(query_text, username)
    print(search_results)
    if not search_results:
        negResponse = "I'm unable to answer the question based on the Context Provided."
        print(negResponse)
    else:
        text = search_results[0]["text"]
        table=search_results[1]["table_data"]
        # print(text)
        # print(table)
        model_answer = using_phi3(text, query_text)
        model_answer=extract_text_after_assistant(model_answer)
        print(model_answer)
        search_results[0]["text"] = model_answer
        print(search_results)

    # fid1='vectorstore_test.pdf'
    # fid2='AmazonReport.pdf'
    # data=extracting_from_multiple_files(fid1,fid2,query_text)
    # print(data)
    # text=data[0]["text"]
    # table_data1=data[0]["table_data1"]
    # table_data2=data[0]["table_data2"]
    # model_answer=using_mistral(text,query_text,table_data2)
    # print(model_answer)
    # search_results[0]["text"]=model_answer
    # print(search_results)
































    # # # if not search_results :
    # # #    negResponse = "I'm unable to answer the question based on the information I have."
    # # #    print(negResponse)
    # # # else:
    # # #     text=search_results[0]["text"]
    # # #     data=using_llama2(text,query_text)
    # # #     print(data)
        
    # # #store_data_history(search_results,query_text,username,chat_id)
    # # # chat_id='ebf6bae7-f591-11ee-91be-3ca9f454077c'
    # # # result=retrieve_data_history(username,chat_id)
    # # # print(result)


    # print("fileid part")
    # fid="6645f6174984e66b93265f78"
    # hits=Data_By_FID(fid,query_text)
    # text=hits[0]["_source"].get("text","")
    # print(text)
    # page_no=hits[0]["_source"].get("pageNo","")
    # combined_text=above_and_below_pagedata(text,int(page_no),fid)
    # print(combined_text)
    # print(page_no)
    # model_answer=using_mistral(combined_text,query_text)

    # model_answer=extract_text_after_assistant(model_answer)
    # model_answer=truncate_after_html(model_answer)

    #print(model_answer)
    # # # print("___________________________________________")
    # # # new_data = data["text"][0]
    # # # print(new_data)
    # # # # current_time=time.ctime()
    # # # # print(current_time)
    

    


