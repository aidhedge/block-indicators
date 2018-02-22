import os
from flask import Flask
from flask import jsonify
from flask import request
import json
from cerberus import Validator
from exceptions import payLoadIsMissing
from exceptions import malformedJson
from exceptions import payloadNotMatchingSchema
from exceptions import indicatorNotPresent
import indicators
from logger import Logger
LOG = Logger()

app = Flask(__name__)


@app.errorhandler(indicatorNotPresent)
@app.errorhandler(payLoadIsMissing)
@app.errorhandler(payloadNotMatchingSchema)
@app.errorhandler(malformedJson)
def handle_invalid_usage(error):
    response = jsonify(error.to_dict())
    response.status_code = error.status_code
    return response


''' payload_output_schema =  {
                        'success': {'type': 'boolean', 'required': True},
                        'payload': {'type': 'dict', 'required': True, 'schema': {
                            {'value':{'type':'number', 'required': True}}, 
                            {'country':{'type':'string', 'required': True}}
                            }
                            }
                        } '''

payload_input_schema = {
                    'country': {'type': 'list', 'required': False}
                    }



@app.route("/ping")
def ping():
    return "Pong!"

@app.route("/schema")
def schema():
    return json.dumps(dict(input=payload_input_schema))

@app.route("/", methods=['GET'])
def index():
    return 'Block-indicators'

@app.route("/<indicator>", methods=['POST'])
def simulate(indicator):
    v = Validator()
    v.schema = payload_input_schema
    payload = request.form.get('payload', None)
    LOG.console(payload)
    if not(payload):
        raise payLoadIsMissing('There is no payload', status_code=500)
    try:
        payload = json.loads(payload)
    except:
        raise malformedJson("Payload present but malformed: {}".format(payload))
    if v(payload):
        if indicator == 'interest':
            data = indicators.interest_rate(payload['country'])
        elif indicator == 'inflation':
            data = indicators.inflation(payload['country'])
        else:
            raise indicatorNotPresent("Didn't find indicator '{}'".format(indicator))
        res = dict(success=True,payload=data)
        return json.dumps(res)
    else:
        raise payloadNotMatchingSchema("Payload didn't match schema ({}\n{})".format(payload_input_schema, v.errors))
        

if __name__ == "__main__":
    port = int(os.environ.get('PORT'))
    app.run(host='0.0.0.0', port=port)