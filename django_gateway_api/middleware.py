import json
from django.http import HttpResponseBadRequest
# from rest_framework.authentication import TokenAuthentication
# from rest_framework.exceptions import AuthenticationFailed
from polls.models import connection


def get_connection_config(method, body, data):
    config_to_send = {}
    try:
        for key, value in body.items():
            config_to_send[key] = data[key]

        return json.dumps(config_to_send)
    except Exception as e:
        if method == 'GET':
            return {}
        else:
            raise e


def get_connection_headers(config, headers):
    for key, value in config.items():
        if key not in headers:
            raise Exception(f"Missing Header {key}")

    return headers


class BodyValidationMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        if 'api' in request.path and request.method in ('POST', 'PUT', 'GET', 'DELETE'):
            body = request.body

            body = json.loads(body)

            process = body['process']

            conn = connection.objects.get(
                method=request.method, process=process, ind_activo=1)

            if conn is None or process not in request.path:
                return HttpResponseBadRequest('Invalid Request')

            try:
                headers = request.headers

                reqheaders = {}

                if conn.headers != '{}':
                    reqheaders = json.loads(conn.headers)

                headers_to_send = get_connection_headers(reqheaders, headers)

                request._headers = headers_to_send

            except Exception as e:
                return HttpResponseBadRequest(e)

            try:
                reqbody = {}

                reqparameters = {}

                if conn.body != '{}':
                    reqbody = json.loads(conn.body)

                if conn.params != '{}':
                    reqparameters = json.loads(conn.params)

                body_to_send = get_connection_config(
                    request.method, reqbody, json.loads(body['data']))

                parameters_to_send = get_connection_config(
                    request.method, reqparameters, json.loads(body['parameters']))

                body['data'] = body_to_send

                body['parameters'] = parameters_to_send

            except json.JSONDecodeError:
                return HttpResponseBadRequest('Invalid JSON')

            request._body = json.dumps(body).encode('utf-8')

            request._parameters = parameters_to_send

            response = self.get_response(request)

        elif 'admin' in request.path:
            response = self.get_response(request)

        else:
            response = self.get_response(request)

        return response

# class TokenAuthenticationMiddleware:
#    def __init__(self, get_response):
#        self.get_response = get_response
#        self.token_auth = TokenAuthentication()
#
#    def __call__(self, request):
#        if not request.user.is_authenticated:
#            try:
#                user_auth = self.token_auth.authenticate(request)
#
#                if user_auth is not None:
#                    request.user = user_auth[0]
#            except AuthenticationFailed:
#                pass
#
#        response = self.get_response(request)
#       return response
