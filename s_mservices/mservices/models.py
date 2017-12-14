from django.db import models

# skwee microservice data models

class Url(models.Model):
	# shortened URL value
	short_name = models.CharField(max_length=100, default="")
	# timestamp
	time_created = models.DateTimeField(auto_now_add=True)
	# keep track of redirects
	redirect_count = models.IntegerField(default=0)

	# target urls for different platforms
	mobile_target = models.CharField(max_length=300, default="")
	desktop_target = models.CharField(max_length=300, default="")
	tablet_target = models.CharField(max_length=300, default="")