import random
from passives import Overcrit

class BaseCharacter:
    def __init__(self, base_damage, health, armor, crit_chance, crit_multiplier, name):
            self.base_damage = base_damage
            self.armor = armor
            self.max_health = health
            self.current_health = health
            self.crit_chance = crit_chance
            self.crit_multiplier = crit_multiplier
            self.name = name

    def calc_damage(self, target):
            crit_roll = random.randint(0, 100)
            is_crit = crit_roll <= self.crit_chance
            if is_crit:
                # Critical hit
                damage = self.base_damage * self.crit_multiplier - target.armor
                damage = max(damage, 2)
            else:
                # Normal hit
                damage = self.base_damage - target.armor
                damage = max(damage, 1)

            return round(damage, 2), is_crit
    
    def calc_overcharge(self):
            damage = self.base_damage * 3

            return damage
            
class Player(BaseCharacter):

    def __init__(self, level=1, experience=0, room=1, stat_points=0, name="Player"):
        # Extra player-specific fields
        self.level = level
        self.experience = experience
        self.room = room
        self.stat_points = stat_points
        self.name = name
        self.passives = []

        self.bonus_damage = 0
        self.bonus_health = 0
        self.bonus_armor = 0
        self.bonus_crit_chance = 0
        self.bonus_crit_multiplier = 0

        # Initialize with temporary stats (will recalc immediately)
        super().__init__(base_damage=1, health=1, armor=0, crit_chance=0, crit_multiplier=0, name=name)  

        self.recalc_stats()
        self.current_health = self.max_health

    def add_passive(self, passive):
        # Check if we already have this passive type
        for existing_passive in self.passives:
            if type(existing_passive) == type(passive):
                return
            
        self.passives.append(passive)
        passive.apply(self)  # Apply it immediately

    def check_for_passives(self):
        # Check for Overcrit passive
        if self.crit_chance > 100:
            from passives import Overcrit
            self.add_passive(Overcrit())
 
    def recalc_stats(self):
        # Calculate base stats first
        self.base_damage = 13 * self.level
        self.max_health = 100 * self.level
        self.armor = 5 + (0.1 * self.level)
        self.crit_chance = 1 + (0.1 * self.level)
        self.crit_multiplier = 1 + (0.01 * self.level)

        # Apply bonuses
        self.base_damage = round(self.base_damage + self.bonus_damage, 2)
        self.max_health = round(self.max_health + self.bonus_health, 2)
        self.armor = round(self.armor + self.bonus_armor, 2)
        self.crit_chance = round(self.crit_chance + self.bonus_crit_chance, 2)
        self.crit_multiplier = round(self.crit_multiplier + self.bonus_crit_multiplier, 2)

        self.check_for_passives()

    def experience_to_next_level(self):
        return 100 * self.level
    
    def stat_allocation(self, stat, points):
        if points > self.stat_points:
            print("Not enough stat points.")
            return
        if stat == "damage":
            # Each point increases base damage by 2%
            self.bonus_damage += points * 2
            
        elif stat == "health":
            # Each point increases max health by 2%
            self.bonus_health += points * 2
            self.current_health = self.max_health  # Heal to full on health increase

        elif stat == "armor":
            # Each point increases armor by 2%
            self.bonus_armor += points * 2

        elif stat == "crit_chance":
            # Each point increases crit chance by 2%
            self.bonus_crit_chance += points * 2

        elif stat == "crit_multiplier":
            # Each point increases crit multiplier by 1%
            self.bonus_crit_multiplier += points * 1
            # ensure crit multiplier does not exceed 3x
            if self.crit_multiplier + self.bonus_crit_multiplier > 3:
                self.bonus_crit_multiplier = 3 - self.crit_multiplier
            
        else:
            print("Invalid stat.")
            return
        
        self.stat_points -= points
        self.recalc_stats()
        print(f"Allocated {points} points to {stat}.")

    def added_experience(self, amount):
        self.experience += amount
        while self.experience >= self.experience_to_next_level():
            self.experience -= self.experience_to_next_level()
            self.level_up()
            self.stat_points += 5
            print(f"You have leveled up to level {self.level}! You have {self.stat_points} stat points to spend.")
            
    def level_up(self, levels=1, heal_on_level=True):
        self.level += levels
        self.recalc_stats()
        if heal_on_level:
            self.current_health = self.max_health

class Monster(BaseCharacter):
    def __init__(self, base_damage, health, armor, crit_chance, crit_multiplier, name, tier):
        super().__init__(base_damage, health, armor, crit_chance, crit_multiplier, name)
        self.current_health = self.max_health
        self.tier = tier