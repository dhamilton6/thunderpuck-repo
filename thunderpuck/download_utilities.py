import requests
import ujson

HEADERS = {'User-Agent' : 'Mozilla/5.0 (Macintosh; U; Intel Mac OS X 10.5; en-US; rv:1.9.1.4) Gecko/20091016 Firefox/3.5.4'}

def get_json_with_retries(url, params={}):
    requests.models.json = ujson
    try:
        r = get_with_retries(url, headers=HEADERS, params=params)
    except:
        raise
    return r.json()

def get_with_retries(*args, **kwargs):
    """
    Wrapper around `requests.get`, takes the same arguments,
    but raises exception in case of wrong status code.
    """
    max_retries = kwargs.pop('_max_retries', 1)
    if max_retries < 0:
        raise ValueError
    retries = 0
    while True:
        try:
            response = requests.get(*args, **kwargs)
            response.raise_for_status()
            return response
        except Exception:
            if retries >= max_retries:
                raise
            retries += 1