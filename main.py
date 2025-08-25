import os
import time
from termcolor import colored

from characters import Player, Monster, random

debug_mode = False
player = None

# (next time for me) figure out what math/balanced goes into stat (maybe)
# add class like abilitys in combat (must) working on it
# rebalance monsters to strong at start? (maybe)

def clear():
    os.system("cls" if os.name == "nt" else "clear")

def start():
    global player, debug_mode
    clear()
    print("Welcome to my text game!")
    print("This is a simple text-based adventure.")
    print("Enjoy your journey!")
    print("1. Start Game")
    print("2. Exit")
    print("Please enter your choice (1 or 2): ")
    choice = input("> ")

    if choice == "1":
        print("Starting the game...")
        time.sleep(1)
        game_loop()
    elif choice == "2":
        print("Exiting the game. Goodbye!")
        time.sleep(1)
        exit()
    elif choice.lower() == "debug":
        # entering debug mode
        print("Entering debug mode...")
        print("Creating a debug character...")
        print("Enter level for debug character (default is 1): ")
        level_input = input("> ")
        print("Enter room for debug character (default is 1): ")
        rm_input = input("> ")
        if level_input.isdigit():
            level = int(level_input)
        else:
            level = 1

        if rm_input.isdigit():
            room = int(rm_input)
        else:
            room = 1
        
        player = CreateCharacter()
        player.level = level
        player.room = room
        player.stat_points = level * 5
        player.recalc_stats()
        player.current_health = player.max_health
        print(f"Debug character created at level {player.level} with {player.current_health} health.")
        global debug_mode
        debug_mode = True
        game_loop()
    else:
        print("Invalid choice. Please try again.")
        time.sleep(1)
        start()

def combat(player, monster):
    player_mana = 0
    turn = 1
    is_defending = False

    clear()
    if debug_mode:
        print("[DEBUG] Player Stats:", vars(player))
        print("\n[DEBUG] Monster Stats:", vars(monster))

    while player.current_health > 0 and monster.current_health > 0:
        print(f"\n--- Combat Turn {turn} ---")
        print(f"You'r Health: {colored(round(player.current_health, 2), 'green')} | Mana: {colored(player_mana, 'blue')}")
        print(f"{monster.name}'s Health: {colored(round(monster.current_health, 2), 'yellow')}")
        if player.char_class == "Mage":
            print("1. Attack  2. Defend  3. Overcharge Attack (Cost 6 mana)")
        else:
            print("1. Attack  2. Defend  3. Overcharge Attack (Cost 4 mana)")
        choice = input("> ")

        # ---- Player Action ----
        if choice == "1":
            damage, is_crit = player.calc_damage(monster)
            monster.current_health -= damage
            if is_crit:
                print(f"You land a {colored('critical hit!', 'red')} dealing {colored(damage, 'red')} damage!")
            else:
                print(f"You deal {colored(damage, 'yellow')} damage.")

            if player.char_class == "Vampire":
                heal_amount = damage * player.life_steal
                player.current_health = min(player.max_health, player.current_health + heal_amount)
                print(f"You Heal {colored(round(heal_amount, 2), 'green')} health!")

            if player.char_class == "Assassin" and random.randint(1, 100) <= player.double_strike_chance:
                damage2, is_crit2 = player.calc_damage(monster)
                monster.current_health -= damage2
                if is_crit2:
                    print(f"{colored('Double Strike!', 'cyan')} You land a {colored('critical hit!', 'red')} dealing {colored(damage, 'red')} damage!")
                else:
                    print(f"{colored('Double Strike!', 'cyan')} You deal {colored(damage, 'yellow')} damage.")
            
            if player.char_class == "Mage":
               player_mana += 4 
            else:
                player_mana += 2

        elif choice == "2":
            print("You brace yourself, halving the next attack.")
            is_defending = True
            if player.char_class == "Mage":
                player_mana += 2
            else:
                player_mana += 1

        elif choice == "3":
            if player_mana >= 6 and player.char_class == "Mage":
                damage = player.calc_overcharge(monster)
                # boost damage based on multiplier for mage class
                damage = damage * player.overcharge_boost
                monster.current_health -= damage
                print(f"You unleash an {colored('MEGA Overcharge Attack!', 'cyan')} dealing {colored(damage, 'red')} damage!")
            else:
                if player_mana >= 4:
                    damage = player.calc_overcharge(monster)
                    monster.current_health -= damage
                    print(f"You unleash an {colored('Overcharge Attack!', 'red')} dealing {colored(damage, 'red')} damage!")
                    player_mana -= 4
                else:
                    print("Not enough mana for Overcharge Attack!")
                    continue  # skip to retry input

            if player.char_class == "Vampire":
                heal_amount = damage * player.life_steal
                player.current_health = min(player.max_health, player.current_health + heal_amount)
                print(f"You Heal {colored(round(heal_amount, 2), 'green')} health!")
        turn += 1

        if monster.current_health <= 0:
            return "Monster defeated"

        # ---- Monster Action ----
        damage, is_crit = monster.calc_damage(player)
        
        if player.char_class == "Warrior":
            damage = round(damage * player.toughness_modfier, 2)

        if is_defending:
            damage = damage / 2
            is_defending = False  # reset defense

        player.current_health -= damage
        if is_crit:
            print(f"The {monster.name} lands a {colored('critical hit!', 'red')} for {colored(damage, 'red')} damage!")
        else:
            print(f"The {monster.name} deals {colored(damage, 'yellow')} damage!")

        if player.current_health <= 0:
            if debug_mode:
                return "Debug_safemode"
            return "Player defeated"

