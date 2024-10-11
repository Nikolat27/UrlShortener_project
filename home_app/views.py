from django.shortcuts import render, get_object_or_404
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse
import json
import string
import random
from django.http import HttpResponse
from .models import Url
import redis

# Create your views here.

# redis_client = redis.Redis(host="127.0.0.1:6379", db=0)

def home_page(request):
    if request.user.is_authenticated:
        user_urls = Url.objects.filter(user=request.user)
    else:      
        session_id = request.session.get('anonymous_user')
        user_urls = Url.objects.filter(session_id=session_id)
    
    return render(request, "home_app/index.html", context={"user_urls": user_urls})


@csrf_exempt
def create(request):
    if request.method == "POST":
        data = json.loads(request.body)

        # Validate input (optional, but highly recommended)
        long_url = data.get("long_url")
        if not long_url:
            return JsonResponse({"error": "Long URL is required"}, status=400)

        expiration_date = data.get("expiration_date", None)
        password = data.get("password", None)
        max_usage = data.get("max_usage", None)  # Handle the potential null/empty value
        short_url = url_shortener(length=5)
    
        expiration_date = None if not expiration_date else expiration_date
        password = None if not password else password
        max_usage = None if not max_usage else max_usage

        # Create the URL object 
        if request.user.is_authenticated:
            url_obj = Url.objects.create(
                user=request.user,
                long_url=long_url,
                short_url=short_url,
                expiration_time=expiration_date,
                password=password,
                max_usage=max_usage,
            )
        else:
            # Use session for anonymous users
            session_id = request.session.get("anonymous_user")
            if not session_id:
                session_id = random.randint(10000, 99999)
                request.session["anonymous_user"] = session_id
                request.session.save()

            url_obj = Url.objects.create(
                session_id=session_id,
                long_url=long_url,
                short_url=short_url,
                expiration_time=expiration_date,
                password=password,
                max_usage=max_usage,
            )

        return JsonResponse({"data": {"shortened_url": short_url}})
    else:
        return JsonResponse({"error": "Method not allowed"}, status=405)



def url_shortener(length):
    chars_available = (
        string.ascii_letters + string.digits
    )  # 5 length = 961 mil possible urls
    # 6 length = 585 bil possible urls
    new_url = []
    for _ in range(int(length)):
        new_url.append(random.choice(chars_available))

    return "".join(new_url)


@csrf_exempt
def update_url(request, short_url):
    if request.method == "PUT":
        data = json.loads(request.body)
        updated_long_url = data.get("updatedLongUrl")
        updated_expiration_date = data.get("updatedExpireDate")
        updated_password = data.get("updatedPassword")
        updated_max_usage = data.get("updatedMaxUsage")

        try:
            url_obj = Url.objects.get(short_url=short_url)
        except Url.DoesNotExist:
            return JsonResponse({"error": "URL not found"}, status=404)

        if updated_long_url:
            url_obj.long_url = updated_long_url
        if updated_expiration_date:
            url_obj.expiration_time = updated_expiration_date
        if updated_password:
            url_obj.password = updated_password
        if updated_max_usage is not None:
            url_obj.max_usage = updated_max_usage

        url_obj.save()

        return JsonResponse({"success": "URL updated successfully"})
    else:
        return JsonResponse({"error": "Method not allowed"}, status=405)
        


def delete_url(request, shorted_url):
    instance = get_object_or_404(Url, short_url=shorted_url)
    instance.delete()
    return JsonResponse({"data": "Url deleted successfully!"})

@login_required
def get_user_urls(request):
    user_urls = Url.objects.filter(user=request.user).order_by("-created_at")
    urls_data = []
    for url in user_urls:
        urls_data.append(
            {
                "shortUrl": url.short_url,
                "longUrl": url.long_url,
                "expirationDate": url.expiration_date,
                "password": bool(url.password),  # Convert password to boolean
                "maxUsage": url.max_usage,
            }
        )
    return JsonResponse(urls_data, safe=False)
