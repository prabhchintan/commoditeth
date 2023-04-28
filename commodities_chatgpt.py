import requests

commodity = 'LUMBER'
base_currency = 'ETH'
endpoint = 'latest'
access_key = '8atmpalynnqn13q5jkllbmn675na618mtu3ia20q7lal6e6je85bq0o361ok'

resp = requests.get(
    'https://commodities-api.com/api/' + endpoint + '?access_key=' + access_key + '&base=' + commodity + '&symbols=' + base_currency
)
if resp.status_code != 200:
    # This means something went wrong.
    raise ApiError('GET /' + endpoint + '/ {}'.format(resp.status_code))
print(resp.json())
