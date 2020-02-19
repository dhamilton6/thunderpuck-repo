from django.db import models
from cities.models import City

from thunderpuck.leagues.models import League, Conference, Division


"""{
"id": 1,
"name": "New Jersey Devils",
"link": "/api/v1/teams/1",
"venue": {
"name": "Prudential Center",
"link": "/api/v1/venues/null",
"city": "Newark",
"timeZone": {
"id": "America/New_York",
"offset": -5,
"tz": "EST"
}
},
"abbreviation": "NJD",
"teamName": "Devils",
"locationName": "New Jersey",
"firstYearOfPlay": "1982",
"division": {
"id": 18,
"name": "Metropolitan",
"nameShort": "Metro",
"link": "/api/v1/divisions/18",
"abbreviation": "M"
},
"conference": {
"id": 6,
"name": "Eastern",
"link": "/api/v1/conferences/6"
},
"franchise": {
"franchiseId": 23,
"teamName": "Devils",
"link": "/api/v1/franchises/23"
},
"shortName": "New Jersey",
"officialSiteUrl": "http://www.newjerseydevils.com/",
"franchiseId": 23,
"active": true
},"""
class Team(models.Model):
    league = models.ForeignKey(League, on_delete=models.CASCADE)
    conference = models.ForeignKey(Conference, on_delete=models.CASCADE, to_field='nhl_id')
    division = models.ForeignKey(Division, on_delete=models.CASCADE, to_field='nhl_id')
    nhl_id = models.IntegerField(default=0)
    name = models.CharField(max_length=64)
    venue = models.ForeignKey('Venue', on_delete=models.CASCADE, to_field='nhl_id')
    all_venues = models.ManyToManyField('Venue', related_name='venues')
    abbreviation = models.CharField(max_length=3)
    first_year_of_play = models.IntegerField()
    team_name = models.CharField(max_length=64)
    location_name = models.CharField(max_length=64)
    short_name = models.CharField(max_length=64)
    official_site_url = models.CharField(max_length=64)
    franchise = models.ForeignKey('Franchise', models.CASCADE, to_field='nhl_id')
    active = models.BooleanField(default=True)

    def __str__(self):
        return f'{self.name}'

class Venue(models.Model):
    nhl_id = models.IntegerField(unique=True)
    name = models.CharField(max_length=64)
    link = models.URLField()
    city = models.ForeignKey(City, on_delete=models.CASCADE)

    def __str__(self):
        return f'{self.name}'

class Franchise(models.Model):
    nhl_id = models.IntegerField(unique=True)
    first_season_id = models.IntegerField()
    team_name = models.CharField(max_length=64)
    location_name = models.CharField(max_length=64)

    def __str__(self):
        return f'Franchise: {self.location_name} {self.team_name}'
