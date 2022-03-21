from urllib.parse import urljoin

import requests
from requests.cookies import cookiejar_from_dict


class ApiClient:

    def __init__(self, base_url, user, password):
        self.base_url = base_url
        self.user = user
        self.password = password

        self.session = requests.Session()

    def get_token(self):
        headers = requests.get(self.base_url).headers['Set-Cookie'].split(';')
        token_header = [h for h in headers if 'csrftoken' in h]
        if not token_header:
            raise Exception('No csrftoken found in main page headers')

        token_header = token_header[0]
        return token_header.split('=')[-1]

    def post_login(self):
        csrf_token = self.get_token()

        headers = {
            'X-CSRFToken': f'{csrf_token}',
            'Cookie': f'csrftoken={csrf_token}',
        }

        data = {
            'login': self.user,
            'password': self.password
        }

        login_url = urljoin(self.base_url, 'login/')
        resp = requests.post(login_url, headers=headers, data=data)

        resp_cookies = resp.headers['Set-Cookie'].split(';')
        new_csrf_token = [c for c in resp_cookies if 'csrftoken' in c][0].split('=')[-1]
        sessionid_gtp = [c for c in resp_cookies if 'sessionid_gtp' in c][0].split('=')[-1]

        self.session.cookies = cookiejar_from_dict({
            'csrftoken' : new_csrf_token,
            'sessionid_gtp': sessionid_gtp
        })

        return resp.json()
