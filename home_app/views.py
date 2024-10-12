from django.shortcuts import render, get_object_or_404, redirect
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth import login, authenticate
from django.contrib.auth.hashers import check_password
from django.contrib.auth.decorators import login_required
from django.views import View
from django.http import JsonResponse
from django.core.serializers import serialize
from django.db.models import F
import json
import string
import secrets
import random
from django.http import HttpResponse
from .models import Url, ApprovalRequest
import redis
from django.views.decorators.http import require_POST
from django.utils import timezone

# Create your views here.

# redis_client = redis.Redis(host="127.0.0.1:6379", db=0)


def home_page(request):
    if not request.user.is_authenticated:
        session_id = request.session.get('anonymous_user')
        user_urls = Url.objects.filter(session_id=session_id)

    user_urls = Url.objects.filter(user=request.user)
    return render(request, "home_app/index.html", context={"user_urls": user_urls})

def redirect_view(request, shorted_url):
    url = get_object_or_404(Url, short_url=shorted_url)

    if url.max_usage and url.max_usage <= url.used_times:
        return HttpResponse("This url Unfortunately has reached its maximum usage!")
        
    if url.expiration_time and url.expiration_time > timezone.now():
        return HttpResponse("This url has been expired!")
    
    if url.requires_approval:
        if not request.user.is_authenticated:
            return redirect("home_app:login_page")
        approval_request, created = ApprovalRequest.objects.get_or_create(
            owner=url.user, user=request.user, url=url)
        if approval_request.approved is False:
            return HttpResponse("This url requires an approval, So pls w8 until the owner approve you request!")

    if url.requires_approval and approval_request.approved is False:
        return HttpResponse("This url requires an approval, So pls w8 until the owner approve you request!")
    elif url.requires_approval and (not request.user.is_authenticated):
        return redirect("home_app:login_page")
    

    if url.password:
        return render(request, "home_app/password_prompt.html", context={"short_url": shorted_url})

    url.used_times = F("used_times") + 1 
    url.save()

    return redirect(url.long_url) 

def login_page(request):
    if request.method != "POST":
        return render(request, "home_app/login.html")
    
     

class LoginPageView(View):
    template_name = "home_app/login.html"
    def get(self, request):
        return render(request, self.template_name)

    def post(self, request):
        username = request.POST.get("username")
        password = request.POST.get("password")
        user = authenticate(username=username, password=password)
        if user is None:
            return render(request, "home_app/login.html", 
                            {"error": "The provided credentials are wrong!",
                            "username": username, 
                            "password": password})

        login(request, user)
        return redirect("home_app:main_page")  
         
@csrf_exempt
def validate_password(request, shorted_url):
    url = get_object_or_404(Url, short_url=shorted_url)

    if not url.password:
        return JsonResponse({'error': 'URL is not password protected'}, status=400)   

    if request.method != "POST":
       return JsonResponse({'error': 'Invalid request method'}, status=405)   

    entered_password = json.loads(request.body).get("password")
    if not entered_password and (check_password(entered_password, url.password) is False):
        return JsonResponse({'error': 'Incorrect password'}, status=400)

    url.used_times = F("used_times") + 1 
    url.save()
    return JsonResponse({'success': True, 'redirect_url': url.long_url})

def pendingApproval_requests(request):
    pending_requests = ApprovalRequest.objects.filter(owner=request.user
                                ).select_related('user', 'url')

    requests = serialize("json", pending_requests, use_natural_primary_keys=True)
    serialized_requests = json.loads(requests)
    return JsonResponse(serialized_requests, safe=False)
    
@login_required
def approve_request(request, pk):
    approval_request = get_object_or_404(ApprovalRequest, id=pk)

    if request.user != approval_request.owner:
        return HttpResponse("You have to be the owner of the url", status=[403])
    
    approval_request.approved = True
    approval_request.save()
    return HttpResponse("OK")

@login_required
def reject_request(request, pk):
    approval_request = get_object_or_404(ApprovalRequest, id=pk)

    if request.user != approval_request.owner:
        return HttpResponse("You have to be the owner of the url", status=[403])
    
    approval_request.approved = False
    approval_request.save()
    return HttpResponse("OK")
    
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
    chars_available = string.ascii_letters + string.digits
    return ''.join([secrets.choice(chars_available) for _ in range(length)])

@csrf_exempt
def get_url_details(request, shorted_url):
    if request.method != "GET":
        return JsonResponse({"error": "Method not allowed"}, status=405)
        
    url_obj = get_object_or_404(Url, short_url=shorted_url)
    return JsonResponse({
        "data": {
            "shortened_url": url_obj.short_url,
            "long_url": url_obj.long_url,
            "expiration_time": url_obj.expiration_time,
            "password": url_obj.password,
            "max_usage": url_obj.max_usage
        }
    })
        
    

@csrf_exempt
def update_url(request, shorted_url):
    if request.method == "PUT":
        data = json.loads(request.body)
        updated_long_url = data.get("updatedLongUrl")
        updated_expiration_date = data.get("updatedExpireDate")
        updated_password = data.get("updatedPassword")
        updated_max_usage = data.get("updatedMaxUsage")

        try:
            url_obj = Url.objects.get(short_url=shorted_url)
        except Url.DoesNotExist:
            return JsonResponse({"error": "URL not found"}, status=404)

        updated_expiration_date = None if not updated_expiration_date else updated_expiration_date
        updated_password = None if not updated_password else updated_password
        updated_max_usage = None if not updated_max_usage else updated_max_usage

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


def delete_url(shorted_url):
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
