import argparse
import json
import os
import pandas as pd
import pprint

from fantasy_stattracker.web.api_access import YahooAPI
from fantasy_stattracker.web.requester import Requester
from fantasy_stattracker.utils.parsing import *

### NOTE: This file must be run after running get_league_info.py. If you run
###       this before, it will error out.

def main(args):
    league_info_path = os.path.abspath(args.league_info)
    if not os.path.isfile(league_info_path):
        raise FileNotFoundError("[get_teams_data] Provided league information file \"{}\" does not exist".format(args.league_info))

    with open(league_info_path, "r") as f:
        league_info = json.load(f)

    api = YahooAPI()
    requester = Requester(api)

    # Get necessary parameters
    league_key = league_info["league_key"]
    team_ids = league_info["team_ids"]
    n_teams = len(league_info["team_ids"].keys())

    league_data = requester.request("league", league_key=league_key, subresource="metadata")
    n_weeks = int(league_data["end_week"]) - int(league_data["start_week"]) + 1
    cur_week = int(league_data["current_week"])

    # Process each team
    team_keys = [league_key + ".t.{}".format(i + 1) for i in range(n_teams)]
    team_data = requester.request("team", team_key=team_keys[0], subresource="stats", week=1)
    pprint.pprint(team_data)


if __name__ == "__main__":
    parser = argparse.ArgumentParser("Fetch team data for all teams in a fantasy league using Yahoo API")
    parser.add_argument("--league_info", "-l", type=str,
                        default="./league_info.json",
                        help="file containing league information details")
    parser.add_argument("--prev_data", "-p", type=str,
                        default="./league_stats.pd",
                        help="binary file containing league statistics from previous weeks (if available, will only add data from recent week(s), else this file will be generated using all available data)")
    args = parser.parse_args()
    main(args)