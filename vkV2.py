import requests
from requests_oauthlib import OAuth2Session
from oauthlib.oauth2 import BackendApplicationClient

api_version = '5.74'
token = '21f1207c6adff155016bd91083ea9c07d36a8ed995c961eda6a988517cf3fb487133dc9de19425fd89e33'
token_url = 'https://api.everypixel.com/oauth/token'
query_prefix = 'https://api.vk.com/method/'
client_id = '2PJB6JOphWlfS3JmPG30UbSv0lwr0dBG8mlxEJsv'
client_secret = 'Y6BHGwwTWLLIuGKf1GeEGohn4k6iNjadQ1rz6AQYtFp8T2zumk'
everypixel_url = 'https://api.everypixel.com/v1/keywords'
oauth = OAuth2Session(client=BackendApplicationClient(client_id))
token_to_everyPixel = oauth.fetch_token(token_url=token_url,
                                        auth=(client_id, client_secret))
api = OAuth2Session(client_id, token=token_to_everyPixel)

print("Введите id пользователя")
user_id = input()
params = dict(access_token=token, v=api_version, fields='photo_max_orig', user_id=user_id)
response = requests.get(query_prefix + 'users.get', params=params).json()
photo_url = response['response'][0]['photo_max_orig']
params = {'url': photo_url}
keywords = api.get(everypixel_url, params=params).json()['keywords']
answer = sorted(keywords, key=lambda x: x['score'])[-5:]
for keyword in reversed(answer):
    print(keyword['keyword'])
