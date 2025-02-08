from django.shortcuts import render

def index(request):
    return render(request, 'index.html')

def about(request):
    return render(request, 'about.html')

def shop(request):
    return render(request, 'shop.html')

# Add more views as needed