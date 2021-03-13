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
            raise NotImplementedError("To be implemented")
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
    
    def league_request(self, league_key=None, subresource=None):
        assert league_key is not None, "[Requester] Must provide a league key"

        valid_subresources = [
            "metadata", "settings", "standings", "scoreboard", "teams", "players", "draftresults", "transactions"
        ]
        assert subresource in valid_subresources, \
            "[Requester] Requested league subresource \"{}\" is invalid".format(subresource)

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
        assert game_code in ["nhl", "nba", "mlb", "nfl"], \
            "[Requester] Unsupported game code \"{}\"".format(game_code)
        url = self.base_url + "game/{}".format(game_code)
        return self.api.get(url)["fantasy_content"]["game"][0]


