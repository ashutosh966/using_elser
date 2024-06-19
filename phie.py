import requests
import time
from elasticsearch import Elasticsearch
es=Elasticsearch(['http://3.7.32.64:9200'])
def query(payload):
    API_URL = "https://api-inference.huggingface.co/models/microsoft/phi-2"
    API_TOKEN = "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"

    headers = {"Authorization": f"Bearer {API_TOKEN}"}
    model_loaded = False

    while not model_loaded:
        try:
            response = requests.post(API_URL, headers=headers, json=payload)
            response.raise_for_status()  # Raise an exception for any HTTP error
            data = response.json()
            generated_text = data[0]['generated_text']

            # Find the index of the first occurrence of '[/INST]'
            prompt_index = generated_text.find('[/INST]')
            # Extract the text after the prompt
            if prompt_index != -1:
                generated_text = generated_text[prompt_index + len('[/INST]'):]

            model_loaded = True  # Set the flag to True indicating model is loaded

            return generated_text
        except requests.exceptions.HTTPError as err:
            if response.status_code == 503:  # Service Unavailable error
                print("Model loading. Retrying in 5 seconds...")
                time.sleep(5)  # Wait for 5 seconds and retry
            else:
                print("HTTP Error:", err)
                print("Response content:", response.content)
                return None
        except Exception as e:
            print("Error:", e)
            print("Retrying in 5 seconds...")
            time.sleep(5)  # Wait for 5 seconds and retry
def search_documents_gpt(query_text, user_name):
    """
    Search documents in Elasticsearch based on the provided query and filter the answer directly from the text.
    """
    hits = Search_Docs(query_text)
    
    if not hits:
        return []
    max_score = hits[0]["_score"]
    text=hits[0]["_source"].get("text","")
    search_results = [{"text":text,"id":2}]
    for hit in hits:
        score = hit["_score"]
        relative_score = (score / max_score) * 100
        username = hit["_source"].get("username", "")
        
        if relative_score > 60 and username == user_name:
            file_id = hit["_source"].get("fId","")
            file_name=hit["_source"].get("fileName","")
            search_results.append({"fId": file_id, "score": score,"filename":file_name})

    
    return search_results
def Search_Docs(query):
    response = es.search(
        index="teamsyncfirstn",
        query={
            "bool": { 
                "should": [
                        {
                        "text_expansion": {
                            "text_embedding": {
                                "model_text": query,
                                "model_id": ".elser_model_2",
                                "boost": 1 
                            }
                        }
                        }
                ]
            }
        }
    )
    return response['hits']['hits']

# Example usage:
query_text='how many incident occur during farmer protest'
username=1207
result=search_documents_gpt(query_text,username)
text=result[0]["text"]
prompt = f"<s>[INST] Provide a precise answer  to the following question: {query_text} And  Response should be  in bullet points [/INST]\n\n{text}"

payload = {"inputs": prompt}
result = query(payload)
print("Generated text:", result)
