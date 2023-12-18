from django.core.handlers.wsgi import WSGIRequest
from django.http import HttpResponse
from django.http import JsonResponse
from django.http import HttpResponseBadRequest
from django.views.decorators.csrf import csrf_exempt
from .models import connection
from .models import eventlog
import requests
import json
import base64


def handler(request, process, action, *args, **kwargs):
    print('handler request: ', request)
    params = json.loads(request.body)
    try:
        id_req = json.loads(params['parameters'])['id']
    except:
        id_req = ""

    try:
        userid = params['userid']
    except:
        userid = ""

    response = None

    errors = None

    try:
        if request.method == 'POST':
            response = post(request, process, action, *args, **kwargs)
        elif request.method == 'PUT':
            response = post(request, process, action,
                            str(id_req), *args, **kwargs)
        elif request.method == 'GET':
            response = get(request, process, action,
                           str(id_req), *args, **kwargs)
        elif request.method == 'DELETE':
            response = delete(request, process, action,
                              str(id_req), *args, **kwargs)
    except Exception as e:
        print(f"Error: {e}")

        # try:
        #    event = eventlog.objects.create(process=process, action=action, rowid_entity=id_req, userid=userid,
        #                                    request=json.dumps(request), response=None, errors=e)
        #    print(f"Log saved: {event}")
        # except Exception as eventError:
        #    print(f"Log error: {eventError}")

        return HttpResponseBadRequest(e)

    # try:
    #    event = eventlog.objects.create(process=process, action=action, rowid_entity=id_req, userid=userid,
    #                                    request=json.dumps(request), response=json.dumps(response), errors=None)
    #    print(f"Log saved: {event}")
    # except Exception as eventError:
    #    print(f"Log error: {eventError}")

    print('handler response: ', response)
    return HttpResponse(response.content)


# @csrf_exempt


def post(request, process, action, *args, **kwargs):
    data = json.loads(request.body)

    token = auth_token(data['userid'], process, action)
    post_data = {
        'process': data['process'],
        'action': data['action'],
        'data': data['data'],
        'parameters': data['parameters'],
        'userid': data['userid'],
    }

    conn = getConnectionString(
        method="POST", process=process, action=action, id_req=None, params="")
    response = requests.post(url=conn,
                             data=json.dumps(post_data),
                             headers={'Content-Type': 'application/json'},
                             auth=('admin', token),
                             params=json.dumps(data['parameters']))
    return response

# @csrf_exempt


def put(request, process, action, id_req, *args, **kwargs):
    data = json.loads(request.body)
    token = auth_token(data['userid'], process, action)
    put_data = {
        'process': data['process'],
        'action': data['action'],
        'data': data['data'],
        'parameters': data['parameters'],
        'userid': data['userid'],
    }

    conn = getConnectionString(
        method="PUT", process=process, action=action, id_req=id_req, params="")
    response = requests.put(url=conn,
                            data=json.dumps(put_data),
                            headers={'Content-Type': 'application/json'},
                            auth=('admin', token),
                            params=json.dumps(data['parameters']))
    return response

# @csrf_exempt


def get(request, process, action, id_req, *args, **kwargs):
    data = json.loads(request.body)
    token = auth_token(data['userid'], process, action)
    try:
        get_data = {
            'process': data['process'],
            'action': data['action'],
            'data': data['data'],
            'parameters': data['parameters'],
            'userid': data['userid'],
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
                            auth=('admin', token),
                            params=json.dumps(data['parameters']))
    return response

# @csrf_exempt


def delete(request, process, action, id_req, *args, **kwargs):
    data = json.loads(request.body)
    token = auth_token(data['userid'], process, action)
    delete_data = {
        'process': data['process'],
        'action': data['action'],
        'data': data['data'],
        'parameters': data['parameters'],
        'userid': data['userid'],
    }

    conn = getConnectionString(
        method="DELETE", process=process, action=action, id_req=id_req, params="")
    response = requests.delete(url=conn,
                               data=json.dumps(delete_data),
                               headers={'Content-Type': 'application/json'},
                               auth=('admin', token),
                               params=json.dumps(data['parameters']))

    return response


def getConnectionString(method, process, action, id_req, params):
    conn = connection.objects.get(method=method, process=process, ind_activo=1)
    list = ["http://", conn.server]

    if conn.port > 0 and len(str(conn.port)) > 0:
        list.append("".join([":", str(conn.port)]))

    list.append("".join(["/api/", process, "/", action]))

    if id_req is not None and len(id_req) > 0:  # and id_req != "0":
        list.append("".join(["/", str(id_req)]))
    if params is not None and len(params) > 0:
        list.append("?" % params)

    url = "".join(list)

    return url


def auth_token(userid, process, action):
    # TODO: Must send the request to the auth provider to get the token for the userid and check if has permission to the requested url

    try:
        authorized = True
    except:
        authorized = False

    if (authorized):
        if (process == 'Courses' or process == 'Classes'):
            return 'nodejs_courses_api'
        elif (process == 'Files'):
            return 'dotnet_resources_api'
        else:
            return base64.b64encode(process.encode('utf-8')).decode('utf-8')
    else:
        return ''
