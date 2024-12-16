import requests

URL = 'https://quizplease.ru'

class QuizAPI:
    def __init__(self, url=URL):
        self.url = URL

    def _get_request(self, endpoint, headers=None, parameters=None):
        headers = headers or {}
        parameters = parameters or {}
        full_url = f'{self.url}{endpoint}'
        response = requests.get(url=full_url, headers=headers, params=parameters)
        return response.json()

    def cities(self):
        endpoint = '/api/city'
        return self._get_request(endpoint=endpoint)
