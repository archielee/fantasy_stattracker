class Requester:
    def __init__(self, api):
        self.api = api
        self.base_url = "https://fantasysports.yahooapis.com/fantasy/v2/"



    def request(self, resource, **kwargs):
        self.api.login()
        
        if resource == "league":
            return self.league_request(**kwargs)
        elif resource == "game":
            return self.game_request(**kwargs)
        elif resource == "team":
            return self.team_request(**kwargs)
        elif resource == "roster":
            raise NotImplementedError("To be implemented")
        elif resource == "player":
            raise NotImplementedError("To be implemented")
        elif resource == "transaction":
            raise NotImplementedError("To be implemented")
        elif resource == "user":
            raise NotImplementedError("To be implemented")
        else:
            raise ValueError("[Requester] Unknown API resource \"{}\"".format(resource))
    
    # TODO: handle subresource parsing in resource-specific classes

    def league_request(self, league_key=None, subresource=None):
        if league_key is None:
            raise ValueError("[Requester] Must provide a league key for league request")

        valid_subresources = [
            "metadata", "settings", "standings", "scoreboard", "teams", "players", "draftresults", "transactions"
        ]
        if subresource not in valid_subresources:
            raise ValueError("[Requester] Requested league subresource \"{}\" is invalid".format(subresource))

        url = self.base_url + "league/{}/{}".format(league_key, subresource)
        resp = self.api.get(url)["fantasy_content"]["league"]

        # Metadata is always first element in response list
        if subresource == "metadata":
            return resp[0]
        elif subresource == "settings":
            return resp[1][subresource][0]
        else:
            return resp[1][subresource]

    def game_request(self, game_code=None):
        if game_code not in ["nhl", "nba", "mlb", "nfl"]:
            raise ValueError("[Requester] Unsupported game code \"{}\"".format(game_code))

        url = self.base_url + "game/{}".format(game_code)
        return self.api.get(url)["fantasy_content"]["game"][0]

    def team_request(self, team_key=None, subresource=None, week=None):
        if team_key is None:
            raise ValueError("[Requester] Must provide a team key for team request")

        # Matchups is only valid if the league is head-to-head
        # TODO: add head-to-head check here
        valid_subresources = [
            "metadata", "stats", "standings", "roster", "draftresults", "matchups"
        ]
        if subresource not in valid_subresources:
            raise ValueError("[Requester] Requested team subresource \"{}\" is invalid".format(subresource))

        url = self.base_url + "team/{}/{}".format(team_key, subresource)
        # Add filter for week number if provided (for matchups and stats only)
        if subresource in ["stats", "matchups"] and week is not None:
            if subresource == "stats":
                # For stats, week must be a single value
                if type(week) is not int:
                    raise TypeError("[Requester] Must pass in a single week value as an integer")
                url += ";type=week;week={}".format(week)
            else:
                # For matchups, can string together multiple values using commas
                if type(week) is int:
                    week = [week]
                elif type(week) is not list:
                    raise TypeError("[Requester] Week values must be passed in as a list")
                week = [str(el) for el in week]
                weeks = ",".join(week)
                url += ";weeks={}".format(weeks)
        resp = self.api.get(url)["fantasy_content"]["team"]

        # Metadata is always first element in response list
        if subresource == "metadata":
            return resp[0]
        elif subresource == "stats":
            return resp[1]["team_stats"]["stats"]
        else:
            return resp[1][subresource]