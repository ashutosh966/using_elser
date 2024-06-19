from fastapi import FastAPI, HTTPException
from elasticsearch import Elasticsearch

app = FastAPI()

# Establish connection to Elasticsearch
es = Elasticsearch(["http://3.7.32.64:9200"])

@app.get("/ping")
async def ping_elasticsearch():
    """
    Check if Elasticsearch is available.
    """
    return {"ping": es.ping()}

@app.post("/search")
async def search_documents(text):
    """
    Search documents in Elasticsearch based on the provided query.
    """
    model_text = text
    if not model_text:
        raise HTTPException(status_code=400, detail="Query parameter 'model_text' is required.")

    response = es.search(
        index="teamsyncfirstn",
        body={
            "query": {
                "text_expansion": {
                    "text_embedding": {
                        "model_id": ".elser_model_2",
                        "model_text": model_text
                    }
                }
            }
        }
    )

    hits = response["hits"]["hits"]
    search_results = []
    max_score=hits[0]["_score"]
    for hit in hits:
        score = hit["_score"]
        relative_score=(score/max_score)*100
        if relative_score>60:
            filename = hit["_source"].get("fId", "")
            
            search_results.append({"filename": filename,"score":relative_score})
    
    return search_results
