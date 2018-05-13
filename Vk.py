import requests
from requests_oauthlib import OAuth2Session
from oauthlib.oauth2 import BackendApplicationClient
from random import shuffle

api_version = "5.74"
token = "21f1207c6adff155016bd91083ea9c07d36a8ed995c961eda6a988517cf3fb487133dc9de19425fd89e33"
token_url = 'https://api.everypixel.com/oauth/token'
query_prefix = "https://api.vk.com/method/"
client_id = '2PJB6JOphWlfS3JmPG30UbSv0lwr0dBG8mlxEJsv'
client_secret = 'Y6BHGwwTWLLIuGKf1GeEGohn4k6iNjadQ1rz6AQYtFp8T2zumk'
everypixel_url = 'https://api.everypixel.com/v1/quality'
oauth = OAuth2Session(client=BackendApplicationClient(client_id))
token_to_everyPixel = oauth.fetch_token(token_url=token_url,
                                        auth=(client_id, client_secret))
api = OAuth2Session(client_id, token=token_to_everyPixel)

print("Введите id пользователя")
user_id = input()
params = dict(access_token=token, v=api_version, fields='photo_max_orig', user_id=user_id)
response = requests.get(query_prefix + "friends.get", params=params).json()
friends = response['response']['items']
results = {}
shuffle(friends)
for friend in friends:
    photo_url = friend['photo_max_orig']
    first_name = friend['first_name']
    last_name = friend['last_name']
    params = {'url': photo_url}
    quality = api.get(everypixel_url, params=params).json()
    if 'error' in quality.keys():
        break
    results[first_name + " " + last_name] = float(quality['quality']['score'])
answer = sorted(results.keys(), key=lambda x: results[x])
counter = 1
for name in reversed(answer):
    print(str(counter) + '.' + name + ' : ' + str(results[name] * 100) + '% качества')
    counter += 1
