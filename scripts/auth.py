import json
import os
import pprint

from yahoo_oauth import OAuth2


class YahooAPIAuth:
    def __init__(self, auth_key_file='../auth_key.json'):
        assert os.path.isfile(os.path.abspath(auth_key_file)), \
            "[YahooAPIAuth] Provided file path \"{}\" does not exist".format(auth_key_file)

        # Yahoo uses OAuth2
        self.oauth = OAuth2(None, None, from_file=os.path.abspath(auth_key_file))

    def login(self):
        if not self.oauth.token_is_valid():
            self.oauth.refresh_access_token()
            print("[YahooAPIAuth] Successfully logged in!")


if __name__ == "__main__":
    oauth = YahooAPIAuth()
    oauth.get()
