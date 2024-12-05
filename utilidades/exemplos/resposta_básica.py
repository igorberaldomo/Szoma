from flask import make_response, jsonify

def resposta_básica(json):
    formatedresponse = make_response(jsonify(json))
    return formatedresponse

