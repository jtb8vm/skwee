from django.shortcuts import render
from django.http import HttpResponse, JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.forms import model_to_dict
from mservices.models import Url
from mservices.forms import CreateShortenedURL
import string

def success_response(data):
	return JsonResponse({"success":True, "data":data})

def error_response(message):
	return JsonResponse({"success":False, "error":message})

# helper function to map IDs to short alphanumeric names
def shortname(id):
	digs = [] # digits
	alphabet = string.digits + string.ascii_letters
	# convert the id to the base of the alphabet, 62 for ([0-9a-zA-Z])
	while id > 0:
		digs.append(alphabet[id % 62])
		id = id // 62
	digs.reverse()
	short_id = "".join(str(dig) for dig in digs)
	return short_id

@csrf_exempt
def post_url(request):
	if request.method == "POST":
		# django form to help with input validation
		create_url = CreateShortenedURL(request.POST)
		if create_url.is_valid():
			try:
				existing_url = Url.objects.get(desktop_target=create_url.cleaned_data["desktop_target"])
				return error_response("URL already exists")
			except:
				url = create_url.save() # save so we can get out the id
				url_id = model_to_dict(url)["id"]
				url.short_name = shortname(url_id)
				url.save()
				return success_response(model_to_dict(url))
		else:
			return error_response(create_url.errors)
	else:
		return error_response("invalid HTTP method type")

@csrf_exempt
def redirect(request, shortname):
	if request.method == "GET":
		# lookup the shortname
		try:
			url = Url.objects.get(short_name=shortname)
			url_dict = model_to_dict(url)

			# redirect to the url based on platform (using django user agents)
			if (request.user_agent.is_mobile):
				return success_response(url_dict["mobile_target"])

			if (request.user_agent.is_tablet):
				return success_response(url_dict["tablet_target"])

			if(request.user_agent.is_pc):
				return success_response(url_dict["desktop_target"])

			return success_response(request.user_agent.is_mobile)
		except:
			return error_response("Shortened url not found.")
	else:
		return error_response("invalid HTTP method type")

@csrf_exempt
def get_urls(request):
	if request.method == "GET":
		urls = Url.objects.all().values()
		return success_response([url for url in urls])
	else:
		return error_response("invalid HTTP method type")