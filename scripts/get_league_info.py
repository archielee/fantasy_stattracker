import argparse
import json
import os

from fantasy_stattracker.web.api_access import YahooAPI
from fantasy_stattracker.web.requester import Requester
from fantasy_stattracker.utils.parsing import *


league_type_to_game_map = {
    "hockey": "nhl",
    "basketball": "nba",
    "football": "nfl",
    "baseball": "mlb"
}


def main(args):
    league_info_path = os.path.abspath(args.league_info)
    if not os.path.isfile(league_info_path):
        raise FileNotFoundError("[get_league_info] Provided league information file \"{}\" does not exist".format(args.league_info))

    with open(league_info_path, "r") as f:
        league_info = json.load(f)

    api = YahooAPI()
    requester = Requester(api)

    if league_info.get("league_key") is None:
        # Get map from game type to game ID (this changes from year to year)
        # For example, fantasy hockey for the 2020 season has game ID 403
        if league_info.get("game_id") is None:
            league_type = league_info["league_type"]
            if league_type not in league_type_to_game_map.keys():
                raise ValueError("[get_league_info] Unsupported league type \"{}\"".format(league_type))
            game_code = league_type_to_game_map[league_info["league_type"]]
            game_data = requester.request("game", game_code=game_code)
            game_id = game_data["game_id"]
            league_info["game_id"] = game_id

        league_info["league_key"] = "{}.l.{}".format(game_id, league_info["league_id"])
        league_id = league_info["league_id"]

    league_data = requester.request("league", league_key=league_info["league_key"], subresource="metadata")
    league_info["n_weeks"] = int(league_data["end_week"]) - int(league_data["start_week"]) + 1
    league_info["scoring_type"] = league_data["scoring_type"]

    team_data = requester.request("league", league_key=league_info["league_key"], subresource="teams")
    team_id_map = get_team_id_map(team_data)
    league_info["team_ids"] = team_id_map

    league_settings = requester.request("league", league_key=league_info["league_key"], subresource="settings")
    league_info["roster"], league_info["stat_categories"] = parse_league_settings(league_settings)

    with open(league_info_path, "w") as f:
        f.write(json.dumps(league_info, indent=4))


if __name__ == "__main__":
    parser = argparse.ArgumentParser("Fetch league settings using Yahoo API")
    parser.add_argument("--league_info", "-l", type=str,
                        default="./json_files/league_info.json",
                        help="file containing league information details")
    args = parser.parse_args()
    main(args)
