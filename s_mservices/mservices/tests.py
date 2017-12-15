from django.test import TestCase, Client
import json


MSERVICES_VM_URL = "http://192.168.99.100:8000/" # Docker Toolbox
MSERVICES_NATIVE_URL = "http://0.0.0.0:8000/" # Docker for Windows, Mac (Native)
MSERVICES_URL = ""

# Create your tests here.
class getUrls(TestCase):

	def test_get_urls_success(self):
		print('Testing get URLs return code...')
		try:
			response = self.client.get(MSERVICES_NATIVE_URL + 'get_urls')
			MSERVICES_URL = MSERVICES_NATIVE_URL
		except:
			response = self.client.get(MSERVICES_VM_URL + 'get_urls')
			MSERVICES_URL = MSERVICES_VM_URL
		self.assertEqual(response.json()["success"], True)

class postUrl(TestCase):

	def test_post_url_success(self):
		print('Testing post URL return code...')
		params = {
			"desktop_target" : "http://www.purple.com"
		}
		try:
			response = self.client.post(MSERVICES_NATIVE_URL + 'post_url', params)
			MSERVICES_URL = MSERVICES_NATIVE_URL
		except:
			response = self.client.post(MSERVICES_VM_URL + 'post_url', params)
			MSERVICES_URL = MSERVICES_VM_URL
		self.assertEqual(response.json()["success"], True)