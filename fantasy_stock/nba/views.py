# Create your views here.
from django.shortcuts import render
import requests



# Fantasy Stock front end to return the template
def dashboard(request):
    """
    Returns the NBA dashboard which contains news and the NBA Schedule.
    """
    return render(request, 'dashboard.html')


def all_players(request):
    """
    Returns the data table of the active NBA players for the current season.
    """
    return render(request, 'all_players.html')