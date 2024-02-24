from statistics import mean

from request_types.types import *


def get_rwoa_by_team(league_matches: LeagueMatches, team_round_win_percentage: TeamRoundWinPercentages):
    team_rwoa = {}

    for team_name, matches in league_matches.matches.items():
        rwoa_values = {'total': [], 't': [], 'ct': []}

        for opponent_name, match_detail in matches.items():
            biases = {
                'won': match_detail.score.opponent.total_rounds_won,
                'played': match_detail.score.opponent.total_rounds_won + match_detail.score.my.total_rounds_won,
                't_won': match_detail.score.opponent.t_rounds_won,
                't_played': match_detail.score.opponent.t_rounds_won + match_detail.score.my.ct_rounds_won,
                'ct_won': match_detail.score.opponent.ct_rounds_won,
                'ct_played': match_detail.score.opponent.ct_rounds_won + match_detail.score.my.t_rounds_won,
            }

            opponent_stats = team_round_win_percentage[opponent_name]
            opponent_biases_removed = {
                'rounds_won': opponent_stats.rounds_won - biases['won'],
                'rounds_played': opponent_stats.rounds_played - biases['played'],
                't_rounds_won': opponent_stats.t_rounds_won - biases['t_won'],
                't_rounds_played': opponent_stats.t_rounds_played - biases['t_played'],
                'ct_rounds_won': opponent_stats.ct_rounds_won - biases['ct_won'],
                'ct_rounds_played': opponent_stats.ct_rounds_played - biases['ct_played'],
            }

            rwp = {
                'total': biases['won'] / biases['played'] if biases['played'] else 0,
                't': biases['t_won'] / biases['t_played'] if biases['t_played'] else 0,
                'ct': biases['ct_won'] / biases['ct_played'] if biases['ct_played'] else 0,
            }

            opponent_rwp = {
                'total': opponent_biases_removed['rounds_won'] / opponent_biases_removed['rounds_played'] if opponent_biases_removed['rounds_played'] else 0,
                't': opponent_biases_removed['t_rounds_won'] / opponent_biases_removed['t_rounds_played'] if opponent_biases_removed['t_rounds_played'] else 0,
                'ct': opponent_biases_removed['ct_rounds_won'] / opponent_biases_removed['ct_rounds_played'] if opponent_biases_removed['ct_rounds_played'] else 0,
            }

            for key in ['total', 't', 'ct']:
                rwoa_value = (1 - rwp[key]) / (1 - opponent_rwp[key]) if opponent_rwp[key] != 1 else 0
                rwoa_values[key].append(rwoa_value)

        team_rwoa[team_name] = RWOA(
            total=mean(rwoa_values['total']),
            ct=mean(rwoa_values['t']),
            t=mean(rwoa_values['ct']),
        )

    return team_rwoa
