import requests
import json


class RestRequest:
    def __init__(self, certificate=None, proxies=None):
        self.__headers = {
            'Content-Type': 'application/json',
        }
        self.__certificate = None
        if certificate:
            self.__certificate = (
                certificate['crt'],
                certificate['key']
            )
        self.__proxies = proxies

    def _get_headers(self):
        return self.__headers

    def _get_certificate(self):
        return self.__certificate

    def _get_proxies(self):
        return self.__proxies

    def get(self, url, message=None):
        headers = self._get_headers()
        certificate = self._get_certificate()
        proxies = self._get_proxies()

        if not message:
            message = {}

        response = requests.get(url,
                                params=message,
                                headers=headers,
                                cert=certificate,
                                proxies=proxies)
        return response

    def post(self, url, message=None):
        headers = self._get_headers()
        certificate = self._get_certificate()
        proxies = self._get_proxies()

        if not message:
            message = {}

        response = requests.post(url,
                                 data=json.dumps(message),
                                 headers=headers,
                                 cert=certificate,
                                 proxies=proxies)
        return response


class BearerRequest(RestRequest):
    def __init__(self, access_token, certificate=None, proxies=None):
        RestRequest.__init__(self, certificate, proxies)
        headers = self._get_headers()
        headers['Authorization'] = "Bearer {}".format(access_token)
