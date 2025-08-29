from Items import *
import random
from termcolor import colored

# possible items that can exist 
# needs to be manually updated
possible_item_list = [HealingPotion]
items_for_sale = []

def clear_shop():
    global items_for_sale
    del items_for_sale[:]

# generate items for the shop
# if player levels up call it again
def create_items(num_items=4):
    item_list = []
    while len(item_list) < num_items:
        item_class = random.choice(possible_item_list)  # pick class
        if item_class is HealingPotion:
            size = HealingPotion.pot_roll()
            item = HealingPotion(size)
        else:
            item = item_class()
        item_list.append(item)
    return item_list

# show shop and allow buying
def shop_menu(player):
    global items_for_sale

    # if no stock generate one
    if not items_for_sale:
        items_for_sale = create_items()

    print(colored("\nWelcome to the Adventurer's Shop!", "cyan", attrs=["bold"]))
    print(colored("Here are the items available today:\n", "yellow"))
    print(colored(f"Your gold amount: {player.gold}", "yellow"))

    # display items
    for idx, item in enumerate(items_for_sale, start=1):
        color = "green" if isinstance(item, HealingPotion) else "white"
        print(
            f"{colored(str(idx) + '.', 'cyan')} "
            f"{colored(item.name, color, attrs=['bold'])} - {item.desc} | "
            f"{colored('Gold: ' + str(item.gold_cost), 'yellow')}"
        )

    print(colored("\nChoose an item to buy (1-4) or 0 to exit:", "yellow"))
    choice = input("> ")

    if not choice.isdigit():
        print(colored("Invalid input. Please enter a number.", "red"))
        return

    choice = int(choice)
    if choice == 0:
        print(colored("Leaving the shop... Good luck on your adventure!", "cyan"))
        return

    # shop logic
    if 1 <= choice <= len(items_for_sale):
        selected_item = items_for_sale[choice - 1]
        if player.gold >= selected_item.gold_cost:
            player.inventory.append(selected_item)
            player.gold -= selected_item.gold_cost
            print(colored(f"You bought {selected_item.name}! Added to your inventory.", "green"))
            items_for_sale.pop(choice - 1)
        else:
            print(colored("You don't have enough gold!", "red"))
    else:
        print(colored("Invalid choice. Try again.", "red"))