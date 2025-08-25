class Passive:
    def __init__(self, name, dec):
        self.name = name
        self.dec = dec

    def apply(self, player):
        pass

class Overcrit(Passive):
    def __init__(self):
        super().__init__(
            name = "Overcrit", 
            dec = f"Excess crit chance above 100% is converted into crit multiplier."
        )

    def apply(self, player):
        if player.crit_chance > 100:
            overflow = player.crit_chance - 100
            player.crit_multiplier += overflow / 50
            player.crit_chance = 100