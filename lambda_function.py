import json
import boto3

def lambda_handler(event, context):
    #searching for the faq details
    search_client = boto3.client('cloudsearchdomain', endpoint_url='https://search-my-faq-domain-{unique-id}.us-east-1.cloudsearch.amazonaws.com')
    search_response = search_client.search(
        #query="matchall", #use this with the 'structured' query parser below to search for all documents
        #queryParser='structured',
        query=event["faq"],
        queryParser='simple',
        size=1,
        sort='popularity desc'
    )
    #retrieving the document data
    document = search_response["hits"]["hit"][0]
    document_id = document["id"]
    document_faq = document["fields"]["faq"][0]
    document_popularity = int(document["fields"]["popularity"][0]) + 1
    
    #updating the document
    update_client = boto3.client('cloudsearchdomain', endpoint_url='https://doc-my-faq-domain-{unique-id}.us-east-1.cloudsearch.amazonaws.com')
    upload_batch_json_string = "[{\"type\": \"add\", \"id\": \""+document_id+"\", \"fields\": {\"popularity\": \""+str(document_popularity)+"\", \"faq\": \""+document_faq+"\"}}]"
    update_response = update_client.upload_documents(
       documents= bytes(upload_batch_json_string, 'utf-8'),
        #documents='data.json',  #use this if you want to upload a file
        contentType='application/json'
    )
    return {"status": update_response["status"]}