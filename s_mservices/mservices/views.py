from django.shortcuts import render, redirect
from django.http import HttpResponse, JsonResponse, HttpResponseRedirect
from django.views.decorators.csrf import csrf_exempt
from django.forms import model_to_dict
from django.utils import timezone
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
	id += 4000 # remove low-digits
	# convert the id to the base of the alphabet, 62 for ([0-9a-zA-Z])
	while id > 0:
		digs.append(alphabet[id % 62])
		id = id // 62
	digs.reverse()
	short_name = "".join(str(dig) for dig in digs)
	return short_name

@csrf_exempt
def post_url(request):
	if request.method == "POST":
		# django form to help with input validation
		create_url = CreateShortenedURL(request.POST)
		if create_url.is_valid():
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
			if (request.user_agent.is_mobile and url_dict["mobile_target"]):
				url.mobile_redirects += 1  # increment the redirect count
				url.save()
				return HttpResponseRedirect(url_dict["mobile_target"])

			elif (request.user_agent.is_tablet and url_dict["tablet_target"]):
				url.tablet_redirects += 1
				url.save()
				return HttpResponseRedirect(url_dict["tablet_target"])

			else:
				url.desktop_redirects += 1
				url.save()
				return HttpResponseRedirect(url_dict["desktop_target"])

			return error_response("Unsupported platform.")
		except Exception as e:
			return error_response(str(type(e)))
	else:
		return error_response("invalid HTTP method type")

@csrf_exempt
def get_urls(request):
	if request.method == "GET":
		urls = Url.objects.all().values()
		for url in urls:

			# generate the 'time since created' field
			created = (timezone.now()-url["time_created"])
			sec = created.total_seconds()
			min = int(sec // 60)
			hour = int(min // 60)
			day = int(hour // 24)

			min = int(min % 60)
			hour = int(hour % 60)
			sec = int(sec % 60)

			time_since = "{}d {}h {}m {}s"
			url["time_since_created"] = time_since.format(day, hour, min, sec)
		return success_response([url for url in urls])
	else:
		return error_response("invalid HTTP method type")

@csrf_exempt
def delete_url(request, id):
	if request.method == "POST":
		try:
			url = Url.objects.get(id=id)
		except:
			return error_response("url with id {} does not exist.".format(id))
		url.delete()
		return success_response("url with id {} deleted".format(id))
	else:
		return error_response("invalid HTTP method type")