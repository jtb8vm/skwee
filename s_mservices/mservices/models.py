from django.db import models

# skwee microservice data models

class Url(models.Model):
	# shortened URL value
	short_name = models.CharField(max_length=100, default="")
	# timestamp
	time_created = models.DateTimeField(auto_now_add=True)

	# target urls for different platforms with soecific redirect counts for each
	mobile_target = models.CharField(max_length=300, default="")
	mobile_redirects = models.IntegerField(default=0)

	desktop_target = models.CharField(max_length=300, default="")
	desktop_redirects = models.IntegerField(default=0)

	tablet_target = models.CharField(max_length=300, default="")
	tablet_redirects = models.IntegerField(default=0)