def CreateCharacter():
    # Create a new player starting at level 1
    time.sleep(1)
    clear()
    
    print("╔══════════════════════════════╗")
    print("║       CHOOSE YOUR CLASS      ║")
    print("╚══════════════════════════════╝")
    print()
    print("1. Warrior - The mighty tank")
    print("2. Mage    - Master of arcane arts") 
    print("3. Assassin- Silent and deadly")
    print("4. Vampire - Eternal night hunter")
    print()
    
    choice = input("Enter your choice (1-4): ").strip()
    
    class_descriptions = {
        "1": {
            "name": "Warrior",
            "bonus": "Toughness (increased armor)",
            "stats": "+15% Health, +15% Armor"
        },
        "2": {
            "name": "Mage", 
            "bonus": "Magic Overcharge (Overcharge deals more damage)",
            "stats": "+10% Damage, +50% Mana gain"
        },
        "3": {
            "name": "Assassin",
            "bonus": "Double Strike (Chance to attack twice)",
            "stats": "+15% Crit Chance, +10% Crit Multiplier"
        },
        "4": {
            "name": "Vampire",
            "bonus": f"Life Steal (Heal of damage dealt)",
            "stats": f"+10% Health, +5% Life Steal"
        }
    }
    
    if choice in class_descriptions:
        selected = class_descriptions[choice]
        print(f"\n╔{'═'*40}╗")
        print(f"║ You have chosen: {selected['name']:^20}  ║")
        print(f"╚{'═'*40}╝")
        print(f"Class Bonus: {selected['bonus']}")
        print(f"Starting Stats: {selected['stats']}")
        input("Press Enter to continue...")
            
        return Player(level=1, experience=0, room=1, stat_points=0, char_class=selected['name'])
    else:
        print("\nInvalid choice! Defaulting to Adventurer class.")
        time.sleep(1)
        print("You are now an Adventurer - a jack of all trades!")
        return Player(level=1, experience=0, room=1, stat_points=0, char_class="Adventurer")

def monster_encounter(player):
    # List of possible low level monsters
    ll_monsterN = ["Goblin", "Orc", "Troll", "Zombie", "Skeleton", "Slime", "Spider"]
    ml_monsterN = ["Bandit", "Wolf", "Giant Rat", "Harpy", "Gnoll"]
    hl_monsterN = ["Ogre", "Wraith", "Minotaur", "Vampire", "Dragon"]

    room_scale = player.room * 1.5  # scaling factor for the room

    # Create a low level monster based on player level
    if player.level <= 10:
        monster_name = random.choice(ll_monsterN)

        base_damage     = round((12.5 * player.level) + room_scale, 2)
        health          = round((110 * player.level + player.base_damage) + room_scale, 2)
        armor           = round((5 + player.level) + room_scale, 2)
        crit_chance     = round(1.5 + (0.2 * player.level), 2)
        crit_multiplier = round(1 + (0.2 * player.level), 2)
        if crit_multiplier > 2:
            crit_multiplier = 2

        ll_monster = Monster(
            base_damage=base_damage,
            health=health,
            armor=armor,
            crit_chance=crit_chance,
            crit_multiplier=crit_multiplier,
            name=monster_name,
            tier="low"
        )
        return ll_monster
    elif 10 < player.level <= 30:
        monster_name = random.choice(ml_monsterN)

        base_damage     = round((15 * player.level) + room_scale, 2)
        health          = round((230 * player.level + player.base_damage) + room_scale, 2)
        armor           = round((15 + (0.5 * player.level)) + room_scale, 2)
        crit_chance     = round(2 + (0.3 * player.level), 2)
        crit_multiplier = round(1.5 + (0.3 * player.level), 2)
        if crit_multiplier > 3:
            crit_multiplier = 3

        ml_monster = Monster(
            base_damage=base_damage,
            health=health,
            armor=armor,
            crit_chance=crit_chance,
            crit_multiplier=crit_multiplier,
            name=monster_name,
            tier="medium"
        )
        return ml_monster
    elif player.level > 30:
        monster_name = random.choice(hl_monsterN)

        base_damage     = round((20 * player.level) + room_scale, 2)
        health          = round((340 * player.level + player.base_damage) + room_scale, 2)
        armor           = round((20 + (1 * player.level)) + room_scale, 2)
        crit_chance     = round(3 + (0.4 * player.level), 2)
        crit_multiplier = round(2 + (0.4 * player.level), 2)
        if crit_multiplier > 5:
            crit_multiplier = 5

        hl_monster = Monster(
            base_damage=base_damage,
            health=health,
            armor=armor,
            crit_chance=crit_chance,
            crit_multiplier=crit_multiplier,
            name=monster_name,
            tier="high"
        )
        return hl_monster
    else:
        print("No monsters available for your level.")
        return

