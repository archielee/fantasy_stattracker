


class Requester:
    def __init__(self, oauth):
        self.oauth = oauth
        self.base_url = "https://fantasysports.yahooapis.com/fantasy/v2/"

    def get(self, resource, game_type, league_id, sub_resource):
        self.oauth.login()
        
        if resource == "league":
            pass
        elif resource == "game":
            pass
        elif resource == "team":
            pass
        elif resource == "roster":
            pass
        elif resource == "player":
            pass
        elif resource == "transaction":
            pass
        elif resource == "user":
            pass


        url = self.base_url + '{}/{}.l.{}/{}'.format(resource, game_type, league_id, sub_resource)
        url = self.base_url + '{}/{}'.format(resource, game_type)
        response = self.oauth.session.get(url, params={'format': 'json'})
        r = response.json()
        with open('YahooGameInfo.json', 'w') as outfile:
            json.dump(r, outfile)