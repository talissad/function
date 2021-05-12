import logging
import json
import azure.functions as func

import connect_ad
import service_bus


def main(req: func.HttpRequest) -> func.HttpResponse:
    logging.info('Python HTTP trigger function processed a request.')

    users = connect_ad.get_all_users()
    try:
        service_bus.send_users(users)
        return func.HttpResponse(json.dumps(users, indent=4, sort_keys=True), status_code=200)
    except Exception as e:
        return func.HttpResponse(str(e), status_code=400)