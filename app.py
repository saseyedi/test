import bottle
import json
import jsonschema
from bottle import request, response
from bottle import post, get, delete
from jsonschema import validate
from validators.task_form_validator import schema

app = bottle.Bottle()

@post('/v1/create_task')
def create_task():
    try:        
        data = request.json
        validate(instance=data, schema=schema)
    except jsonschema.exceptions.ValidationError as ve:
        detail = ve.message
        return json.dumps({"error_message": detail})


@delete('/v1/delete_task')
def delete_task():
    try:
        data = request.json
        validate(instance=data, schema=schema)
    except jsonschema.exceptions.ValidationError as ve:
        detail = ve.message
        return json.dumps({"error_message": detail})


@post('/v1/user_login')
def user_login():
    try:
        data = request.json
        validate(instance=data, schema=schema)

    except jsonschema.exceptions.ValidationError as ve:
        detail = ve.message
        return json.dumps({"error_message": detail})


@post('/v1/user_register')
def user_register():
    try:
        data = request.json
        validate(instance=data, schema=schema)
    except jsonschema.exceptions.ValidationError as ve:
        detail = ve.message
        return json.dumps({"error_message": detail})


def json_response(body='', **kwargs):
    kwargs['body'] = json.dumps(body or kwargs['body']).encode('utf-8')
    kwargs['content_type'] = 'text/json'
    return response(**kwargs)

if __name__ == '__main__':
    bottle.run(server='gunicorn', host='127.0.0.1', port=8000, reloader=True)
