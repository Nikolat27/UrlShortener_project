from django import forms
from .models import Url

class UrlCreateForm(forms.ModelForm):
    class Meta:
        model = Url
        fields = ['long_url', 'expiration_time', "password", "max_usage"]
        widgets = {
            'expiration_date': forms.DateInput(attrs={'type': 'date'}),
        }

    def clean_long_url(self):
        long_url = self.cleaned_data.get("long_url")
        if not long_url:
            raise forms.ValidationError("You have to send the long url")
    
    def clean_max_usage(self):
        max_usage = self.cleaned_data.get("max_usage")
        if max_usage < 0 and max_usage is not None:
            raise forms.ValidationError("Max usage`s value must be Positive or null")
    
    def clean(self):
        cleaned_data = super().clean()
        return cleaned_data
    