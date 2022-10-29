import requests
import pandas as pd
import base64
import keys

def players_df() -> pd.DataFrame:
    """
    Returns the dataframe of NBA players and stats. Generates stock price.
    """
    headers={
        "Authorization": "Basic " + base64.b64encode('{}:{}'.format(keys.MYSPORTSFEEDS, "MYSPORTSFEEDS").encode('utf-8')).decode('ascii')
    }
    rq = requests.request("GET", "https://api.mysportsfeeds.com/v2.1/pull/nba/2022-2023-regular/player_stats_totals.json", headers=headers)
    stats_df = pd.json_normalize(rq.json()['playerStatsTotals'])

    # The Jinja template does not parse dot notation in DataFrames, so some column names needs to be changed.
    stats_df = stats_df.rename(columns={
        'player.id': 'playerID',
        'player.firstName': 'firstName',
        'player.lastName': 'lastName',
        'player.primaryPosition': 'position',
        'player.currentTeam.abbreviation': 'team',
        'player.height': 'height',
        'player.weight': 'weight',
        'player.officialImageSrc': 'headshot',
        'player.currentInjury': 'injury',
        'player.currentInjury.description': 'injuryDescription',
        'player.currentInjury.playingProbability': 'playingProbability',
        'player.jerseyNumber': 'jerseyNumber',
        'player.rookie': 'isRookie',
        'stats.gamesPlayed': 'gamesPlayed',
        'stats.miscellaneous.gamesStarted': 'gamesStarted',
        'stats.fieldGoals.fg3PtMadePerGame': 'fg3PtMadePerGame',
        'stats.rebounds.rebPerGame': 'rebPerGame',
        'stats.offense.ptsPerGame': 'ptsPerGame',
        'stats.fieldGoals.fgPct': 'fgPct',
        'stats.freeThrows.ftPct': 'ftPct',
        'stats.defense.blkPerGame': 'blkPerGame',
        'stats.defense.stlPerGame': 'stlPerGame',
        'stats.miscellaneous.foulsPerGame': 'foulsPerGame',
        'stats.defense.tovPerGame': 'tovPerGame',
        'stats.miscellaneous.plusMinusPerGame': 'plusMinusPerGame'
    })

    drop_cols = [
        'player.currentTeam.id',
        'player.birthDate',
        'player.birthCity',
        'player.birthCountry',
        'player.highSchool',
        'player.college',
        'player.handedness.shoots',
        'player.socialMediaAccounts',
        'team.id',
        'team.abbreviation',
        'player.currentRosterStatus'
    ]

    stats_df = stats_df.drop(drop_cols, axis=1)
    stats_df = stats_df.set_index(['playerID'])

    # General Bonus
    games_played_bonus = stats_df['gamesPlayed'] / 82 * 100
    games_started_bonus = stats_df['gamesStarted'] / stats_df['gamesPlayed'] * 100
    plus_minus = stats_df['plusMinusPerGame']
    rebounds_bonus = stats_df['rebPerGame']

    # Offensive Bonuses
    points_bonus = stats_df['ptsPerGame'] * 1.5
    three_bonus = stats_df['fg3PtMadePerGame'] * 3
    fg_bonus = stats_df['fgPct']
    ft_bonus = stats_df['ftPct']

    # Defensive Bonuses
    blocks_bonus = stats_df['blkPerGame'] * 2
    steals_bonus = stats_df['stlPerGame'] * 1.5

    # Penalties
    fouls_penalty = stats_df['foulsPerGame']
    turnovers_penalty = stats_df['tovPerGame'] * 2

    total_bonus = games_played_bonus + games_started_bonus + rebounds_bonus + points_bonus  + fg_bonus + ft_bonus + blocks_bonus + steals_bonus + three_bonus
    total_penalty = fouls_penalty + turnovers_penalty

    stock = total_bonus - total_penalty

    final_stock = plus_minus + stock

    stats_df['stock'] = final_stock
    stats_df['stock'] = stats_df['stock'].round(decimals=2)

    # Generating Proficiencies
    offense = points_bonus + fg_bonus + ft_bonus - turnovers_penalty
    defense = blocks_bonus + steals_bonus - fouls_penalty

    stats_df['offensiveProficiencies'] = offense.round(decimals=2)
    stats_df['defensiveProficiencies'] = defense.round(decimals=2)


    return stats_df


def teams_df() -> pd.DataFrame:
    """
    Returns a Dataframe of NBA Teams.
    """
    headers={
        "Authorization": "Basic " + base64.b64encode('{}:{}'.format(keys.MYSPORTSFEEDS, "MYSPORTSFEEDS").encode('utf-8')).decode('ascii')
    }
    rq = requests.request("GET", "https://api.mysportsfeeds.com/v2.1/pull/nba/2022-2023-regular/team_stats_totals.json", headers=headers)

    teams = pd.json_normalize(rq.json()['teamStatsTotals'])
    
    # The Jinja template does not parse dot notation in DataFrames, so some column names needs to be changed.
    teams = teams.rename(columns={
        'team.id': 'teamid',
        'team.city': 'city',
        'team.name': 'name',
        'team.abbreviation': 'key',
        'team.officialLogoImageSrc': 'logo',
        'stats.fieldGoals.fgPct': 'fgPct',
        'stats.freeThrows.ftPct': 'ftPct',
        'stats.rebounds.rebPerGame': 'rebPerGame',
        'stats.offense.astPerGame': 'astPerGame',
        'stats.offense.ptsPerGame': 'ptsPerGame',
        'stats.defense.stlPerGame': 'stlPerGame',
        'stats.defense.blkPerGame': 'blkPerGame',
        'stats.miscellaneous.foulsPerGame': 'foulsPerGame',
        'stats.defense.tovPerGame': 'tovPerGame',
        'stats.standings.wins': 'wins',
        'stats.standings.losses': 'losses'
        })

    teams = teams.set_index(['teamid'])

    return teams


def schedule_df() -> pd.DataFrame:
    """
    Returns a DataFrame the NBA schedule.
    """
    headers={
        "Authorization": "Basic " + base64.b64encode('{}:{}'.format(keys.MYSPORTSFEEDS, "MYSPORTSFEEDS").encode('utf-8')).decode('ascii')
    }
    rq = requests.request("GET", "https://api.mysportsfeeds.com/v2.1/pull/nba/2022-2023-regular/games.json", headers=headers)

    schedule = pd.json_normalize(rq.json()['games'])

    # The Jinja template does not parse dot notation in DataFrames, so some column names needs to be changed.
    schedule = schedule.rename(columns={
        'schedule.startTime': 'startTime',
        'schedule.awayTeam.abbreviation': 'awayTeam',
        'schedule.homeTeam.abbreviation': 'homeTeam'
    })

    #Change startTime column to DateTime data type
    schedule['startTime'] = pd.to_datetime(schedule['startTime'])

    return schedule