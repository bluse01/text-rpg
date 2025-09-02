import random
from termcolor import colored

class Item:
    all_Items = []

    def __init__(self, name, desc, gold_cost, usable=False):
        self.name = name
        self.desc = desc
        self.gold_cost = gold_cost
        self.usable = usable
        Item.all_Items.append(self)
        
    def use(self, player):
        if not self.usable:
            print(f"The {self.name} is not a consumable!")
            return False
        return True
    
class HealingPotion(Item):
    def __init__(self, size="small"):

        if size == "small":
            name = "Small Healing Potion"
            gold_cost = 15
            heal_amount = 25
        elif size == "medium":
            name = "Medium Healing Potion"
            gold_cost = 30
            heal_amount = 50
        elif size == "large":
            name = "Large Healing Potion"
            gold_cost = 50
            heal_amount = 100
        else:
            raise ValueError("Invalid potion size!")

        super().__init__(name, f"Restores {heal_amount} HP", gold_cost, usable=True)
        self.heal_amount = heal_amount

    def pot_roll():
        # Returns a random size string
        roll = random.randint(0, 100)
        if roll >= 75:
            return "large"
        elif roll >= 25:
            return "medium"
        elif roll >= 0:
            return "small"

    def use(self, player):
        if super().use(player):
            heal = min(player.max_health - player.current_health, self.heal_amount)
            player.current_health += heal
            print(f"You used {self.name} and healed for {heal} HP!")
            return True
        return False
    
class PocketBomb(Item):
    def __init__(self, bomb_type="small"):
        if bomb_type == "small":
            name = "Small Pocket Bomb"
            gold_cost = 25
            damage = 15
        elif bomb_type == "medium":
            name = "Medium Pocket Bomb"
            gold_cost = 55
            damage = 45
        elif bomb_type == "large":
            name = "Large Pocket Bomb"
            gold_cost = 125
            damage = 80
        else:
            raise ValueError("Invalid bomb type!")

        super().__init__(name, f"Deals {damage} damage to enemy (Combat only)", gold_cost, usable=True)
        self.damage = damage
        self.bomb_type = bomb_type

    def bomb_roll():
        roll = random.randint(0, 100)
        if roll >= 75:
            return "large"
        elif roll >= 25:
            return "medium"
        elif roll >= 0:
            return "small"

    def use(self, player, monster=None):
        if monster is None:
            print("Can't use the bomb outside of combat!")
            return False
        
        # Calculate damage (ignores armor)
        damage = self.damage
        monster.current_health -= damage
        print(f"You throw a {self.name}! It explodes dealing {colored(damage, "yellow")} damage to {monster.name}!")
        return True
    
class Armorkit(Item):
    def __init__(self):
        super().__init__(
            name = "Armor Repair Kit",
            desc = f"Increases armor by 25% for next combat",
            gold_cost = 100,
            usable = True
        )
        self.armor_boost = 0.25

    def use(self, player, monster = None):
        if hasattr(player, 'temp_armor_boost'):
            print("Your armor is already reinforced!")
            return False
            
        player.temp_armor_boost = self.armor_boost
        print(f"You reinforce your armor! Your armor will be 25% stronger in the next combat!")
        return True
    
class LuckyCharm(Item):
    def __init__(self):
        super().__init__(
            name = "Lucky Charm",
            desc = "Increases crit chance by 15% for next combat",
            gold_cost = 50,
            usable = True
        )
        self.crit_boost = 15

    def use(self, player, monster = None):
        if hasattr(player, "temp_crit_boost"):
            print("You already have a luck boost active!")
            return False
        
        player.temp_crit_boost = self.crit_boost
        print(f"You activate the lucky charm! Your crit chance will be 15% higher in the next combat!")
        return True

class VampirePotion(Item):
    def __init__(self):
        super().__init__(
            name = "Vampire Potion",
            desc = "On use gain +0.2 life steal!",
            gold_cost = 30,
            usable = True
        )
        self.lifesteal_boost = 0.2
    
    def use(self, player, monster = None):
        if hasattr(player, "temp_lifesteal_boost"):
            print("You already have a life steal boost active!")
            return False
        
        player.temp_lifesteal_boost = self.lifesteal_boost
        print("You activate the life steal! Next combat you heal more!")
        return True

class ManaPotion(Item):
    def __init__(self):
        super().__init__(
            name = "Mana Potion",
            desc = "On use gain +4 Mana!",
            gold_cost = 20,
            usable = True
        )
        self.gain_mana = 4

    def use(self, player, monster = None):
        if monster is None:
            print("You can't use this item outside of combat!")
            return False

        player.mana += self.gain_mana
        print(colored(f"You Used a mana potion gained {colored('4 - mana', 'blue')}!", "green"))

class SharpeningStone(Item):
    def __init__(self):
        super().__init__(
            name="Sharpening Stone",
            desc=f"Increases damage by 20% for next combat",
            gold_cost=60,
            usable=True
        )
        self.damage_boost = 0.2

    def use(self, player, monster=None):
        if hasattr(player, 'temp_damage_boost'):
            print("You already have a damage boost active!")
            return False
            
        player.temp_damage_boost = self.damage_boost
        print(colored(f"You sharpen your weapon! Your next combat will deal 20% more damage!", "green"))
        return True
