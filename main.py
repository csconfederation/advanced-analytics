from request_types.types import DivisionUnion

from generate_stats.base_stats import (
    get_match_info_by_team_for_tier,
    get_round_win_percentage_by_team,
    get_strength_of_schedule_by_team,
    get_average_ratings_by_team,
)
from generate_stats.get_and_stitch_stats import get_stats
from generate_stats.rwoa import get_rwoa_by_team

stats = get_stats()


def calculate_tier_stats(tier: DivisionUnion, rwoa_f):
    # LeagueMatches allows us to calculate RWP, SOS, and RWOA
    league_matches = get_match_info_by_team_for_tier(tier)
    round_win_percents = get_round_win_percentage_by_team(league_matches)
    strength_of_schedule = get_strength_of_schedule_by_team(
        league_matches, round_win_percents
    )
    team_rwoas = get_rwoa_by_team(league_matches, round_win_percents)
    win_loss_records = get_win_loss_record_by_team(league_matches)

    # Write RWOA and SOS to CSV file
    for team in team_rwoas:
        win_loss = win_loss_records[team]
        rwoa_f.write(
            f"{type(tier[0]).__name__},{team},{win_loss.wins},{win_loss.losses},{win_loss.total_round_difference},{round(win_loss.t_side_win_rate * 100, 2)}%,{round(win_loss.ct_side_win_rate * 100, 2)}%,{round((team_rwoas[team].total - 1) * 100, 2)}%,{round((team_rwoas[team].t - 1) * 100, 2)}%,{round((team_rwoas[team].ct - 1) * 100, 2)}%,{strength_of_schedule[team].percentage}\n"
        )


tiers = [
    stats.Recruit,
    stats.Prospect,
    stats.Contender,
    stats.Challenger,
    stats.Elite,
    stats.Premier,
]

with open(f"rwoa.csv", "w") as rwoa_f:
    rwoa_f.write("Tier,Team,W,L,RD,TWin,CTWin,RWOA Total,T RWOA,CT RWOA,SOS\n")
    for tier in tiers:
        calculate_tier_stats(tier, rwoa_f)
