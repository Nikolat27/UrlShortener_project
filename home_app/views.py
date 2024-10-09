from django.shortcuts import render
from django.views.decorators.csrf import csrf_exempt
from django.http import JsonResponse
import json
# Create your views here.

@csrf_exempt
def home_page(request):
    if request.method == "POST":
        data = json.loads(request.body)
        long_url = data.get("long_url")
        expiration_date = data.get("expiration_date")
        password = data.get("password")
        max_usage = data.get("max_usage")

        return JsonResponse({"data": long_url})

    return render(request, "home_app/index.html", context={"username": request})