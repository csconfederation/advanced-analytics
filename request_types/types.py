from typing import Dict, List, Optional, Any
from pydantic import BaseModel, field_validator
from typing import Union, List


class Winner(BaseModel):
    name: str


class Stat(BaseModel):
    homeScore: int
    awayScore: int
    winner: Optional[Winner]


class MatchDay(BaseModel):
    number: int

    @field_validator("number", mode="before")
    @classmethod
    def parse_match_day_number(cls, v: Any):
        if isinstance(v, str):
            return int(v.lstrip("M"))
        return v


class Player(BaseModel):
    name: str
    type: str


class Home(BaseModel):
    name: str
    players: List[Player]


class Away(BaseModel):
    name: str
    players: List[Player]


class TeamStat(BaseModel):
    name: str
    score: int


class Round(BaseModel):
    winnerENUM: int  # 2 is T 3 is CT
    winnerClanName: str


class Match(BaseModel):
    tier: str
    matchId: str
    mapName: str
    rounds: List[Round]


class PlayerStat(BaseModel):
    name: str
    rating: float
    TRating: float
    ctRating: float
    teamClanName: str
    rounds: int
    match: Match


class Division(BaseModel):  # Base class for Premier, Elite, Challenger, etc.
    id: str
    completedAt: str
    stats: List[Stat]
    matchDay: MatchDay
    home: Home
    away: Away
    playerStats: List[PlayerStat]


class Premier(Division):
    pass


class Elite(Division):
    pass


class Challenger(Division):
    pass


class Contender(Division):
    pass


class Prospect(Division):
    pass


class Recruit(Division):
    pass


DivisionUnion = Union[
    List[Premier],
    List[Elite],
    List[Challenger],
    List[Contender],
    List[Prospect],
    List[Recruit],
]


class StitchedStats(BaseModel):
    Premier: List[Premier]
    Elite: List[Elite]
    Challenger: List[Challenger]
    Contender: List[Contender]
    Prospect: List[Prospect]
    Recruit: List[Recruit]


class Score(BaseModel):
    t_rounds_won: int
    ct_rounds_won: int
    total_rounds_won: int


class MatchResult(BaseModel):
    my: Score
    opponent: Score


class MatchDetail(BaseModel):
    map: str
    score: MatchResult


class LeagueMatches(BaseModel):
    matches: Dict[str, Dict[str, MatchDetail]]


class TeamRoundWinPercentage(BaseModel):
    rounds_won: int
    rounds_played: int
    t_rounds_won: int
    t_rounds_played: int
    ct_rounds_won: int
    ct_rounds_played: int
    percentage: float
    t_percentage: float
    ct_percentage: float


class TeamStrengthOfSchedule(BaseModel):
    opponent_rounds_won: int
    opponent_rounds_played: int
    percentage: float


class TeamAverageRating(BaseModel):
    rating: float
    t_rating: float
    ct_rating: float


TeamRoundWinPercentages = Dict[str, TeamRoundWinPercentage]


class RWOA(BaseModel):
    total: float
    t: float
    ct: float
