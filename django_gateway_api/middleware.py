import json
import socket
import time
import logging

from django.http import HttpResponseBadRequest
from polls.models import connection
from polls.models import eventlog


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

            action = body['action']

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
                try:
                    eventlog.objects.create(process=process, action=action, rowid_entity=0, userid="",
                                            request=json.dumps(request), response=None, errors=e)
                    print(f"Log saved")
                except Exception as eventError:
                    print(f"Log error: {eventError}")
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
                try:
                    eventlog.objects.create(process=process, action=action, rowid_entity=0, userid="",
                                            request=json.dumps(request), response=None, errors="Invalid Body JSON")
                    print(f"Log saved")
                except Exception as eventError:
                    print(f"Log error: {eventError}")

                return HttpResponseBadRequest('Invalid Body JSON')

            request._body = json.dumps(body).encode('utf-8')

            request._parameters = parameters_to_send

            response = self.get_response(request)

            try:
                eventlog.objects.create(process=process, action=action, rowid_entity=0, userid="",
                                        request=json.dumps(request), response=json.dumps(response), errors=None)
                print(f"Log saved")
            except Exception as eventError:
                print(f"Log error: {eventError}")

        elif 'admin' in request.path:
            response = self.get_response(request)

        else:
            response = self.get_response(request)

        return response


request_logger = logging.getLogger(__name__)


class RequestLogMiddleware:
    """Request Logging Middleware."""

    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        start_time = time.monotonic()
        log_data = {
            "remote_address": request.META["REMOTE_ADDR"],
            "server_hostname": socket.gethostname(),
            "request_method": request.method,
            "request_path": request.get_full_path(),
        }

        # Only logging "*/api/*" patterns
        if "/api/" in str(request.get_full_path()):
            req_body = json.loads(request.body.decode(
                "utf-8")) if request.body else {}
            log_data["request_body"] = req_body

        # request passes on to controller
        response = self.get_response(request)

        # add runtime to our log_data
        if response and response["content-type"] == "application/json":
            response_body = json.loads(response.content.decode("utf-8"))
            log_data["response_body"] = response_body
        log_data["run_time"] = time.time() - start_time

        request_logger.info(msg=log_data)
        return response

    # Log unhandled exceptions as well
    def process_exception(self, request, exception):
        try:
            raise exception
        except Exception as e:
            request_logger.exception("Unhandled Exception: " + str(e))
        return exception
