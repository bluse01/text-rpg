from characters import random

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
            name = "Big Healing Potion"
            gold_cost = 50
            heal_amount = 100
        else:
            raise ValueError("Invalid potion size!")

        super().__init__(name, f"Restores {heal_amount} HP", gold_cost, usable=True)
        self.heal_amount = heal_amount

    def pot_roll():
        # Returns a random size string
        roll = random.randint(0, 2)
        if roll == 0:
            return "small"
        elif roll == 1:
            return "medium"
        else:
            return "large"

    def use(self, player):
        if super().use(player):
            heal = min(player.max_health - player.current_health, self.heal_amount)
            player.current_health += heal
            print(f"You used {self.name} and healed for {heal} HP!")
            return True
        return False