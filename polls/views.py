from django.http import HttpResponse
from .models import connection
import requests


def post(request, process, action, *args, **kwargs):
    conn = getConnectionString(method="POST", process=process, action=action)
    response = requests.post(conn, data=request.body)
    print(response.status_code)
    print(response.content)
    return HttpResponse(response.content)


def put(request, process, action, id, *args, **kwargs):
    conn = getConnectionString(
        method="PUT", process=process, action=action, id=id)
    response = requests.put(conn, data=request.body)
    print(response.status_code)
    print(response.content)
    return HttpResponse(response.content)


def get(request, process, action, id, *args, **kwargs):
    print(request)
    conn = getConnectionString(
        method="GET", process=process, action=action, id=id, params="")
    response = requests.get(conn, data=request.body)
    print(response.status_code)
    print(response.content)
    return HttpResponse(response.content)


def delete(request, process, action, id, *args, **kwargs):
    conn = getConnectionString(
        method="DELETE", process=process, action=action, id=id)
    response = requests.delete(conn, data=request.body)
    print(response.status_code)
    print(response.content)
    return HttpResponse(response.content)


def getConnectionString(method, process, action, id, params):
    conn = connection.objects.get(method=method, process=process, ind_activo=1)

    list = ["http://", conn.server, ":",
            str(conn.port), "/api/", process, "/", action]

    if id is not None and len(id) > 0 and id != "0":
        list.append("/" % id)

    if id is not None and len(params) > 0:
        list.append("?" % params)

    return "".join(list)
