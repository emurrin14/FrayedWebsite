from django.shortcuts import render, redirect, get_object_or_404
from django.conf import settings
from django.http import JsonResponse, HttpResponseRedirect, HttpResponseBadRequest
from django.views.decorators.csrf import csrf_exempt
import stripe
from django.utils.timezone import localtime
from .models import Product, Product_Variant, Cart, CartItem, Size, EmailVerificationToken
from .forms import CustomLoginForm, CustomUserCreationForm
import json
from django.views.decorators.http import require_POST
from django.urls import reverse
from django.core.mail import send_mail
from django.contrib.auth.decorators import login_required
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages

stripe.api_key = settings.STRIPE_SECRET_KEY

# Create your views here.
def index(request):
    new_products = Product.objects.filter(tags__name__iexact="New").distinct()
    denim_products = Product.objects.filter(tags__name__iexact="Denim").distinct()
    shirt_products = Product.objects.filter(tags__name__iexact="Shirts").distinct()
    jacket_products = Product.objects.filter(tags__name__iexact="Jackets").distinct()
    context = {
        'new_products': new_products,
        'denim_products': denim_products,
        'shirt_products': shirt_products,
        'jacket_products': jacket_products,
    }
    return render(request, 'index.html', context)


def Product_Detail(request, slug):
   product = get_object_or_404(
        Product.objects.prefetch_related('images', 'variants__size', 'variants__color'), 
        slug=slug
   )
   context = {
        'product': product,
   }
   return render(request, 'product.html', context)


def cart(request):
    cart = get_cart(request)
    items = cart.items.all()
    total = cart.total_price()

    return render(request, 'cart.html', {
        "cart": cart,
        "items": items,
        "total": total,
        "STRIPE_PUBLISHABLE_KEY": settings.STRIPE_PUBLISHABLE_KEY,
    })

def get_cart(request):
    if request.user.is_authenticated:
        cart, created = Cart.objects.get_or_create(user=request.user)
    else:
        session_key = request.session.session_key
        if not session_key:
            request.session.create()
            session_key = request.session.session_key
        cart, created = Cart.objects.get_or_create(session_key=session_key)
    return cart



@require_POST
def add_to_cart(request, product_id):
    cart = get_cart(request)
    product = get_object_or_404(Product, id=product_id)

    variant_id = request.POST.get("variant_id")
    if not variant_id:
        return HttpResponseBadRequest("Variant must be selected.")

    variant = get_object_or_404(Product_Variant, id=variant_id)

    # Read quantity from the form
    quantity = int(request.POST.get("quantity", 1))

    cart_item, created = CartItem.objects.get_or_create(
        cart=cart,
        product=product,
        variant=variant,
        defaults={"quantity": quantity},
    )

    if not created:
        # Increase by the submitted quantity
        cart_item.quantity += quantity
        cart_item.save()

    return JsonResponse({
        "success": True,
        "quantity": cart_item.quantity,
    })




def subtract_from_cart(request, item_id):
    cart_item = get_object_or_404(CartItem, id=item_id)

    if cart_item.quantity > 1:
        cart_item.quantity -= 1
        cart_item.save()
    
    else:
        cart_item.delete()
    
    return redirect("cart")

def remove_from_cart(request, item_id):
    cart_item = get_object_or_404(CartItem, id=item_id)
    cart_item.delete()
    return redirect("cart")


@csrf_exempt
def create_checkout_session(request):
    YOUR_DOMAIN = 'http://localhost:8000'
    if request.method == "POST":
        try:
            checkout_session = stripe.checkout.Session.create(
                line_items=[
                    {
                        'price': 'price_1SUIoeH81M5unIKcxNmKPert',  # replace with Price ID
                        'quantity': 1,
                    },
                ],
                mode='payment',
                success_url=YOUR_DOMAIN + '/success/',
                cancel_url=YOUR_DOMAIN + '/cancel/',
            )
            return HttpResponseRedirect(checkout_session.url)
        except Exception as e:
            return JsonResponse({'error': str(e)})
    else:
        return JsonResponse({'error': 'Invalid request method'})


def success_view(request):
   return render(request, 'success.html')


def cancel_view(request):
   return render(request, 'cancel.html')

# USER LOGIN AND REGISTRATION VIEWS

def signup_view(request):
    if request.method == "POST":
        form = CustomUserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            # Create verification token
            token = EmailVerificationToken.objects.create(user=user)
            # Send verification email
            verification_url = request.build_absolute_uri(
                reverse('verify_email', kwargs={'token': token.token})
            )
            send_mail(
                'Verify your email address',
                f'Please click the following link to verify your email address:\n\n{verification_url}\n\nThis link will expire in 24 hours.',
                settings.DEFAULT_FROM_EMAIL,
                [user.email],
                fail_silently=False,
            )
            messages.success(
                request,
                'Registration successful! Please check your email to verify your account before logging in.'
            )
            return redirect("login")
    else:
        form = CustomUserCreationForm()
    return render(request, "signup.html", {"form": form})


def login_view(request):
    # Redirect if already logged in
    if request.user.is_authenticated:
        return redirect("index")
    
    if request.method == "POST":
        form = CustomLoginForm(data=request.POST)
        if form.is_valid():
            user = form.get_user()
            # Check if email is verified
            if not user.email_verified:
                messages.error(
                    request,
                    'Your email address has not been verified. Please check your email and click the verification link.'
                )
                return render(request, "login.html", {"form": form})
            login(request, user)
            # Redirect to next page if specified, otherwise to index
            next_url = request.GET.get('next', 'index')
            return redirect(next_url)
        else:
            return render(request, "login.html", {"form": form})
    else:
        form = CustomLoginForm()

    return render(request, "login.html", {"form": form})


@login_required
def logout_view(request):
    logout(request)
    return redirect("login")

def verify_email(request, token):
    try:
        verification_token = EmailVerificationToken.objects.get(token=token)
        if verification_token.is_valid():
            user = verification_token.user
            user.email_verified = True
            user.is_active = True
            user.save()
            verification_token.is_used = True
            verification_token.save()
            messages.success(request, 'Your email has been verified successfully! You can now log in.')
            return redirect('login')
        else:
            messages.error(request, 'This verification link has expired or has already been used.')
            return redirect('signup')
    except EmailVerificationToken.DoesNotExist:
        messages.error(request, 'Invalid verification link.')
        return redirect('signup')