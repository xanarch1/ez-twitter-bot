from requests_oauthlib import OAuth1Session
import json
import os
from dotenv import dotenv_values

config = dotenv_values(".env")  # config = {"USER": "foo", "EMAIL": "foo@example.org"}

consumer_key = config["API_KEY"]
consumer_secret = config["API_SECRET_KEY"]


payload = {"text": "Test"}

request_token_url = "https://api.twitter.com/oauth/request_token"
oauth = OAuth1Session(consumer_key, client_secret=consumer_secret)

try:
    fetch_response = oauth.fetch_request_token(request_token_url)
except ValueError:
    print("There may have been an issue with the keys you entered")

resource_owner_key = fetch_response.get("oauth_token")
resource_owner_secret = fetch_response.get("oauth_token_secret")

print("Got OAuth token: %s" % resource_owner_key)

#getting authorization

base_authorization_url = "https://api.twitter.com/oauth/authorize"
authorization_url = oauth.authorization_url(base_authorization_url)
print("Please go here and authorize: %s" % authorization_url)
verifier = input("Paste the PIN here: ")

#Get the access token
access_token_url = "https://api.twitter.com/oauth/access_token"
oauth = OAuth1Session(
        consumer_key,
        client_secret=consumer_secret,
        resource_owner_key=resource_owner_key,
        resource_owner_secret=resource_owner_secret,
        verifier=verifier
        )
oauth_tokens = oauth.fetch_access_token(access_token_url)

access_token = oauth_tokens["oauth_token"]
access_token_secret = oauth_tokens["oauth_token_secret"]

#Making the request

response = oauth.post(
        "https://api.twitter.com/2/tweets",
        json=payload
        )

if response.status_code != 201:
    raise Exception(
            "Request returned error; {} {}".format(response.status_code, response.text)
            )

print("Response code: {}".format(response.status_code))


#saving response

json_response = response.json()

print(json.dumps(json_response, indent=4, sort_keys=True))


