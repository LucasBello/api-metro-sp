import logging
import json
import azure.functions as func


def main(req: func.HttpRequest) -> func.HttpResponse:
    logging.info('Python HTTP trigger function processed a request.')

    with open('extracted_status.json', 'r') as openfile:
        json_object = json.load(openfile)
    return func.HttpResponse(
        json.dumps(json_object),
        mimetype="application/json",
    )

