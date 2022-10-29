from django.shortcuts import render
from django.http import HttpResponse

import df




# Create your views here.

def nba_players(request) -> HttpResponse:
    """
    Returns an HTML response of NBA Players
    """
    return HttpResponse(df.players_df().to_json(orient='table'), content_type='application/json')


def nba_player_by_playerid(request, playerid) -> HttpResponse:
    """
    Returns an HTML response of a specified NBA player.
    Paramaters: playerid
    """
    player = df.players_df().loc[int(playerid)]
    return HttpResponse(player.to_json(), content_type='application/json')


def nba_player_by_team(request, team) -> HttpResponse:
    """
    Returns an HTML response of a specified NBA Player
    Paramaters: team
    """
    player = df.players_df().loc[df.players_df()['team'] == team]
    return HttpResponse(player.to_json(orient='table'), content_type='application/json')


def nba_rookies(request) -> HttpResponse:
    """
    Returns the season NBA rookies
    """
    players = df.players_df().loc[df.players_df()['isRookie'] == True]
    return HttpResponse(players.to_json(orient='table'), content_type='application/json')


def nba_teams(request) -> HttpResponse:
    """
    Returns an HTML response of NBA Teams
    """
    return HttpResponse(df.teams_df().to_json(orient='table'), content_type='application/json')


def nba_teams_by_teamid(request, teamid) -> HttpResponse:
    """
    Returns a specific team
    Paramaters: teamid
    """
    team = df.teams_df().loc[int(teamid)]
    return HttpResponse(team.to_json(), content_type='application/json')


def nba_schedule(request) -> HttpResponse:
    """
    Returns an HTML response of NBA Schedule
    """
    return HttpResponse(df.schedule_df().to_json(orient='table'), content_type='application/json')