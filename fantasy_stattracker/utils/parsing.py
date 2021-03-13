# TODO: This should all probably go in individual resource classes

def get_team_id_map(teams_data):
    '''
    Maps the numerical team IDs to a team name

    Arguments:
        teams_data (dict): dict returned from API request for data on all teams
                           in the fantasy league

    Returns:
        Dictionary where every team ID (int) is mapped to the corresponding
        team name (str)
    '''
    team_id_map = {}
    n_teams = int(teams_data["count"])
    for i in range(n_teams):
        team_data = teams_data[str(i)]["team"][0]
        team_id = team_data[1]["team_id"]
        team_name = team_data[2]["name"]
        team_id_map[team_id] = team_name
    return team_id_map

def parse_league_settings(league_settings):
    '''
    Extract relevant information from league settings API response

    Arguments:
        league_settings (dict): dict returned from API request for settings

    Returns:
        roster (list): list of roster positions
        stat_categories (dict): dict mapping stat categories tracked in league
                                to the corresponding stat ID used in the API
    '''
    roster_positions = league_settings["roster_positions"]
    positions = []
    for position in roster_positions:
        position_type = position["roster_position"]["position"]
        n_position = int(position["roster_position"]["count"])
        for i in range(n_position):
            positions.append(position_type)

    stat_types = league_settings["stat_categories"]["stats"]
    stat_categories = {}
    n_stats = len(stat_categories)
    for stat_type in stat_types:
        stat = stat_type["stat"]
        stat_id = stat["stat_id"]
        stat_name = stat["display_name"]
        stat_categories[stat_name] = stat_id
    return positions, stat_categories
