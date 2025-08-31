import random
from termcolor import colored

class Passive:
    def __init__(self, name, dec):
        self.name = name
        self.dec = dec

    # this hook can be called outside combat to add passvies ability to entity
    def on_entity_apply_hook(self, entity):
        pass

    # this hook can be called inside a combat to return modified value
    def on_combat_hook(self, damage):
        pass

class Infection(Passive):
    def __init__(self):
        super().__init__(
            name="Infection", 
            dec="On hit chance to deal 1.5x damage and apply Infection DOT")
    
    def on_combat_hook(self, damage):
        on_roll = random.randint(0, 100)

        if on_roll < 25:
            damage = damage * 1.5
            print(f"{colored('Infection triggered!', 'green')} +50% damage!")
            return damage, True
        # return damage = 0 because combat doesn't check if passive on hit was applied or not
        return 0, False  

class Slash(Passive):
    def __init__(self):
        super().__init__(
            name = "Slash", 
            dec = "On hit chance to deal 1.5x damage to the enemy.")

    def on_combat_hook(self, damage, target=None):
        on_roll = random.randint(0, 1)

        if on_roll:
            damage = damage * 1.5
            return damage, False
        else:
            return damage, False        

class Overcrit(Passive):
    def __init__(self):
        super().__init__(
            name = "Overcrit", 
            dec = f"Excess crit chance above 100% is converted into crit multiplier."
        )

    def on_entity_apply_hook(self, entity):
        if entity.crit_chance > 100:
            overflow = entity.crit_chance - 100
            entity.crit_multiplier += round(overflow / 50)
            entity.crit_chance = 100