from request_types.types import *


def get_match_info_by_team_for_tier(matches: DivisionUnion):
    """
    Creates a dictionary that allows individual matches to be surfaced using a team and opponent name. The match data contains map
    the match was played on, as well as an object representing the round scores of the given team and their opponent.
    """
    league_matches = {}

    for match in matches:
        map = match.playerStats[0].match.mapName
        rounds = match.playerStats[0].match.rounds

        if match.home.name not in league_matches:
            league_matches[match.home.name] = {}
        if match.away.name not in league_matches:
            league_matches[match.away.name] = {}

        home_rounds_won = away_rounds_won = 0
        home_t_rounds_won = home_ct_rounds_won = 0
        away_t_rounds_won = away_ct_rounds_won = 0

        for round in rounds:
            if round.winnerClanName == match.home.name:
                home_rounds_won += 1
                home_t_rounds_won += round.winnerENUM == 2
                home_ct_rounds_won += round.winnerENUM == 3
            elif round.winnerClanName == match.away.name:
                away_rounds_won += 1
                away_t_rounds_won += round.winnerENUM == 2
                away_ct_rounds_won += round.winnerENUM == 3

        league_matches[match.home.name][match.away.name] = {
            "map": map,
            "score": {
                "my": {
                    "t_rounds_won": home_t_rounds_won,
                    "ct_rounds_won": home_ct_rounds_won,
                    "total_rounds_won": home_rounds_won,
                },
                "opponent": {
                    "t_rounds_won": away_t_rounds_won,
                    "ct_rounds_won": away_ct_rounds_won,
                    "total_rounds_won": away_rounds_won,
                },
            },
        }
        league_matches[match.away.name][match.home.name] = {
            "map": map,
            "score": {
                "my": {
                    "t_rounds_won": away_t_rounds_won,
                    "ct_rounds_won": away_ct_rounds_won,
                    "total_rounds_won": away_rounds_won,
                },
                "opponent": {
                    "t_rounds_won": home_t_rounds_won,
                    "ct_rounds_won": home_ct_rounds_won,
                    "total_rounds_won": home_rounds_won,
                },
            },
        }

    return LeagueMatches(matches=league_matches)


def get_round_win_percentage_by_team(
    league_matches: LeagueMatches,
) -> TeamRoundWinPercentages:
    """
    Creates a dictionary that allows individual teams to surface their round win percentage against their opponents.
    """
    round_win_percentage = {}

    for team in league_matches.matches:
        rounds_won = 0
        rounds_played = 0
        t_rounds_won = 0
        ct_rounds_won = 0
        t_rounds_played = 0
        ct_rounds_played = 0

        for opponent in league_matches.matches[team]:
            my_score = league_matches.matches[team][opponent].score.my.total_rounds_won
            opponent_score = league_matches.matches[team][
                opponent
            ].score.opponent.total_rounds_won
            rounds_won += my_score
            rounds_played += my_score + opponent_score
            t_rounds_won += league_matches.matches[team][opponent].score.my.t_rounds_won
            ct_rounds_won += league_matches.matches[team][
                opponent
            ].score.my.ct_rounds_won
            t_rounds_played += (
                league_matches.matches[team][opponent].score.my.t_rounds_won
                + league_matches.matches[team][opponent].score.opponent.ct_rounds_won
            )
            ct_rounds_played += (
                league_matches.matches[team][opponent].score.my.ct_rounds_won
                + league_matches.matches[team][opponent].score.opponent.t_rounds_won
            )

        round_win_percentage[team] = TeamRoundWinPercentage(
            rounds_won=rounds_won,
            rounds_played=rounds_played,
            t_rounds_won=t_rounds_won,
            t_rounds_played=t_rounds_played,
            ct_rounds_won=ct_rounds_won,
            ct_rounds_played=ct_rounds_played,
            percentage=rounds_won / rounds_played,
            t_percentage=t_rounds_won / t_rounds_played,
            ct_percentage=ct_rounds_won / ct_rounds_played,
        )

    return round_win_percentage


def get_strength_of_schedule_by_team(
    league_matches: LeagueMatches, round_win_percentage: TeamRoundWinPercentages
) -> Dict[str, TeamStrengthOfSchedule]:
    strength_of_schedule = {}

    for team in league_matches.matches:
        total_opponent_rounds_won = 0
        total_opponent_rounds_played = 0
        for opponent in league_matches.matches[team]:
            won_bias = league_matches.matches[team][
                opponent
            ].score.opponent.total_rounds_won
            played_bias = (
                league_matches.matches[team][opponent].score.opponent.total_rounds_won
                + league_matches.matches[team][opponent].score.my.total_rounds_won
            )
            opponent_rounds_won = round_win_percentage[opponent].rounds_won - won_bias
            opponent_rounds_played = (
                round_win_percentage[opponent].rounds_played - played_bias
            )
            total_opponent_rounds_won += opponent_rounds_won
            total_opponent_rounds_played += opponent_rounds_played

        strength_of_schedule[team] = TeamStrengthOfSchedule(
            opponent_rounds_won=total_opponent_rounds_won,
            opponent_rounds_played=total_opponent_rounds_played,
            percentage=round((total_opponent_rounds_won / total_opponent_rounds_played) * 100, 2),
        )

    return strength_of_schedule


def get_average_ratings_by_team(matches: DivisionUnion) -> Dict[str, TeamAverageRating]:
    """
    Creates a dictionary that allows individual teams to surface their average rating.
    """
    team_ratings = {}

    def is_signed(player: Player):
        return (
            player.type == "SIGNED"
            or player.type == "SIGNED_SUBBED"
            or player.type == "SIGNED_PROMOTED"
        )

    for match in matches:
        home_team = match.home.name
        home_signed_players = [
            player.name for player in match.home.players if is_signed(player)
        ]
        away_team = match.away.name
        away_signed_players = [
            player.name for player in match.away.players if is_signed(player)
        ]
        if home_team not in team_ratings:
            team_ratings[home_team] = {
                "rating": [],
                "ct_rating": [],
                "t_rating": [],
            }
        if away_team not in team_ratings:
            team_ratings[away_team] = {
                "rating": [],
                "ct_rating": [],
                "t_rating": [],
            }

        for player in match.playerStats:
            if player.teamClanName == home_team and player.name in home_signed_players:
                team_ratings[home_team]["rating"].append(player.rating)
                team_ratings[home_team]["ct_rating"].append(player.ctRating)
                team_ratings[home_team]["t_rating"].append(player.TRating)
            elif (
                player.teamClanName == away_team and player.name in away_signed_players
            ):
                team_ratings[away_team]["rating"].append(player.rating)
                team_ratings[away_team]["ct_rating"].append(player.ctRating)
                team_ratings[away_team]["t_rating"].append(player.TRating)

    for team in team_ratings:
        team_ratings[team] = TeamAverageRating(
            rating=sum(team_ratings[team]["rating"])
            / len(team_ratings[team]["rating"]),
            ct_rating=sum(team_ratings[team]["ct_rating"])
            / len(team_ratings[team]["ct_rating"]),
            t_rating=sum(team_ratings[team]["t_rating"])
            / len(team_ratings[team]["t_rating"]),
        )

    return team_ratings
