from django.shortcuts import render
from django.http import HttpResponse, JsonResponse
from django.views.decorators.csrf import csrf_exempt
from mservices.models import Url
from mservices.forms import CreateShortenedURL

# Create your views here.
def success_response(data):
	return JsonResponse({"success":True, "data":data})

def error_response(message):
	return JsonResponse({"success":False, "error":message})

@csrf_exempt
def post_url(request):
	if request.method == "POST":
		create_url = CreateShortenedURL(request.POST)
		if create_url.is_valid():
			# TODO: generate the shortened URL, stick into DB

			return success_response("test post success")
		else:
			return error_response("formatting error")
	else:
		return error_response("did not recieve post")

@csrf_exempt
def get_url(request):
	if request.method == "GET":
		return success_response("test get success")
	else:
		return error_response("did not recieve get")