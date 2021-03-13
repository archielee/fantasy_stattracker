import json
import os
import pprint
import requests

from yahoo_oauth import OAuth2


class YahooAPIAuth:
    def __init__(self, auth_key_file='auth_key.json'):
        if not os.path.isfile(os.path.abspath(auth_key_file)):
            raise FileNotFoundError("[YahooAPIAuth] Required file \"{}\" does not exist - please provide your API keys".format(auth_key_file))

        # Yahoo uses OAuth2
        self.oauth = OAuth2(None, None, from_file=os.path.abspath(auth_key_file))
        if self.oauth.token_is_valid():
            print("[YahooAPIAuth] Initialized Yahoo API connection")

    def login(self):
        if not self.oauth.token_is_valid():
            self.oauth.refresh_access_token()
            print("[YahooAPIAuth] Successfully logged in!")

    def get(self, url):
        try:
            r = self.oauth.session.get(url, params={'format': 'json'})
            return r.json()
        except requests.exceptions.MissingSchema as e:
            msg = "[YahooAPIAuth] Failed to get a response from URL \"{}\" - your URL is probably malformed".format(url)
            raise ValueError(msg)
        except requests.exceptions.ConnectionError as e:
            msg = "[YahooAPIAuth] Failed to get a response from URL \"{}\" - are you sure this is a valid URL?".format(url)
            raise requests.exceptions.ConnectionError(msg)
        except ValueError as e:
            msg = "[YahooAPIAuth] Failed to get valid JSON message from Yahoo API response"
            raise ValueError(msg)


if __name__ == "__main__":
    oauth = YahooAPIAuth()
    oauth.login()
    test_url = "https://fantasysports.yahooapis.com/fantasy/v2/"
    r = oauth.get(test_url)
    print("[YahooAPIAuth] Response from Yahoo API")
    pprint.pprint(r)
