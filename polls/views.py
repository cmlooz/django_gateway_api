import json

from django.http import HttpResponse
from django.views.decorators.csrf import csrf_exempt
from .models import connection
import requests

@csrf_exempt
def post(request, process, action, *args, **kwargs):
    print(request)
    data = json.loads(request.body)
    post_data = {
        'process': data['process'],
        'action': data['action'],
        'data': data['data'],
        'parameters':data['parameters'],
        'user':data['user'],
        #For checking the security of the user
        'auth_token':auth_token(data['user'],data['process'],data['action'])
    }
    conn = getConnectionString(method="POST", process=process, action=action,id="0",params="")
    response = requests.post(conn, data=json.dumps(post_data),
                             headers={'Content-Type': 'application/json'})
    return HttpResponse(response.content)

@csrf_exempt
def put(request, process, action, id, *args, **kwargs):
    print(request)
    data = json.loads(request.body)
    put_data = {
        'process': data['process'],
        'action': data['action'],
        'data': data['data'],
        'parameters': data['parameters'],
        'user': data['user'],
        # For checking the security of the user
        'auth_token': auth_token(data['user'],data['process'],data['action'])
    }
    conn = getConnectionString(
        method="PUT", process=process, action=action, id=id,params="")
    response = requests.put(conn, data=json.dumps(put_data),
                             headers={'Content-Type': 'application/json'})
    return HttpResponse(response.content)

@csrf_exempt
def get(request, process, action, id, *args, **kwargs):
    print(request)
    data = json.loads(request.body)
    try:
        get_data = {
            'process': data['process'],
            'action': data['action'],
            'data': data['data'],
            'parameters': data['parameters'],
            'user': data['user'],
            # For checking the security of the user
            'auth_token': auth_token(data['user'],data['process'],data['action'])
        }
    except:
        get_data = {
            # For checking the security of the user
            'auth_token': auth_token(data['user'],data['process'],data['action'])
        }

    conn = getConnectionString(
        method="GET", process=process, action=action, id=id, params="")
    response = requests.get(conn, data=json.dumps(get_data))
    return HttpResponse(response.content)

@csrf_exempt
def delete(request, process, action, id, *args, **kwargs):
    print(request)
    data = json.loads(request.body)
    try:
        delete_data = {
            'process': data['process'],
            'action': data['action'],
            'data': data['data'],
            'parameters': data['parameters'],
            'user': data['user'],
            # For checking the security of the user
            'auth_token': auth_token(data['user'],data['process'],data['action'])
        }
    except:
        delete_data = {
            # For checking the security of the user
            'auth_token': auth_token(data['user'],data['process'],data['action'])
        }
    conn = getConnectionString(
        method="DELETE", process=process, action=action, id=id,params="")
    response = requests.delete(conn, data=json.dumps(delete_data))
    print(response.status_code)
    print(response.content)
    return HttpResponse(response.content)

def getConnectionString(method, process, action, id, params):
    conn = connection.objects.get(method=method, process=process, ind_activo=1)
    list = ["http://", conn.server, ":",
            str(conn.port), "/api/", process, "/", action]
    if id is not None and len(id) > 0 and id != "0":
        list.append("/" % id)
    if params is not None and len(params) > 0:
        list.append("?" % params)
    return "".join(list)

def auth_token(user, process, action):
    #TODO: Must send the request to the auth provider to get the token for the user and check if has permission to the requested url
    return "|".join(user,process, action)