from django.http.response import HttpResponseRedirect
from django.shortcuts import render
from django.contrib.auth import authenticate, login, logout
from django.urls.base import reverse
from django.contrib.auth.decorators import login_required
from django.core.mail import send_mail
from django.views import defaults
from .models import User, MobilePhone
import pyotp
# Create your views here.
@login_required(login_url='login')
def index(request):
    # Fetch user account
    user = User.objects.get(username=request.user.username)
    # if user is verified redirect to products page else redirect to verification page
    if user.is_verified:
        # Fetch available mobile phones in the database
        products = MobilePhone.objects.all()
        return render(request, "mobile_store/products.html", {
            "products": products
            })
    else:
        return HttpResponseRedirect(reverse('verify'))

def login_view(request):
    # If user submits the login form
    if request.method == "POST":

        # Attempt to sign user in
        username = request.POST["username"]
        password = request.POST["password"]
        user = authenticate(request, username=username, password=password)

        # Check if authentication successful
        if user is not None:
            login(request, user)
            return HttpResponseRedirect(reverse("index"))
        else:
            return render(request, "mobile_store/login.html", {
                "message": "Invalid username and/or password."
            })
    else:
        return render(request, "mobile_store/login.html")

def logout_view(request):
    logout(request)
    return HttpResponseRedirect(reverse("index"))


def sign_up(request):
    # If user submits the signup form
    if request.method == "POST":
        # Fetch form values
        username = request.POST["username"]
        email = request.POST["email"]
        first_name = request.POST["firstname"]
        last_name = request.POST["lastname"]


        # Ensure password matches confirmation
        password = request.POST["password"]
        confirmation = request.POST["confirmation"]
        if password != confirmation:
            return render(request, "mobile_store/signup.html", {
                "message": "Passwords must match."
            })
        # Generate OTP
        print("here 1")
        hotp = pyotp.HOTP('base32secret3232')

        # Attempt to create new user 
        try:
            user = User.objects.create_user(username, email, password, first_name=first_name, last_name=last_name)
            user.save()
            user_otp = hotp.at(user.id)
            user.otp = user_otp
            user.save(update_fields=['otp'])
            # If user creation successful, send otp as email to the user
            response = send_mail(
                'The Mobile Store - OTP Token',
                f"Your OTP for the mobile store is {user_otp}",
                'pramitsingh872@gmail.com',
                [str(email)],
                fail_silently=True,
            )
            print("Here 2")
            if response != 1:
                return render(request, "mobile_store/signup.html", {
                    "message": "Failed to send otp. Please try again"
                })
        except:
            return render(request, "mobile_store/signup.html", {
                "message": "Username already taken."
            })
        # Log the user in and redirect them to homepage
        login(request, user)
        return HttpResponseRedirect(reverse("index"))
    else:
        return render(request, "mobile_store/signup.html")
@login_required(login_url='login')
def verify(request):
    if request.method == "POST":
        try:
            # Fetch the current logged in user
            current_user = User.objects.get(username=request.user.username)
            # Fetch the input OTP
            form_otp = request.POST["otp"]

            if form_otp == current_user.otp:
                current_user.is_verified = True
            else:
                current_user.is_verified = False
            current_user.save(update_fields=["is_verified"])
        # In case of any errors return cannot verify
        except:
            return render(request, "mobile_store/verification.html", {
                "message": "Cannot verify user. Please try again later"
                })
        # If everything passes successfully, redirect user to index
        return HttpResponseRedirect(reverse('index'))
    else:
        # If user is not submitting form redirect user to verification page
        return render(request, "mobile_store/verification.html")
@login_required(login_url='login')
def product_page(request, product_id):
    # Fetch product from product id from database
    product = MobilePhone.objects.get(pk=product_id)
    if product is not None:
        return render(request, "mobile_store/product_page.html", {
            "product": product
            })
    else:
        return defaults.page_not_found()

def sell_phones(request):
    # If user submit's the sell form
    if request.method == "POST":
        # Fetch the details of mobile phone
        model_name = request.POST["modelname"]
        model_memory = request.POST["modelmemory"]
        model_storage = request.POST["modelstorage"]
        model_display = request.POST["modeldisplay"]
        model_price = request.POST["modelprice"]
        model_image = request.POST["modelimage"]
        model_camera = request.POST['modelcamera']
        model_seller = request.user
        # Create mobile phone object
        mobile = MobilePhone(
                model_name=model_name,
                camera_spec=model_camera,
                model_ram=model_memory,
                model_storage=model_storage,
                model_display=model_display,
                model_price=int(model_price),
                model_seller=model_seller,
                model_image=model_image,
            )
        # Save mobile phone to database
        mobile.save()
        # Redirect to index
        return HttpResponseRedirect(reverse('index'))
    else:
        return render(request, "mobile_store/sell.html")
