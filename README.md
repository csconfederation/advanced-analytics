# Counter-Strike Team Performance Metrics

This document outlines the methodology and various factors used to evaluate the performance of teams in Counter-Strike. These metrics are divided into three main categories: raw factors, semi-calculated factors, and super calculated factors, each offering a unique insight into team performance dynamics.

## Raw Factors

- **RWP (Round Win Percentage):** The percentage of rounds won by a team.
- **SOS (Strength of Schedule):** The difficulty level of the opponents faced by the team.
- **Rating:** The average rating of the team, considering all players.

## Semi-Calculated Factors

- **RWOA (Rounds Won Over Average):** This metric provides a team-by-team comparison of rounds won against an opponent versus the average rounds won against the same opponent by other teams.
- **Map Pool Distribution:** An analysis of the variety and outcomes of maps played by the team.
- **Substitutes:** Considers the impact of substitute players on team performance.
- **Starting Side Analysis:** Breaks down performance based on whether the team starts on the Terrorist (T) or Counter-Terrorist (CT) side.

## Super Calculated Factors

- **Side-Based RWOA:** An advanced version of RWOA that also takes into account the starting side (T vs. CT) to provide a deeper analysis of performance.
- **Aggression Factor:** Calculates a team's aggressiveness by factoring in the average round time, giving insight into their playstyle.
- **ML RWOA (Machine Learning RWOA):** An iterative calculation of RWOA that uses a cyclical approach to refine the metric. It involves map-based RWOA adjustments, excluding matches between the two subject teams, and iterates to reach a stable assessment of direct competition performance.
