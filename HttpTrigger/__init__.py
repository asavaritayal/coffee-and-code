import logging

import azure.functions as func

import pandas as pd
import statsmodels.formula.api as smf
import statsmodels.api as sm


def main(req: func.HttpRequest) -> func.HttpResponse:
    logging.info('Python HTTP trigger function processed a request.')

    # initialize the model
    model = sm.load('HttpTrigger/model.pickle')

    codinghours = req.params.get('hours')

    if not codinghours:
        try:
            req_body = req.get_json()
        except ValueError:
            pass
        else:
            name = req_body.get('hours')

    if codinghours:

        # you have to create a DataFrame since the Statsmodels formula interface expects it
        hours = pd.DataFrame({'CodingHours': [0]})
        hours['CodingHours'][0] = int(codinghours)

        # use the model to make predictions on a new value
        coffeecups = model.predict(hours)

        return func.HttpResponse(f"{coffeecups[0]}")

    else:
        return func.HttpResponse(
             "Please pass a the number of coding hours in the request body",
             status_code=400
        )
