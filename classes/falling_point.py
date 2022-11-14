class FallingPoint():
    x: float
    y: float
    vel_y: float
    acc_y: float
    max_y: float
    is_past_max: bool = False

    def __init__(self, pos: tuple[float, float], start_vel_y: float, acc_y: float, max_y: float) -> None:
        self.x, self.y = pos
        self.vel_y = start_vel_y
        self.acc_y = acc_y
        self.max_y = max_y
        self.is_past_max = False

    def update(self, dt: float):
        """dt is seconds since last update"""
        self.vel_y += self.acc_y
        self.y += self.vel_y
        if self.y >= self.max_y:
            self.is_past_max = True
