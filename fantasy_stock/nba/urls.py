from django.urls import path
import nba.views

urlpatterns = [
    path('', nba.views.dashboard),
    path('players/', nba.views.all_players)
]