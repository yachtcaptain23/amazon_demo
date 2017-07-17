import json
import dateutil.parser
import datetime
import time
import os
import math
import random
import logging
import requests

SOOTHE_PRODUCTION = "https://www.soothe.com"
SOOTHE_LOCAL = "https://626a1d70.ngrok.io"
HOST_URL = SOOTHE_LOCAL

logger = logging.getLogger()
logger.setLevel(logging.DEBUG)

# Close dialog with the customer, reporting fulfillmentState of Failed or Fulfilled ("Thanks, your pizza will arrive in 20 minutes")
def close(session_attributes, fulfillment_state, message):
    if session_attributes == None:
        session_attributes = {}
            
    return {
        "dialogAction": {
            "type": 'Close',
            "fulfillmentState": fulfillment_state,
            "message": message
        }
    }
    '''    
    return {
        "sessionAttributes": session_attributes,
        "dialogAction": {
            "type": 'Close',
            "fulfillmentState": fulfillment_state,
            "message": message
        }
    }
    '''
'''
EVENTS    
'''
def dispatch(intent_request):
    print('request received for userId=%s, intentName=%s'%(intent_request["userId"], intent_request["currentIntent"]))
    session_attributes = intent_request["sessionAttributes"]
    slots = intent_request["currentIntent"]["slots"]
    checkin_type = slots["CheckInOrOut"]
    key = os.environ['AUTH_KEY']
    # Assume that Lex handles check-in and check-out
    if "in" in checkin_type:
        r = requests.post(HOST_URL + "/aws_lambda/therapists/%s/check_in"%intent_request["userId"], data = {'aws_lambda_key':key})
    else:
        r = requests.post(HOST_URL + "/aws_lambda/therapists/%s/check_out"%intent_request["userId"], data = {'aws_lambda_key':key})
    print(r.text)
    
    return close(session_attributes, 'Fulfilled',
        {
            'contentType': 'PlainText', 
            'content': "%s"%(json.loads(r.text)["message"])
        }
    )
'''    
------------------ Main handler -----------------------

# Route the incoming request based on intent.
# The JSON body of the request is provided in the event slot.
'''
def lambda_handler(event, context):
    os.environ['TZ'] = 'America/New_York'
    time.tzset()
    logger.debug('event.bot.name={}'.format(event['bot']['name']))
    ret_val = dispatch(event)
    print(ret_val)
    return ret_val
    
