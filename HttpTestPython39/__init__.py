import logging
import json
import azure.functions as func

import teste


def main(req: func.HttpRequest) -> func.HttpResponse:
    logging.info('Python HTTP trigger function processed a request.')

    path = req.params.get('path')
    if not path:
        return func.HttpResponse("Informe a url que quer executar", status_code=200)
    try:
        response = teste.execute(path)
        return func.HttpResponse(json.dumps(response, indent=4, sort_keys=True), status_code=200)
    except Exception as e:
        return func.HttpResponse(str(e), status_code=400)