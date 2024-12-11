from flask import make_response, jsonify

def response(json):
    formatedresponse = make_response(jsonify(json))
    return formatedresponse