def game_loop(): 
    global player
    clear()
    if player is None:
        player = CreateCharacter()  
        print("Character created! Let the adventure begin!\n")

    def room_create(player):
        print(f"\nYou are in room {player.room}.")
        print("You see a door to the north and a door to the east.")
        print("What do you want to do?")
        print("1. Go north")
        print("2. Go east")
        choice = input("> ")
        if choice == "1":
            print("You have chosen to go north.")
            return "1"
        elif choice == "2":
            print("You have chosen to go east.")
            return "2"
        else:
            print("Invalid choice. Please try again.")
            time.sleep(1)
            clear()
            return room_create(player)

    def stat_allocation_menu(player):
        print("\n--- Stat Allocation Menu ---")
        print(f"You have {player.stat_points} stat points to allocate.")
        print("1. Increase Damage (+2% per point)")
        print("2. Increase Health (+2% per point)")
        print("3. Increase Armor (+2% per point)")
        print("4. Increase Crit Chance (+2% per point)")
        print("5. Increase Crit Multiplier (+5% per point)")
        print("6. Exit Stat Allocation Menu")
        choice = input("> ")
        match choice:
            case "1":
                stat = "damage"
            case "2":
                stat = "health"
            case "3":
                stat = "armor"
            case "4":
                stat = "crit_chance"
            case "5":
                stat = "crit_multiplier"
            case "6":
                return
            case _:
                print("Invalid choice. Please try again.")
                time.sleep(1)
                clear()
                return stat_allocation_menu(player)
        print(f"How many points do you want to allocate to {stat}?")
        points = input("> ")
        if points.isdigit():
            points = int(points)
            player.stat_allocation(stat, points)
        else:
            print("Invalid input. Please enter a number.")
            time.sleep(1)
            clear()
            return stat_allocation_menu(player)
        
        input("Press Enter to continue...")
        clear()
        return

    while True:
        if debug_mode:
            print("[DEBUG] Player Stats:", vars(player))
        else:
            print("Your current stats are:")
            print(f"Level: {player.level}, Health: {round(player.current_health, 2)}/{player.max_health}, Damage: {player.base_damage}, Armor: {player.armor}, Crit Chance: {player.crit_chance}%, Crit Multiplier: {player.crit_multiplier}x")

        print("\n--- Main Menu ---")
        print("1. Continue with adventure")
        print("2. Allocate stat points")
        print("3. Rest (to full health)")
        print("4. Exit game")
        choice = input("> ")

        rm = None
        # Handle main menu choices
        if choice == "1":
            print("Continuing your adventure...")
            rm = room_create(player)
        elif choice == "2":
            stat_allocation_menu(player)
            clear()
            continue
        elif choice == "3":
            player.current_health = player.max_health
            print("You have rested and restored your health to full.")
            time.sleep(1)
            clear()
            continue
        elif choice == "4":
            print("Exiting the game. Goodbye!")
            time.sleep(1)
            exit()
        else:
            print("Invalid choice. Please try again.")
            time.sleep(1)
            clear()
            continue
        monster = monster_encounter(player)

        def door1(player):
            return combat(player, monster)

        def door2(player):
            return combat(player, monster)

        if rm == "1":
            result = door1(player)
        elif rm == "2":
            result = door2(player)

        # Handle combat results
        if result == "Player defeated":
            print("You have been defeated! Game over.")
            input("Press Enter to exit...")
            exit()
        elif result == "Monster defeated":
            # Monster defeated gain experience and level up if enough experience
            print(f"You have defeated the {monster.name}!")
            if debug_mode:
                # In debug mode, give more experience for testing
                exp_gain = 20 + (10 * player.level) * 10
            else:
                # Normal experience gain
                exp_gain = 20 + (10 * player.level)
            print(f"You gain {exp_gain} experience points.")
            player.added_experience(exp_gain)
            print(f"Level {player.level}, XP {player.experience}/{player.experience_to_next_level()}")
            input("Press Enter to continue...")
            clear()
            # Move to the next room
            player.room += 1
        elif result == "Debug_safemode":
            print("[DEBUG] Your player health reached 0 restarting the level!")
            input("Press Enter to continue...")
            player.current_health = player.max_health
            clear()

if __name__ == "__main__":
    start()