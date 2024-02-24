from statistics import mean

from request_types.types import *


def get_rwoa_by_team(
    league_matches: LeagueMatches, round_win_percentage: TeamRoundWinPercentages
):
    rwoa = {}

    for team in league_matches.matches:
        total_opponent_rounds_won = 0
        total_opponent_rounds_played = 0
        total_t_opponent_rounds_won = 0
        total_t_opponent_rounds_played = 0
        total_ct_opponent_rounds_won = 0
        total_ct_opponent_rounds_played = 0
        total_won_bias = 0
        total_played_bias = 0
        total_t_won_bias = 0
        total_t_played_bias = 0
        total_ct_won_bias = 0
        total_ct_played_bias = 0

        total_rwoa = []
        total_t_rwoa = []
        total_ct_rwoa = []

        for opponent in league_matches.matches[team]:
            won_bias = league_matches.matches[team][
                opponent
            ].score.opponent.total_rounds_won
            t_won_bias = league_matches.matches[team][
                opponent
            ].score.opponent.t_rounds_won
            ct_won_bias = league_matches.matches[team][
                opponent
            ].score.opponent.ct_rounds_won
            played_bias = (
                league_matches.matches[team][opponent].score.opponent.total_rounds_won
                + league_matches.matches[team][opponent].score.my.total_rounds_won
            )
            t_played_bias = (
                league_matches.matches[team][opponent].score.opponent.t_rounds_won
                + league_matches.matches[team][opponent].score.my.ct_rounds_won
            )
            ct_played_bias = (
                league_matches.matches[team][opponent].score.opponent.ct_rounds_won
                + league_matches.matches[team][opponent].score.my.t_rounds_won
            )
            total_won_bias += won_bias
            total_played_bias += played_bias
            total_t_won_bias += t_won_bias
            total_t_played_bias += t_played_bias
            total_ct_won_bias += ct_won_bias
            total_ct_played_bias += ct_played_bias

            opponent_rounds_won = round_win_percentage[opponent].rounds_won - won_bias
            opponent_rounds_played = (
                round_win_percentage[opponent].rounds_played - played_bias
            )
            t_opponent_rounds_won = (
                round_win_percentage[opponent].t_rounds_won - t_won_bias
            )
            t_opponent_rounds_played = (
                round_win_percentage[opponent].t_rounds_played - t_played_bias
            )
            ct_opponent_rounds_won = (
                round_win_percentage[opponent].ct_rounds_won - ct_won_bias
            )
            ct_opponent_rounds_played = (
                round_win_percentage[opponent].ct_rounds_played - ct_played_bias
            )

            total_opponent_rounds_won += opponent_rounds_won
            total_opponent_rounds_played += opponent_rounds_played
            total_t_opponent_rounds_won += t_opponent_rounds_won
            total_t_opponent_rounds_played += t_opponent_rounds_played
            total_ct_opponent_rounds_won += ct_opponent_rounds_won
            total_ct_opponent_rounds_played += ct_opponent_rounds_played

            opponent_rwp = (
                opponent_rounds_won / opponent_rounds_played
                if opponent_rounds_played != 0
                else 0
            )
            t_opponent_rwp = (
                t_opponent_rounds_won / t_opponent_rounds_played
                if t_opponent_rounds_played != 0
                else 0
            )
            ct_opponent_rwp = (
                ct_opponent_rounds_won / ct_opponent_rounds_played
                if ct_opponent_rounds_played != 0
                else 0
            )

            rwp = won_bias / played_bias if played_bias != 0 else 0
            t_rwp = t_won_bias / t_played_bias if t_played_bias != 0 else 0
            ct_rwp = ct_won_bias / ct_played_bias if ct_played_bias != 0 else 0

            total_rwoa.append((1 - rwp) / (1 - opponent_rwp))
            total_t_rwoa.append((1 - t_rwp) / (1 - t_opponent_rwp))
            total_ct_rwoa.append((1 - ct_rwp) / (1 - ct_opponent_rwp))

        rwoa[team] = RWOA(
            total=mean(total_rwoa),
            t=mean(total_ct_rwoa),
            ct=mean(total_t_rwoa),
        )

    return rwoa
