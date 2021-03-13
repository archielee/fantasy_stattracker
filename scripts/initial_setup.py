import pprint
from fantasy_stattracker.web.auth import YahooAPIAuth

if __name__ == "__main__":
    oauth = YahooAPIAuth()
    oauth.login()
    test_url = "https://fantasysports.yahooapis.com/fantasy/v2/"
    r = oauth.get(test_url)
    print("[YahooAPIAuth] Response from Yahoo API")
    pprint.pprint(r)