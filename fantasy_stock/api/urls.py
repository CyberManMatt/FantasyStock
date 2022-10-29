from django.urls import path
import api.views

urlpatterns = [
    path("nba/players/", api.views.nba_players),
    path("nba/players/rookies/", api.views.nba_rookies),
    path("nba/players/<int:playerid>/", api.views.nba_player_by_playerid),
    path("nba/players/<str:team>/", api.views.nba_player_by_team),
    path("nba/schedule/", api.views.nba_schedule),
    path("nba/teams/", api.views.nba_teams),
    path("nba/teams/<int:teamid>/", api.views.nba_teams_by_teamid)
]
