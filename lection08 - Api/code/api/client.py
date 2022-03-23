import logging
from urllib.parse import urljoin

import requests
from requests.cookies import cookiejar_from_dict

logger = logging.getLogger('test')

MAX_RESPONSE_LENGTH = 300


class InvalidLoginException(Exception):
    pass


class RespondErrorException(Exception):
    pass


class ResponseStatusCodeException(Exception):
    pass


class ApiClient:

    def __init__(self, base_url, user, password):
        self.base_url = base_url
        self.user = user
        self.password = password

        self.session = requests.Session()

        self.csrf_token = None
        self.sessionid_gtp = None

    #  общий метод для осуществления get и post запросов
    def _request(self, method, location, headers=None, data=None, expected_status=200, jsonify=True, params=None):
        # Формируем URL
        url = urljoin(self.base_url, location)

        # Делаем запрос
        response = self.session.request(method=method, url=url, headers=headers, data=data, params=params)

        # Проверяем код возврата
        if response.status_code != expected_status:
            raise ResponseStatusCodeException(f'Got {response.status_code} {response.reason} for URL "{url}"')

        if jsonify:
            # Приводим к словарю, если стоит флаг jsonify
            json_response = response.json()
            if json_response.get('bStateError', False):
                error = json_response['sErrorMsg'] or 'Unknown'
                raise RespondErrorException(f'Request {url} returned error {error}!')

            return json_response

        return response

    def get_token(self):
        headers = self._request(method='GET', location=self.base_url, jsonify=False).headers['Set-Cookie'].split(';')
        token_header = [h for h in headers if 'csrftoken' in h]
        if not token_header:
            raise Exception('No csrftoken found in main page headers')

        token_header = token_header[0]
        return token_header.split('=')[-1]

    def post_login(self, set_session=True):
        self.csrf_token = self.get_token()

        headers = {
            'X-CSRFToken': f'{self.csrf_token}',
            'Cookie': f'csrftoken={self.csrf_token}',
        }

        data = {
            'login': self.user,
            'password': self.password
        }

        resp = self._request('POST', 'login/', headers=headers, data=data, jsonify=False)

        if not set_session:
            return resp.json()

        try:
            resp_cookies = resp.headers['Set-Cookie'].split(';')
            new_csrf_token = [c for c in resp_cookies if 'csrftoken' in c][0].split('=')[-1]
            self.csrf_token = new_csrf_token
            sessionid_gtp = [c for c in resp_cookies if 'sessionid_gtp' in c][0].split('=')[-1]

            self.session.cookies = cookiejar_from_dict({
                'csrftoken': new_csrf_token,
                'sessionid_gtp': sessionid_gtp
            })
        except Exception as e:
            raise InvalidLoginException(e)

        return resp.json()

    def post_topic_create(self, blog_id, title, text, publish=True):

        data = {
            'csrfmiddlewaretoken': f'{self.csrf_token}',
            'blog': blog_id,
            'title': title,
            'text': text,
            'publish': 'on' if publish else ''
        }

        return self._request('POST', location='blog/topic/create/', data=data)

    def get_feed(self, feed_type='all'):
        params = {'type': feed_type}
        return self._request(method='GET', location='feed/update/stream/', params=params)

    def post_topic_delete(self, topic_id):
        data = {
            'csrfmiddlewaretoken': self.csrf_token,
            'submit': 'Удалить',
        }
        return self._request('POST', f'/blog/topic/delete/{topic_id}/', data=data, jsonify=False)

    def get_topic(self, topic_id, absent=False):
        location = f'/blog/topic/view/{topic_id}/'

        return self._request('GET', location, jsonify=False, expected_status=404 if absent else 200)
