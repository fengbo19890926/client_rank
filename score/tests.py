import json

from django.test import TestCase

# Create your tests here.


class ClientScoreTests(TestCase):
    def setUp(self):
        print('start')

    def test_client_score_post(self):
        print('start_post')
        url = 'http://127.0.0.1:8000/client_score'
        request_data = {'client_name': '客户端1', 'score': 1}
        response = self.client.post(url, json.dumps(request_data), content_type="application/json")
        self.assertEquals(response.status_code, 201)

    def test_client_score_get(self):
        print('start_get')
        url = 'http://127.0.0.1:8000/client_score'
        response = self.client.get(url, data={'client_name': '客户端1'})
        response_data = response.status_code
        self.assertEquals(response_data, 200)
        print(response.content.decode())

    def tearDown(self):
        print('finished')
