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


def calculate_tier_stats(tier: DivisionUnion, rwoa_f, sos_f):
    # LeagueMatches allows us to calculate RWP, SOS, and RWOA
    league_matches = get_match_info_by_team_for_tier(tier)
    round_win_percents = get_round_win_percentage_by_team(league_matches)
    strength_of_schedule = get_strength_of_schedule_by_team(
        league_matches, round_win_percents
    )
    team_rwoas = get_rwoa_by_team(league_matches, round_win_percents)

    # Write RWOA and SOS to CSV file
    for team in team_rwoas:
        rwoa_f.write(
            f"{type(tier[0]).__name__},{team},{round((team_rwoas[team].total - 1) * 100, 2)}%,{round((team_rwoas[team].t - 1) * 100, 2)}%,{round((team_rwoas[team].ct - 1) * 100, 2)}%\n"
        )

    for team in strength_of_schedule:
        sos_f.write(
            f"{type(tier[0]).__name__},{team},{strength_of_schedule[team].percentage}\n"
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
    rwoa_f.write("Tier,Team,Total,T,CT\n")
    with open(f"sos.csv", "w") as sos_f:
        sos_f.write("Tier,Team,SOS\n")
        for tier in tiers:
            calculate_tier_stats(tier, rwoa_f, sos_f)
