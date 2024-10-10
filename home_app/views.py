from django.shortcuts import render
from django.views.decorators.csrf import csrf_exempt
from django.http import JsonResponse
import json
import string
import random
from django.http import HttpResponse
from .models import Url
# Create your views here.

@csrf_exempt
def home_page(request):
    if request.method == "POST":
        data = json.loads(request.body)
        long_url = data.get("long_url")
        expiration_date = data.get("expiration_date")
        password = data.get("password")
        max_usage = data.get("max_usage")

        short_url = url_shortener(length=5)
        Url.objects.create(long_url=long_url, short_url=short_url)
        return JsonResponse({"data": long_url})

    return render(request, "home_app/index.html", context={"username": request})


def url_shortener(length):
    chars_available = string.ascii_letters + string.digits # 5 length = 961 mil possible urls
    # 6 length = 585 bil possible urls
    new_url = []
    for _ in range(int(length)):
        new_url.append(random.choice(chars_available))
    
    return "".join(new_url)