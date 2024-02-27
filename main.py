import csv

from generate_stats.base_stats import (
    get_match_info_by_team_for_tier,
    get_round_win_percentage_by_team,
    get_strength_of_schedule_by_team,
    get_win_loss_record_by_team,
)
from generate_stats.get_and_stitch_stats import get_stats
from generate_stats.rwoa import get_rwoa_by_team
from request_types.types import DivisionUnion

stats = get_stats()

def calculate_tier_stats(tier: DivisionUnion, csv_writer):
    league_matches = get_match_info_by_team_for_tier(tier)
    round_win_percents = get_round_win_percentage_by_team(league_matches)
    strength_of_schedule = get_strength_of_schedule_by_team(
        league_matches, round_win_percents
    )
    team_rwoas = get_rwoa_by_team(league_matches, round_win_percents)
    win_loss_records = get_win_loss_record_by_team(league_matches)

    # Sort team_rwoas by tier, then win desc, then RD desc
    sorted_teams = sorted(team_rwoas.items(), key=lambda x: (
        type(tier[0]).__name__, 
        -win_loss_records[x[0]].wins, 
        -win_loss_records[x[0]].total_round_difference
    ))


    # Write RWOA and SOS to CSV file
    for team, rwoa in sorted_teams:
        win_loss = win_loss_records[team]
        csv_writer.writerow([
            type(tier[0]).__name__,
            team,
            win_loss.wins,
            win_loss.losses,
            win_loss.total_round_difference,
            f"{round(win_loss.t_side_win_rate * 100, 2)}%",
            f"{round(win_loss.ct_side_win_rate * 100, 2)}%",
            f"{round((rwoa.total - 1) * 100, 2)}%",
            f"{round((rwoa.t - 1) * 100, 2)}%",
            f"{round((rwoa.ct - 1) * 100, 2)}%",
            f"{strength_of_schedule[team].percentage}%",
        ])


tiers = [
    stats.Challenger,
    stats.Contender,
    stats.Elite,
    stats.Premier,
    stats.Prospect,
    stats.Recruit,
]

with open(f"rwoa.csv", "w", newline='') as rwoa_f:
    csv_writer = csv.writer(rwoa_f)
    csv_writer.writerow(["Tier", "Team", "W", "L", "RD", "TWin", "CTWin", "RWOA Total", "T RWOA", "CT RWOA", "SOS"])
    for tier in tiers:
        calculate_tier_stats(tier, csv_writer)
