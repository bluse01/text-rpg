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
            dec="On hit chance to deal 1.5x damage and apply Infection DOT.")
    
    def on_combat_hook(self, damage):
        on_roll = random.randint(0, 100)

        if on_roll < 25:
            damage = damage * 1.5
            print(f"{colored('Infection triggered!', 'green')} +50% damage!")
            return damage, True
        return damage, False  

class Slash(Passive):
    def __init__(self):
        super().__init__(
            name = "Slash", 
            dec = "On hit chance to deal 1.5x damage and apply Bleed DOT.")

    # WP working on it
    def on_combat_hook(self, damage, target=None):
        on_roll = random.randint(0, 100)

        if on_roll < 25:
            damage = damage * 1.5
            print(f"{colored('Bleed triggered!', 'red')} +50% damage!")
            return damage, True
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
            return True
        return False

class OverHeal(Passive):
    def __init__(self):
        super().__init__(
            name = "OverHeal",
            dec = "Excess heal converts to overguard."
        )

    # if lifesteal over 1 do this
    def on_entity_apply_hook(self, entity):
        if entity.life_steal >= 1:
            # max_heal is set to max_health so when lifesteal it doesn't go over the threshold
            # this raises the threshold by 50%
            entity.max_heal *= 1.5
            return True
        return False
    
class LuckyStreak(Passive):
    def __init__(self):
        super().__init__(
            name = "Lucky Streak",
            dec = f"Each critical strike landed gain +10% critical strike chance."
        )

    # has a synergy with overcrit
    def on_combat_hook(self, entity):
        try:
            if entity.consecutive_hits != 0:
                # increese by consecutive_hits 50%
                entity.crit_chance = entity.crit_chance * (1 + (entity.consecutive_hits * .5))
            else:
                print("Passive luckystreak value error")

            return True
        except AttributeError:
            return False