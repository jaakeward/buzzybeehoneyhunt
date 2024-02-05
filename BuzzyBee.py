#Display game instructions to player
def game_instructions():
    print("BUZZY BEE - HONEY HUNT\n"
        "Welcome to the Buzzy Bee Honey Hunt!\n"
        "Your queen bee has requested a special batch of honey,\n"
        "so each bee must collect nectar from 6 different flowers.\n"
        "Each flower can be found in a different greenhouse at the local farm.\n"
        "Bee careful – if you encounter a carnivorous plant, they’ll eat you!\n\n"
        "As you fly through each greenhouse, you will have the option to move to a new greenhouse,\n"
        "collect the nectar from the greenhouse you are in, or exit the game.\n"
        "Begining gameplay... Good luck!")

#Function list_stats will print players current room and present command options
def list_stats(room, inventory, item, avail_moves):
    print("\nYou are in the {}".format(room))
    print("Inventory: ", inventory)
    if item != None:
        print("This greenhouse contains nectar from a {}".format(item))
    print("You may choose from the following options: {}".format(avail_moves))

#Define rooms, inventory, start room
#Returns rooms dictionary, empty inventory list, start room, and boolean to begin gameplay loop
def initialize_gameplay():
    # The dictionary 'rooms' links each greenhouse to others near it.
    # 'Rooms' also contains the contents (nectars or villains) of each room
    rooms = {
        "Greenhouse 1": {"EAST": "Greenhouse 2", "SOUTH": "Greenhouse 7", "item": None},
        "Greenhouse 2": {"WEST": "Greenhouse 1", "EAST": "Greenhouse 3", "SOUTH": "Carnivorous Greenhouse",
                         "item": "Rose"},
        "Greenhouse 3": {"WEST": "Greenhouse 2", "SOUTH": "Greenhouse 4", "item": "Lotus"},
        "Greenhouse 4": {"WEST": "Carnivorous Greenhouse", "SOUTH": "Greenhouse 5", "NORTH": "Greenhouse 3",
                         "item": "Hibiscus"},
        "Greenhouse 5": {"WEST": "Greenhouse 6", "NORTH": "Greenhouse 4", "item": "Gardenia"},
        "Greenhouse 6": {"WEST": "Greenhouse 7", "EAST": "Greenhouse 5", "NORTH": "Carnivorous Greenhouse",
                         "item": "Sunflower"},
        "Greenhouse 7": {"EAST": "Greenhouse 6", "NORTH": "Greenhouse 1", "item": "Iris"},
        "Carnivorous Greenhouse": {"item": "Venus Fly Trap"}
    }
    #Empty player inventory
    inventory = []

    # Set variables needed to begin game loop and first room
    play = True
    current_room = 'Greenhouse 1'

    return rooms, inventory, play, current_room

#move player between rooms and validate input
def move_player_position(move, current_pos, rooms):
    temp = current_pos
    for i in rooms[current_pos]:
        if i == move:
            current_pos = rooms[current_pos][move]
    if temp == current_pos:
        print("Cannot go {}, please enter new command.".format(move.lower()))
    return current_pos

#Add item to inventory and remove from current room
def gather_item(rooms, current_room, inventory):
    if rooms[current_room]["item"] == None:
        print("Invalid command --- Please try again")
    else:
        inventory.append(rooms[current_room]["item"])
        rooms[current_room]["item"] = None
    return inventory

#Check if player has won
def check_win(inventory):
    if len(inventory) > 5:
        print("WINNER!")
        print("You have collected all the nectar for the queens's honey!")
        print("Inventory: ", inventory)
        print("You may now return to the hive for a feast (Exit), or play again (Play)")
        return True
    else:
        return False

def player_lost():
    print("***SNAP!***\n"
        "Oh no! You've entered the Carnivorous Greenhouse!\n"
        "You've been trapped in the jaws of a Venus Fly Trap\n"
        "GAME OVER... Would you like to play again? (Play or Exit)")
    return play_more()

def play_more():
    play_again = input().upper()
    validation_check = True
    while validation_check:
        if play_again == 'PLAY':
            play_again = True
            validation_check = False
        elif play_again == 'EXIT':
            play_again = False
            validation_check = False
        else:
            print("Invalid command --- Please try again")
            play_again = input().upper()
    return play_again


def main():
    game_instructions()
    rooms, inventory, play, current_room = initialize_gameplay()

    # Gameplay loop
    while play:
        #Display stats and gather user's input
        avail_moves = list(rooms[current_room].keys())
        for i in avail_moves:
            if i == 'item':
                avail_moves[avail_moves.index('item')] = "Get Nectar"
            elif rooms[current_room]['item'] == None and 'item' in avail_moves:
                avail_moves.remove('item')


        list_stats(current_room, inventory, rooms[current_room]["item"], avail_moves)
        user_option = input().upper()

        #Decision branch to check/execute/validate user input (in order):
        #Exit, Move, Get item and check if user won and wants to play again,
        #Input validation, Check if user lost and wants to play again
        if user_option == 'EXIT':
            play = False

        elif user_option == 'NORTH' or user_option == 'SOUTH' or user_option == 'EAST' or user_option == 'WEST':
            current_room = move_player_position(user_option, current_room, rooms)

        elif user_option == 'GET NECTAR':
            inventory = gather_item(rooms, current_room, inventory)
            if check_win(inventory):
                rooms, inventory, play, current_room = initialize_gameplay()
                play = play_more()
        else:
            print("Invalid command --- Please try again")

        if current_room == "Carnivorous Greenhouse":
            rooms, inventory, play, current_room = initialize_gameplay()
            play = player_lost()

main()