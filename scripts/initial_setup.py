import pprint
from fantasy_stattracker.web.api_access import YahooAPI


def main():
    api = YahooAPI(auth_key_file='./json_files/auth_key.json')
    api.login()
    test_url = "https://fantasysports.yahooapis.com/fantasy/v2/"
    r = api.get(test_url)
    print("[YahooAPI] Response from Yahoo API")
    pprint.pprint(r)


if __name__ == "__main__":
    main()
