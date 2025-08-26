from Items import *
from characters import random
from termcolor import colored

# possible items that can exist
# needs to be manually updated like a pro
global possible_item_list
possible_item_list = ["HealingPotion"]

# this function should be called after level up
# or when player rests
def create_items():
    # how many times item are created
    hw_items = 4
    item_list = []

    while len(item_list) < hw_items:
        item_random_roll = random.randint(0, len(possible_item_list))
        item_list.append(possible_item_list[item_random_roll])

    return item_list

def shop_menu(player):
    # crashes after first entry! fix it
    items_for_sale = create_items()
    
    print(colored("\n🛒 Welcome to the Adventurer's Shop! 🛒", "cyan", attrs=["bold"]))
    print(colored("Here are the items available today:\n", "yellow"))
    print(colored(f"You're gold amount: {player.gold}", "yellow"))
    
    potion_objects = []  # store the actual item objects

    for idx, item_name in enumerate(items_for_sale, start=1):
        if item_name == "HealingPotion":
            size = HealingPotion.pot_roll()        
            potion = HealingPotion(size)           
            potion_objects.append(potion)       
            color = "green"
            desc = potion.desc
        else:
            desc = "A mysterious item."
            color = "magenta"

        print(f"{colored(str(idx) + '.', 'cyan')} {colored(potion.name, color, attrs=['bold'])} - {desc} | {colored('Gold : ' + str(potion.gold_cost), 'yellow')}")
    
    print(colored("\nChoose an item to buy (1-4) or 0 to exit:", "yellow"))
    choice = input("> ")
    
    if choice.isdigit():
        choice = int(choice)
        if choice == 0:
            print(colored("Leaving the shop... Good luck on your adventure!", "cyan"))
            return
        elif 1 <= choice <= len(items_for_sale):
            selected_item = potion_objects[choice - 1]
            # Add to player's inventory
            # if player has enough gold
            if player.gold > potion.gold_cost:
                player.inventory.append(selected_item)
                print(colored(f"You bought {selected_item.name}! It has been added to your inventory.", "green"))
            else:
                print(colored("You don't have enough gold!", "red"))
        else:
            print(colored("Invalid choice. Try again.", "red"))
    else:
        print(colored("Invalid input. Please enter a number.", "red"))