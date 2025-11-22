from django.shortcuts import render, redirect

# Create your views here.
def index(request):
  return render(request, 'index.html')

def cart(request):
  return render(request, 'cart.html')