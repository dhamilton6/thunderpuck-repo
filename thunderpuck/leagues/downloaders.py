from .models import League

def download_and_update_nhl_teams_json():
    l = League.objects.get(name='NHL')
    l.download_and_update_franchise_json()
    l.download_and_update_teams_json()