from django.core.handlers.wsgi import WSGIRequest
from django.http import HttpResponse
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from .models import connection
import django_gateway_api
import requests
import json
import base64


def handler(request, process, action, *args, **kwargs):
    print(request)
    params = json.loads(request.body)
    try:
        id_req = json.loads(params['parameters'])['id']
    except:
        id_req = ""

    if request.method == 'POST':
        return post(request, process, action, *args, **kwargs)
    elif request.method == 'PUT':
        return post(request, process, action, str(id_req), *args, **kwargs)
    elif request.method == 'GET':
        return get(request, process, action, str(id_req), *args, **kwargs)
    elif request.method == 'DELETE':
        return delete(request, process, action, str(id_req), *args, **kwargs)

# @csrf_exempt


def post(request, process, action, *args, **kwargs):
    data = json.loads(request.body)
    token = auth_token(data['user'], process, action)
    post_data = {
        'process': data['process'],
        'action': data['action'],
        'data': data['data'],
        'parameters': data['parameters'],
        'user': data['user'],
    }

    conn = getConnectionString(
        method="POST", process=process, action=action, id_req=None, params="")
    response = requests.post(url=conn,
                             data=json.dumps(post_data),
                             headers={'Content-Type': 'application/json'},
                             auth=('admin', token))
    return HttpResponse(response.content)

# @csrf_exempt


def put(request, process, action, id_req, *args, **kwargs):
    data = json.loads(request.body)
    token = auth_token(data['user'], process, action)
    put_data = {
        'process': data['process'],
        'action': data['action'],
        'data': data['data'],
        'parameters': data['parameters'],
        'user': data['user'],
    }

    conn = getConnectionString(
        method="PUT", process=process, action=action, id_req=id_req, params="")
    response = requests.put(url=conn,
                            data=json.dumps(put_data),
                            headers={'Content-Type': 'application/json'},
                            auth=('admin', token))
    return HttpResponse(response.content)

# @csrf_exempt


def get(request, process, action, id_req, *args, **kwargs):
    data = json.loads(request.body)
    token = auth_token(data['user'], process, action)
    try:
        get_data = {
            'process': data['process'],
            'action': data['action'],
            'data': data['data'],
            'parameters': data['parameters'],
            'user': data['user'],
        }
    except:
        get_data = {
            'token': token
        }
    conn = getConnectionString(
        method="GET", process=process, action=action, id_req=id_req, params="")

    response = requests.get(url=conn,
                            data=json.dumps(get_data),
                            headers={'Content-Type': 'application/json'},
                            auth=('admin', token))
    print(response)
    return HttpResponse(response.content)

# @csrf_exempt


def delete(request, process, action, id_req, *args, **kwargs):
    data = json.loads(request.body)
    token = auth_token(data['user'], process, action)
    delete_data = {
        'process': data['process'],
        'action': data['action'],
        'data': data['data'],
        'parameters': data['parameters'],
        'user': data['user'],
    }

    conn = getConnectionString(
        method="DELETE", process=process, action=action, id_req=id_req, params="")
    response = requests.delete(url=conn,
                               data=json.dumps(delete_data),
                               headers={'Content-Type': 'application/json'},
                               auth=('admin', token))

    return HttpResponse(response.content)


def getConnectionString(method, process, action, id_req, params):
    conn = connection.objects.get(method=method, process=process, ind_activo=1)
    list = ["http://", conn.server, ":",
            str(conn.port), "/api/", process, "/", action]
    if id_req is not None and len(id_req) > 0:  # and id_req != "0":
        list.append("".join(["/", str(id_req)]))
    if params is not None and len(params) > 0:
        list.append("?" % params)
    return "".join(list)


def auth_token(user, process, action):
    # TODO: Must send the request to the auth provider to get the token for the user and check if has permission to the requested url
    try:
        authorized = True
    except:
        authorized = False

    if (authorized):
        return base64.b64encode(process.encode('utf-8')).decode('utf-8')
    else:
        return ''
