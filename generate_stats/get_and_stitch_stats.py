import requests
from collections import Counter

from request_types.types import StitchedStats


def get_stats(season: int) -> StitchedStats:
    # URL and payload for the first GraphQL query
    url1 = "https://stats.csconfederation.com/graphql"
    query1 = {
        "query": f"""
      {{
        findManyPlayerMatchStats(
          where: {{match: {{season: {{equals: {season}}}, matchType: {{equals: Regulation}}}}, side: {{equals: 4}}}}
        ) {{
          name
          steamID
          rating
          TRating
          ctRating
          teamClanName
          rounds
          match {{
            tier
            matchId
            mapName
            rounds {{
              winnerENUM
              winnerClanName
            }}
          }}
        }}
      }}
      """
    }

    # URL and payload for the second GraphQL query
    url2 = "https://core.csconfederation.com/graphql"
    query2 = {
        "query": f"""
      {{
          matches(season: {season}) {{
              id
              completedAt
              stats {{
                  homeScore
                  awayScore
                  winner {{
                      name
                  }}
              }}
              matchDay {{
                  number
              }}
              home {{
                  name
                  players {{
                      name
                      type
                  }}
              }}
              away {{
                  name
                  players {{
                      name
                      type
                  }}
              }}
          }}
      }}
      """
    }

    # Function to perform a GraphQL query
    def perform_query(url, query):
        headers = {"Content-Type": "application/json"}
        response = requests.post(url, json=query, headers=headers)
        if response.status_code == 200:
            return response.json()
        else:
            return f"Query failed with status code {response.status_code}"

    # Perform both queries
    player_match_stats_data = perform_query(url1, query1)
    matches_data = perform_query(url2, query2)

    if (
        not isinstance(player_match_stats_data, dict)
        or "data" not in player_match_stats_data
    ):
        raise ValueError(
            f"Failed to fetch or parse player match stats. Response: {player_match_stats_data}"
        )
    if not isinstance(matches_data, dict) or "data" not in matches_data:
        raise ValueError(
            f"Failed to fetch or parse matches data. Response: {matches_data}"
        )

    def add_player_match_stats_to_matches(matches, player_match_stats):
        """
        Adds player match stats to the matches based on matching matchId and matches id.

        :param matches: A list of match dictionaries from the second query.
        :param player_match_stats: A list of player match stat dictionaries from the first query.
        :return: The updated list of matches with player match stats added.
        """
        # Create a dictionary for quick access to matches by their ID
        matches_dict = {match["id"]: match for match in matches}

        # Iterate over player match stats
        for player_stat in player_match_stats["data"]["findManyPlayerMatchStats"]:
            match_id = player_stat["match"]["matchId"]

            # Check if this player_stat's matchId exists in the matches
            if match_id in matches_dict:
                # Add 'playerStats' key to the match if it doesn't exist
                if "playerStats" not in matches_dict[match_id]:
                    matches_dict[match_id]["playerStats"] = []

                # Append the player_stat to the 'playerStats' list of the match
                matches_dict[match_id]["playerStats"].append(player_stat)

        # Return the updated list of matches
        return list(matches_dict.values())

    # Assume matches_data is the result list from the second query
    # Assume player_match_stats_data is the result list from the first query

    filtered_matches = [
        match
        for match in matches_data["data"]["matches"]
        if len(match["stats"]) > 0 and match["completedAt"] is not None
    ]

    # Example usage
    updated_matches = add_player_match_stats_to_matches(
        filtered_matches, player_match_stats_data
    )

    # Filter out any matches that don't have playerStats
    updated_matches = [match for match in updated_matches if "playerStats" in match]

    def get_most_frequent_tier(player_stats):
        """
        Determines the most frequent tier in the player stats.
        If there's a tie, one of the most frequent tiers is returned.
        """
        tiers = [stat["match"]["tier"] for stat in player_stats if "match" in stat]
        if not tiers:
            return "Unknown Tier"
        most_common = Counter(tiers).most_common(1)
        return most_common[0][0]

    def group_matches_by_tier(matches):
        """
        Groups matches into tiers based on the most frequent tier in their playerStats.

        :param matches: A list of match dictionaries, with player match stats added.
        :return: A dictionary with keys as 'TierName' and values as lists of matches belonging to those tiers.
        """
        tier_dict = {}
        for match in matches:
            # Determine the most frequent tier for the match
            tier = get_most_frequent_tier(match.get("playerStats", []))

            # Initialize the list for the tier if it does not exist
            if tier not in tier_dict:
                tier_dict[tier] = []

            # Append the match to the appropriate tier list
            tier_dict[tier].append(match)

        return tier_dict

    # Assuming updated_matches is the list of matches with playerStats included
    return StitchedStats.model_validate(group_matches_by_tier(updated_matches))
