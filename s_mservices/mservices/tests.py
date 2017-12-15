from django.test import TestCase, Client
from django.core.urlresolvers import reverse

import urllib.request
import urllib.parse
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

	def test_get_urls_data(self):
		print('Testing get URLs data...')

		# enter data into dB ( would use fixtures, but they're throwing strange errors atm... )

		params = {
			"desktop_target" : "http://www.purple.com"
		}
		try:
			post_response = self.client.post(MSERVICES_NATIVE_URL + 'post_url', params)
			MSERVICES_URL = MSERVICES_NATIVE_URL
		except:
			post_response = self.client.post(MSERVICES_VM_URL + 'post_url', params)
			MSERVICES_URL = MSERVICES_VM_URL

		# test that data returns as expected
		response = self.client.get(MSERVICES_URL + 'get_urls')
		url_response = response.json()["data"][0] # get first URL returned
		self.assertEqual(url_response["desktop_target"], "http://www.purple.com")
		self.assertEqual(url_response["short_name"], "12x") # first shortname based on id = 1

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

	def test_post_url_data_desktop(self):
		print('Testing post URL data...')
		params = {
			"desktop_target" : "http://www.purple.com"
		}
		try:
			response = self.client.post(MSERVICES_NATIVE_URL + 'post_url', params)
			MSERVICES_URL = MSERVICES_NATIVE_URL
		except:
			response = self.client.post(MSERVICES_VM_URL + 'post_url', params)
			MSERVICES_URL = MSERVICES_VM_URL
		expected = {}
		expected["success"] = True
		expected_data = {
			"tablet_target": "",
			"mobile_redirects" : 0,
			"tablet_redirects" : 0,
			"short_name" : "12x",
			"mobile_target": "",
			"desktop_target" : "http://www.purple.com",
			"desktop_redirects": 0,
			"id":1
		}
		expected["data"] = expected_data
		#self.assertEqual(response.json()["data"]["short_name"], expected["data"]["short_name"])
		#self.assertEqual(response.json()["data"]["desktop_target"], expected["data"]["desktop_target"])
		self.assertDictEqual(response.json(), expected)

class redirectUrl(TestCase):
	def test_redirect_counter_desktop(self):
		print('Testing redirect desktop data...')
		params = {
				"desktop_target" : "http://www.purple.com"
			}
		try:
			post_response = self.client.post(MSERVICES_NATIVE_URL + 'post_url', params)
			MSERVICES_URL = MSERVICES_NATIVE_URL
		except:
			post_response = self.client.post(MSERVICES_VM_URL + 'post_url', params)
			MSERVICES_URL = MSERVICES_VM_URL
		# test that data returns as expected
		redir_response = self.client.get(MSERVICES_URL + post_response.json()["data"]["short_name"])
		check_response = self.client.get(MSERVICES_URL + 'get_urls')
		url_response = check_response.json()["data"][0]
		self.assertEqual(url_response["desktop_redirects"], 1)

	def test_redirect_counter_mobile(self):
		print('Testing redirect mobile data...')
		params = {
				"desktop_target" : "http://www.purple.com",
				"mobile_target" : "http://www.google.com"
			}
		try:
			post_response = self.client.post(MSERVICES_NATIVE_URL + 'post_url', params)
			MSERVICES_URL = MSERVICES_NATIVE_URL
		except:
			post_response = self.client.post(MSERVICES_VM_URL + 'post_url', params)
			MSERVICES_URL = MSERVICES_VM_URL
		# test that data returns as expected
		redir_response = self.client.get(MSERVICES_URL + post_response.json()["data"]["short_name"])
		check_response = self.client.get(MSERVICES_URL + 'get_urls')
		url_response = check_response.json()["data"][0]
		self.assertEqual(url_response["mobile_redirects"], 0)
		self.assertEqual(url_response["tablet_redirects"], 0)
		self.assertEqual(url_response["desktop_redirects"], 1)