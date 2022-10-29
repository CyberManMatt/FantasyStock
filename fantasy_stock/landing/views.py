from django.shortcuts import render

# Create your views here.

def index(request):
    """
    Landing page of the web app.
    """
    return render(request, 'landing.html')