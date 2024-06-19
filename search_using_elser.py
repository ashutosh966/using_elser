from elasticsearch import Elasticsearch, helpers, exceptions
from urllib.request import urlopen
import json 
import time


es=Elasticsearch(["http://3.7.32.64:9200"])
# es_cloud_id='CRPF-Demo:YXAtc291dGgtMS5hd3MuZWxhc3RpYy1jbG91ZC5jb20kMGM2ODg2NTM0ZGJjNDUyY2EyY2RmOTM4ZjRiYmI4MzEkZjNmMjJkN2Y3MWNiNDQxOThjNDUxZjA4OWEwOGY0ZDQ='
# es_user='costa1'
# es_pass='R3al@2023'
# es = Elasticsearch(cloud_id=es_cloud_id, 
#                 basic_auth=(es_user, es_pass)
#                 )
print(es.ping())


def create_pipeline():
    es.ingest.put_pipeline(
        id="elser-teamsync-pipeline",
        description="Ingest pipeline for ELSER",
        processors=[
            {
                "inference": {
                    "model_id": ".elser_model_2",
                    "input_output": [
                        {"input_field": "text", "output_field": "text_embedding"}
                    ],
                }
            }
        ],
    )
def create_index():
    es.indices.delete(index="test-teamsyncfirstn", ignore_unavailable=True)
    es.indices.create(
        index="test-teamsyncfirstn",
        settings={"index": {"default_pipeline": "elser-teamsync-pipeline"}},
        mappings={
            "properties": {
                "text": {
                    "type": "text",
                    "fields": {"keyword": {"type": "keyword", "ignore_above": 256}},
                },
                "text_embedding": {"type": "sparse_vector"},
                "_class": {
                "type": "text",
                "fields": {
                "keyword": {
                    "type": "keyword",
                    "ignore_above": 256
                }
                }
            },
            "fileName": {
                "type": "text",
                "fields": {
                "keyword": {
                    "type": "keyword",
                    "ignore_above": 256
                }
                }
            },
            "path": {
                "type": "text",
                "fields": {
                "keyword": {
                    "type": "keyword",
                    "ignore_above": 256
                }
                }
            },
           
            "username": {
                "type": "text",
                "fields": {
                "keyword": {
                    "type": "keyword",
                    "ignore_above": 256
                }
                }
            },
            "fId":{
                "type":"text"
            },
             "pageNo":{
                "type":"text"
            },
            "tables":{
                "type":"object"
                }
            }

                    }
    )




def Search_Docs(query):
    response = es.search(
        index="teamsyncfirstn",
        query={
            "text_expansion": {
                "text_embedding": {
                    "model_id": ".elser_model_2",
                    "model_text": query
                }
            }
        },
    )
    return response

def search_documents(query,user_name):
    """
    Search documents in Elasticsearch based on the provided query.
    """
    hits = Search_Docs(query)
    text=hits[0]["_source"].get("text","")
    search_results = [{"text":text}]
    if not hits:
        return []
    max_score = hits[0]["_score"]
    for hit in hits:
        score = hit["_score"]
        relative_score = (score / max_score) * 100
        username=hit["_source"].get("username","")
        
        if (relative_score >60) and (username==user_name) :
            
            fileid = hit["_source"].get("fId")
            
            
            search_results.append({"fId": fileid, "score": score})

    return search_results

# def delete_data():
    
#     # index_name = "teamsyncfirstn"
#     # document_id = "1UolYI4Budvm2Kii6hl7"

#     # Send a delete request
#     response = es.delete(index=index_name, id=document_id)

#     # Check the response
#     if response["result"] == "deleted":
#         print("Document deleted successfully.")
#     else:
#         print("Failed to delete document.")

   


if __name__=="__main__":
    print('helo')

    #create_pipeline()
    create_index()
    
    
    # query="what amendement is made in dpm"
    # username='1207'
    # search_result=Search_Docs(query)
    # print(search_result)
    # # for hit in res["hits"]["hits"]:
    # #     doc_id = hit["_id"]
    # #     score = hit["_score"]
    # #     filename = hit["_source"]["fileName"]
    # #     text = hit["_source"]["text"]
    # #     print(f"Score: {score}\nfilename: {filename}\ntext: {text}\n")
