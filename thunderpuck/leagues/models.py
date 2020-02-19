import hashlib
import ujson

from django.db import models
from django.contrib.postgres.fields import JSONField

from thunderpuck.download_utilities import get_json_with_retries

# Create your models here.
class League(models.Model):
    name = models.CharField(unique=True, max_length=16)
    base_api_url = models.URLField(null=True)
    teams_json_url = models.URLField(null=True)
    teams_json = JSONField(null=True)
    teams_json_md5 = models.CharField(max_length=32, null=True)
    franchise_json_url = models.URLField(null=True)
    franchise_json = JSONField(null=True)
    franchise_json_md5 = models.CharField(max_length=32, null=True)

    def download_and_update_teams_json(self):
        url = f'{self.base_api_url}{self.teams_json_url}'
        teams_json = get_json_with_retries(url)
        self.update_or_create_teams_json(teams_json)

    def update_or_create_teams_json(self, new_json):
        old_md5 = self.teams_json_md5
        new_json_string = ujson.dumps(new_json).encode("utf-8")
        new_md5 = hashlib.md5(new_json_string).hexdigest()
        if new_md5 != old_md5:
            self.teams_json_md5 = new_md5
            self.teams_json = new_json
            self.save(update_fields=['teams_json_md5', 'teams_json'])
            return True
        return False

    def download_and_update_franchise_json(self):
        url = f'{self.base_api_url}{self.franchise_json_url}'
        franchise_json = get_json_with_retries(url)
        self.update_or_create_franchise_json(franchise_json)

    def update_or_create_franchise_json(self, new_json):
        old_md5 = self.franchise_json_md5
        new_json_string = ujson.dumps(new_json).encode("utf-8")
        new_md5 = hashlib.md5(new_json_string).hexdigest()
        if new_md5 != old_md5:
            self.franchise_json_md5 = new_md5
            self.franchise_json = new_json
            self.save(update_fields=['franchise_json_md5', 'franchise_json'])
            return True
        return False

    def __str__(self):
        return f'{self.name}'

class Conference(models.Model):
    nhl_id = models.IntegerField(unique=True)
    name = models.CharField(max_length=64)
    league= models.ForeignKey('League', on_delete=models.CASCADE)

class Division(models.Model):
    nhl_id = models.IntegerField(unique=True)
    name = models.CharField(max_length=64)
    name_short = models.CharField(max_length=16)
    abbreviation = models.CharField(max_length=8)
    conference = models.ForeignKey('Conference', on_delete=models.CASCADE, to_field='nhl_id')
    league = models.ForeignKey('League', on_delete=models.CASCADE)