import random
from passives import Infection
from shop import create_items, clear_shop
from DOTS import DOTManager

class BaseCharacter:
    def __init__(self, base_damage, base_damage_current, health, armor, crit_chance, crit_multiplier, passives, name):
            self.base_damage = base_damage
            self.base_damage_current = base_damage_current
            self.armor = armor
            self.max_health = health
            self.current_health = health
            self.crit_chance = crit_chance
            self.crit_multiplier = crit_multiplier
            self.passives = passives
            self.name = name
    
            self.base_damage_current = base_damage

            self.dot_manager = DOTManager()

    def calc_damage(self, target):
            crit_roll = random.randint(0, 100)
            is_crit = crit_roll <= self.crit_chance

            if is_crit:
                # Critical hit
                damage = self.base_damage_current * self.crit_multiplier - target.armor
                damage = max(damage, 2)
            else:
                # Normal hit
                damage = self.base_damage_current - target.armor
                damage = max(damage, 1)

            return round(damage, 2), is_crit
    
    def calc_overcharge(self, target):
            damage = self.base_damage_current * 3 - (target.armor / 2)

            return round(damage, 2)
            
class Player(BaseCharacter):
    def __init__(self, level, experience, room, stat_points, char_class, gold=0):
        # Player bla bla bla
        self.level = level
        self.experience = experience
        self.room = room
        self.stat_points = stat_points
        self.char_class = char_class
        self.gold = gold
        self.inventory = []

        # player class values
        self.double_strike_chance = 0
        self.life_steal = 0
        self.overcharge_boost = 1.0
        self.toughness_modfier = 0

        self.bonus_damage = 0
        self.bonus_health = 0
        self.bonus_armor = 0
        self.bonus_crit_chance = 0
        self.bonus_crit_multiplier = 0

        # Initialize with temporary stats (will recalc immediately)
        super().__init__(base_damage=1, base_damage_current=1, health=1, armor=0, crit_chance=0, crit_multiplier=0, passives = [], name="Player")  

        self.recalc_stats()
        self.current_health = self.max_health
        self.base_damage_current = self.base_damage

        if self.char_class == "Warrior":
            self.bonus_health += 15  # +15% health
            self.bonus_armor += 15   # +15% armor
            self.toughness_modfier += 0.90
        elif self.char_class == "Mage":
            self.bonus_damage += 10  # +10% damage
            self.overcharge_boost = 2  # +100% Overcharge damage Boost
        elif self.char_class == "Assassin":
            self.bonus_crit_chance += 15  # +15% crit chance
            self.bonus_crit_multiplier += 20  # +20% crit multiplier bonus
            self.double_strike_chance += 10  # 10% chance to attack twice
        elif self.char_class == "Vampire":
            self.bonus_health += 10  # +10% health
            self.life_steal = 0.1  # 10% life steal 

    def add_passive(self, passive):
        # Check if we already have this passive type
        for existing_passive in self.passives:
            if type(existing_passive) == type(passive):
                return
            
        self.passives.append(passive)
        passive.on_entity_apply_hook(self)  # Apply it immediately

    def check_for_passives(self):
        # if crit more and 100 then add passive: Overcrit
        if self.crit_chance > 100:
            from passives import Overcrit
            self.add_passive(Overcrit())
 
    def recalc_stats(self):
        # Calculate base stats first
        self.base_damage = 10 * self.level
        self.max_health = 100 * self.level
        self.armor = 5 + (0.1 * self.level)
        self.crit_chance = 1 + (0.5 * self.level)
        self.crit_multiplier = 1 + (0.05 * self.level)

        # Apply bonuses (convert percentage bonuses to multipliers)
        self.base_damage = round(self.base_damage * (1 + self.bonus_damage/100), 2)
        self.max_health = round(self.max_health * (1.5 + self.bonus_health/100), 2)
        self.armor = round(self.armor * (1.5 + self.bonus_armor/100), 2)
        self.crit_chance = round(self.crit_chance + self.bonus_crit_chance, 2)
        # Crit multiplier is now multiplicative: base * (1 + bonus/100)
        self.crit_multiplier = round(self.crit_multiplier * (1 + self.bonus_crit_multiplier/100), 2)

        if self.char_class == "Assassin":
            self.double_strike_chance = 10 + (10 * self.level)
            if self.double_strike_chance > 100:
                self.double_strike_chance = 100
        elif self.char_class == "Vampire":
            self.life_steal = 0.1 + (0.02 * self.level)

        # readd passives after calling recalc_stats()
        for passive in self.passives:
            passive.on_entity_apply_hook(self)

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
            # give player 50 gold per level up
            self.gold += 50
            print(f"You have leveled up to level {self.level}! You have {self.stat_points} stat points to spend.")
            
    def level_up(self, levels=1, heal_on_level=True):
        self.level += levels
        self.recalc_stats()
        clear_shop()
        if heal_on_level:
            self.current_health = self.max_health

class Monster(BaseCharacter):
    def __init__(self, base_damage, base_damage_current,health, armor, crit_chance, crit_multiplier, passives, name, tier):
        super().__init__(base_damage, base_damage_current, health, armor, crit_chance, crit_multiplier, passives, name)
        self.base_damage_current = base_damage
        self.current_health = self.max_health
        self.tier = tier