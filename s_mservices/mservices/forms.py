from django import forms
from mservices.models import Url

class CreateShortenedURL(forms.ModelForm):
	desktop_target = forms.CharField(required=True)
	mobile_target = forms.CharField(required=False)
	tablet_target = forms.CharField(required=False)
	# all other fields generated by skwee
	class Meta:
		model = Url
		exclude = ["short_name", "time_created", "redirect_count"]