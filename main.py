from classes.game import Person,bcolors
from classes.magic import Spell
from classes.inventory import Item
import random

# for better User Interface
print("\n \n")
print("NAME                  HP                                        MP")

print("\n\n")

# Create Black Magic
fire = Spell("Fire", 25, 600, "Black")
thunder = Spell("thunder", 25, 600, "Black")
blizzard = Spell("blizzard", 25, 600, "Black")
meteor = Spell("meteor", 40, 1200, "Black")
quake = Spell("quake", 14, 140, "Black")

# Create White Magic
cure = Spell("Cure", 25, 620,"white")
cura = Spell("Cura", 30, 1500,"white")

# Create some items
potion = Item("Potion", "potion", "Heals 50 HP", 50)
hipotion = Item("Hi-Potion", "potion", "Heals 100 HP", 100)
superpotion = Item("Super Potion", "potion", "Heals 1000 HP", 1000)
elixer = Item("Elixer", "elixer", "Fully restores HP/MP of one party member", 9999)
highelixer = Item("MegaElixer", "elixer", "Fully restores party's HP/MP", 9999)
grenade = Item("Grenade", "attack", "Deals 500 damage", 500)

player_spells = [fire, thunder, blizzard, meteor, quake, cure, cura]
player_items = [{"item": potion, "quantity": 15},
                {"item": hipotion, "quantity": 5},
                {"item": superpotion, "quantity": 5},
                {"item": elixer, "quantity": 5},
                {"item": highelixer, "quantity": 2},
                {"item": grenade, "quantity": 5}]

# instantiate people
player1 = Person(" Mark : ", 3260, 132, 300, 34, player_spells, player_items)
player2 = Person(" Luke : ", 4160, 188, 311, 34, player_spells, player_items)
player3 = Person(" john : ", 3089, 174, 288, 34, player_spells, player_items)

# instantiate enemies
enemy1 = Person("Lucifer :", 11200, 700, 525, 25, [], [])
enemy2 = Person("Judas :  ", 1250, 130, 560, 25, [], [])
enemy3 = Person("Devil :  ", 1250, 130, 560, 25, [], [])

players = [player1, player2, player3]
enemies =[enemy1, enemy2,enemy3]

running = True
i = 0

print(bcolors.FAIL + bcolors.BOLD + " An Enemy attacks " +bcolors.ENDC)

while running:
    print("=======================")
    print("\n\n")
    print(bcolors.BOLD+"  NAME                      HP                                    MP")
    for player in players:
        player.get_stats()

    for enemy in enemies:
        enemy.get_enemy_stats()

    for player in players:
        print("\n")
        player.choose_action()
        choice = input("    Choose action : ")
        index = int(choice) - 1

        # if user selects attack
        if index == 0:
            dmg = player.generate_damage()
            enemy = player.choose_target(enemies)
            enemies[enemy].take_damage(dmg)
            print("You attacked " + enemies[enemy].name.replace(" ", "") + "for", dmg, "points of damage, ")

            if enemies[enemy].get_hp() == 0:
                print(enemies[enemy].name.replace(" ", "") + " has died ")
                del enemies[enemy]

        # if user selects magic
        elif index == 1:
            player.choose_magic()
            magic_choice=int(input("    Choose magic :")) - 1

            # to go back to the menu
            if magic_choice == -1:
                continue

            spell = player.magic[magic_choice]
            magic_dmg = spell.generate_damage()

            current_mp = player.get_mp()

            if spell.cost > current_mp:
                print(bcolors.FAIL + " \n NOT ENOUGH MP " + bcolors.ENDC)
                continue

            player.reduce_mp(spell.cost)

            if spell.type == "white":
                player.heal(magic_dmg)
                print(bcolors.OKBLUE + "\n" + spell.name + " heals for ", str(magic_dmg), " HP, "+bcolors.ENDC)

            elif spell.type == "black":
                enemy = player.choose_target(enemies)
                enemies[enemy].take_damage(magic_dmg)
                print(bcolors.OKBLUE + " \n " + spell.name +
                      " deals", str(magic_dmg), " points of damage to " + enemies[enemy].name.replace(" ", "") + bcolors.ENDC)

                if enemies[enemy].get_hp() == 0:
                    print(enemies[enemy].name.replace(" ", "") + " has died ")
                    del enemies[enemy]

        # if user selects item
        elif index == 2:
            player.choose_item()
            # to select the from the given list of items from inventory
            item_choice = int(input("    Choose item : ")) - 1

            # to go back to the menu
            if item_choice == -1:
                continue

            item = player.items[item_choice]["item"]

            if player.items[item_choice]["quantity"] == 0:
                print(bcolors.FAIL + "\n" + "None Left..." + bcolors.ENDC)
                continue

            # to reduce the item after user uses it
            player.items[item_choice]["quantity"] -= 1

            if item.type == "potion":
                player.heal(item.prop)
                print(bcolors.OKGREEN + "\n" + item.name + " Heals for ", str(item.prop), " HP " + bcolors.ENDC)

            elif item.type == "elixer":

                if item.name == "MegaElixer":
                    for i in players:
                        i.hp = i.maxhp
                        i.mp = i.maxmp

                else:
                    player.hp = player.maxhp
                    player.mp = player.maxmp

                print(bcolors.OKGREEN + "\n" + item.name + " fully restores HP/MP" + bcolors.ENDC)

            elif item.type == "attack":
                enemy = player.choose_target(enemies)
                enemies[enemy].take_damage(item.prop)
                print(bcolors.FAIL + "\n" + item.name +
                      " deals", str(item.prop), " points of damage to " + enemies[enemy].name + bcolors.ENDC)

                if enemies[enemy].get_hp() == 0:
                    print(enemies[enemy].name.replace(" ", "") + " has died ")
                    del enemies[enemy]

    # to randomly attack the player
    enemy_choice = 1
    target = random.randrange(0, 3)
    enemy_dmg = enemies[0].generate_damage()

    players[target].take_damage(enemy_dmg)
    print("Enemy attacks for ", enemy_dmg)

    # to print the message whether lost or won
    defeated_enemies = 0
    defeated_players = 0

    for enemy in enemies:
        if enemy.get_hp() == 0:
            defeated_enemies += 1

    for player in players:
        if player.get_hp() == 0:
            defeated_players += 1

    if defeated_enemies == 2:
        print(bcolors.OKGREEN + " CONGRATULATIONS BUDDY :) YOU WIN " + bcolors.ENDC)
        running = False

    elif defeated_players == 2:
        print(bcolors.FAIL + " YOU LOST . YOU HAVE BEEN DEFEATED BY THE ENEMIES " + bcolors.ENDC)
        running = False




