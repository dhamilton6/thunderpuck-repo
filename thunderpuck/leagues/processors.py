from cities.models import City

from thunderpuck.teams.models import Team, Venue, Franchise
from thunderpuck.leagues.models import League, Conference, Division

def get_city(city):
    return City.objects.get(name=city)

def get_venue(venue):
    v, _ = Venue.objects.update_or_create(
        nhl_id=venue['id'],
        details={
            'name': venue['name'],
            'city': get_city(venue['city']),
        }
    )
    return v

def get_division(division, conference, league):
    d, created = Division.objects.update_or_create(
        nhl_id=division['id'],
        details={
            'name': division['name'],
            'name_short': division['nameShort'],
            'abbreviation': division['abbreviation'],
            'league': league,
            'conference': conference,
        }
    )
    return d

def get_conference(conference, league):
    c, created = Conference.objects.update_or_create(
        nhl_id=conference['id'],
        details={
            'name': conference['name'],
            'league': league,
        }
    )
    return c

def get_franchise(franchise):
    f, created = Franchise.objects.update_or_create(
        nhl_id=franchise['franchiseId'],
        details={
            'team_name': franchise['teamName'],
        }
    )
    return f

def process_teams_json(league_name):
    try:
        league = League.objects.get(name=league_name) \
                        .only('teams_json')
        teams_json = league.teams_json
    except League.objects.DoesNotExist:
        print(f"Could not find the league {league_name}")
        return
    for team in teams_json.get('teams', []):
        t, _ = Team.objects.get_or_create(nhl_id=team['id'])
        t.name = team['name']
        t.venue = get_venue(team['venue'])
        t.abbreviation = team['abbreviation']
        t.location_name = team['locationName']
        t.team_name = team['teamName']
        t.first_year_of_play = team['firstYearOfPlay']
        t.league = league
        t.conference = get_conference(team['conference'], league)
        t.division = get_division(team['division'], t.conference, league)
        t.franchise = get_franchise(team['franchise'])
        t.short_name = team['shortName']
        t.official_site_url = team['officialSiteUrl']
        t.active = team['active']
        t.save()
        