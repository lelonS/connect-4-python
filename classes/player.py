class Player:
    name: str
    color: tuple[int, int, int]  # RGB
    wins: int
    ties: int
    losses: int
    games: int  # wins + ties + losses

    def __init__(self, name: str, color: tuple[int, int, int]) -> None:
        self.name = name
        self.color = color
        self.wins = 0
        self.ties = 0
        self.losses = 0
        self.games = 0
