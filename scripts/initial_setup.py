import argparse
import pprint
from fantasy_stattracker.web.api_access import YahooAPI

def main(args):
    api = YahooAPI(auth_key_file=args.key_file)
    api.login()
    test_url = "https://fantasysports.yahooapis.com/fantasy/v2/"
    r = api.get(test_url)
    print("[YahooAPI] Response from Yahoo API")
    pprint.pprint(r)

if __name__ == "__main__":
    parser = argparse.ArgumentParser("Yahoo API Key Set-up")
    parser.add_argument("--key_file", "-f", type=str,
                        default="auth_key.json",
                        help="Full path to API key file")
    args = parser.parse_args()
    main(args)
