from elasticsearch import Elasticsearch
import os 

# username='elastic'
# password='admin123'
es = Elasticsearch([{'host': '3.7.32.64', 'port': 9200,'scheme':'http'}]
                #    basic_auth=(username,password),
                #    verify_certs=False,  # Set to False if you want to ignore SSL certificate verification (not recommended)
                #     ssl_show_warn=False
                   )




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



def create_routing_pipeline():
    es.ingest.put_pipeline(
        id="elser-routing-pipeline",
        description="Routing pipeline to select appropriate embedding pipeline",
        processors=[
            {
                "script": {
                    "lang": "painless",
                    "source": """
                        if (ctx.fileName != null && ctx.fileName.endsWith('.csv')) {
                            ctx.pipeline = 'elser-teamsync-pipeline-table';
                        } else {
                            ctx.pipeline = 'elser-teamsync-pipeline-text';
                        }
                    """
                }
            },
            {
                "pipeline": {
                    "name": "{{ctx.pipeline}}"
                }
            }
        ],
    )


def create_index(es):
    es.indices.delete(index="teamsyncfirstn", ignore_unavailable=True)
    es.indices.create(
        index="teamsyncfirstn",

        settings={"index": {"default_pipeline": "elser-teamsync-pipeline"}},
        mappings={
            "properties": {
                "text": {
                    "type": "text"    
                },
                "text_embedding": {"type": "sparse_vector"},
                
                "username": {
                    "type": "text"
                    
                },
                "fId": {
                    "type": "text"
                },
                "fileName":{
                    "type":"text"
                },
                "pageNo": {
                    "type": "text"
                },
                "tables": {
                    "type":"keyword"
                   
               
            }
        }
        }
    )
def add_document(es, index, document):
    es.index(index=index, body=document)

if __name__=="__main__":
    print(es.ping())
    
    # filepath=r"C:\Users\Ashutosh\Desktop\using_elser\vectorstore_test.pdf"
    # filename=os.path.basename(filepath)
    # base,extension=os.path.splitext(filename)
    # print(base)
    # print(extension)
    #create_routing_pipeline()
    # create_pipeline()
    #create_pipeline_table()
    #print('pipeline created successfully')
    create_index(es)
    print('mapping created succesfully')

    

    # # Example documents
 


    # document_csv = {
    #     "fileName": "data.csv",
    #     "text": "sample text data",
    #     "tables": [
    #             [
    #             [
    #                 "Oil & Natural Gas Corporation Limited Well Completion Report Well: GK_42#8 (GK_42#G)    Geology Operations Group, WOB, Mumbai July 2018"
    #             ]
    #             ]
    #         ]
    # }

    #add_document(es, "test-teamsyncfirstn3", document_txt)
    # # # # add_document(es, "test-teamsyncfirstn2", document_text)





