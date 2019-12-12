player_table = {}

SPEED = 2
GRAVITY = .2
JUMP_POWER = 6


def map_file(map_list, wall_list):
    player_table["map"] = map_list
    player_table["wall_list"] = wall_list


def initiate(player):
    player_table[player] = {
        "direction": "right",
        "attacking": False,
        "moving_x": False,
        "can_move_x": True,
        "can_move_y": True,
        "in_air": False,
        "crouching": False,
        "sliding": False,
        "jumping": False,
        "falling": False,
        "can_double_jump": True,
        "right_input": False,
        "left_input": False,
        "tile_location": [int(player.center_x // 40), int(player.center_y // 40)],
        # Player Stats
        "damage_multiplier": 1,
        "speed": 1,
        "damage": 0,
    }


def update_texture(player):
    pass

def update(player):
    collision(player)
    gravity(player)
    move(player)


def collision(player):
    if player.change_y - GRAVITY < 40:
        player.change_y -= GRAVITY
    next_x = player.center_x + player.change_x
    next_y = player.center_y + player.change_y
    collision_detection(player, [next_x, next_y], player_table["wall_list"])


def gravity(player):
    if player_table[player]["can_move_y"]:
        if player.change_y < 0:
            falling(player, True)
            jumping(player, False)
        elif player.change_y >= 0:
            falling(player, False)
        elif player.change_y > 0:
            jumping(player, True)
        player.center_y += player.change_y
    else:
        player.change_y = 0
        falling(player, False)


def move(player):
    if player_table[player]["right_input"] and not player_table[player]["left_input"]:
        player_table[player]["direction"] = "right"
        player.change_x = SPEED
    elif player_table[player]["left_input"] and not player_table[player]["right_input"]:
        player_table[player]["direction"] = "left"
        player.change_x = -SPEED
    else:
        player.change_x = 0

    if player_table[player]["can_move_x"]:
        player.center_x += player.change_x
        if player.change_x != 0:
            player_table[player]["moving_x"] = True
        else:
            player_table[player]["moving_x"] = False


def falling(player, boolean):
    if boolean:
        player_table[player]["falling"] = True
        player_table[player]["crouching"] = False
    else:
        player_table[player]["falling"] = False


def jumping(player, boolean):
    if boolean:
        player_table[player]["jumping"] = True
        player_table[player]["crouching"] = False
    else:
        player_table[player]["jumping"] = False


def right_input(player, action):
    if action:
        player_table[player]["right_input"] = True
    else:
        player_table[player]["right_input"] = False


def left_input(player, action):
    if action:
        player_table[player]["left_input"] = True
    else:
        player_table[player]["left_input"] = False


def jump(player):
    if not player_table[player]["in_air"]:
        player_table[player]["jumping"] = True
        player_table[player]["in_air"] = True
        player.change_y = JUMP_POWER
        player_table[player]["crouching"] = False
    elif player_table[player]["in_air"] and player_table[player]["can_double_jump"]:
        player_table[player]["jumping"] = True
        player_table[player]["in_air"] = True
        player_table[player]["can_double_jump"] = False
        player.change_y = JUMP_POWER


def crouch(player):
    if not player_table[player]["in_air"]:
        player_table[player]["crouching"] = True


def landed(player):
    player_table[player]["can_move_y"] = False
    player_table[player]["can_double_jump"] = True
    player_table[player]["in_air"] = False


def collision_detection(player, next_position, list_to_check):
    player_table[player]["can_move_x"] = True
    player_table[player]["can_move_y"] = True
    for object in list_to_check:
        if (player.width / 2) + (object.width / 2) > abs(next_position[0] - object.center_x) and \
                (player.height / 2) + (object.height / 2) > abs(player.center_y - object.center_y):
            player.change_x = 0
            player_table[player]["can_move_x"] = False
            if player.center_x > object.center_x:
                player.center_x = object.center_x + (object.width / 2) + (player.width / 2)
            else:
                player.center_x = object.center_x - (object.width / 2) - (player.width / 2)

        if (player.height / 2) + (object.height / 2) > abs(next_position[1] - object.center_y) and \
                (player.width / 2) + (object.width / 2) > abs(player.center_x - object.center_x):
            landed(player)
            player.change_y = 0
            if player.center_y > object.center_y:
                player.center_y = object.center_y + (object.height / 2) + (player.height / 2)
            else:
                player.center_y = object.center_y - (object.height / 2) - (player.height / 2)
