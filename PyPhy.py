import arcade
import AniPy

player_table = {}

SPEED = 3
GRAVITY = .4
JUMP_POWER = 10


class DoubleJumpMark(arcade.Sprite):
    def __init__(self, file, scaling, player):
        super().__init__(file, scaling)
        self.frame_time = 0
        self.frame_life = 16
        self.center_x = player.center_x
        self.center_y = player.center_y - (player.height / 3)

    def update(self):
        self.frame_time += 1
        if self.frame_time == self.frame_life:
            self.remove_from_sprite_lists()
            self.kill()


def map_file(map_list, wall_list, coin_list, pystone_list):
    player_table["map"] = map_list
    player_table["wall_list"] = wall_list
    player_table["coin_list"] = coin_list
    player_table["pystone_list"] = pystone_list


def initiate(player):
    player_table[player] = {
        "height": 104,
        "width": 32,
        "walking_animation_frame": 1,
        "walking_animation_buffer": 0,
        "crawling_animation_frame": 1,
        "crawling_animation_buffer": 0,
        "standing_animation_frame": 1,
        "standing_animation_buffer": 0,
        "direction": "right",
        "attacking": False,
        "moving_x": False,
        "can_move_x": True,
        "can_move_y": True,
        "in_air": False,
        "crouching": False,
        "down_key": False,
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


def update(player, game):
    data = player_table[player]
    if not data["height"] == 70:
        update_gravity(player)
        collision(player, player_table[player]["width"], player_table[player]["height"])
        coin_obj = coin_collision(player, player_table[player]["width"], player_table[player]["height"])
        coin_handler(coin_obj, game)
        pystone_obj = pystone_collision(player, player_table[player]["width"], player_table[player]["height"])
        gravity(player)
        move(player)
        update_animation(player)
        update_collison_box(player)

    elif can_uncrouch(player):
        if not player_table[player]["down_key"]:
            player_table[player]["crouching"] = False
        update_gravity(player)
        collision(player, player_table[player]["width"], player_table[player]["height"])
        coin_obj = coin_collision(player, player_table[player]["width"], player_table[player]["height"])
        coin_handler(coin_obj, game)
        pystone_obj = pystone_collision(player, player_table[player]["width"], player_table[player]["height"])
        gravity(player)
        move(player)
        update_animation(player)
        update_collison_box(player)

    else:
        update_gravity(player)
        player_table[player]["jumping"] = False
        player_table[player]["falling"] = False
        player_table[player]["crouching"] = True
        collision(player, player_table[player]["width"], player_table[player]["height"])
        coin_obj = coin_collision(player, player_table[player]["width"], player_table[player]["height"])
        coin_handler(coin_obj, game)
        pystone_obj = pystone_collision(player, player_table[player]["width"], player_table[player]["height"])
        update_animation(player)
        gravity(player)
        move(player)
    if pystone_obj:
        pystone_obj.remove_from_sprite_lists()
        game.holding_pystone = True
        game.win()


def update_collison_box(player):
    if player_table[player]["height"] != 70 and player_table[player]["crouching"]:
        player_table[player]["height"] = 70
        player.center_y -= 17
    elif player_table[player]["height"] == 70 and not player_table[player]["crouching"]:
        player_table[player]["height"] = 104
        player.center_y += 17


def update_animation(player):
    direction = player_table[player]["direction"]
    if player_table[player]["falling"]:
        animation_info = AniPy.retrieve_static_texture_info("falling", direction)
        player.texture = animation_info["texture"]
    elif player_table[player]["jumping"]:
        animation_info = AniPy.retrieve_static_texture_info("jumping", direction)
        player.texture = animation_info["texture"]
    elif player_table[player]["crouching"] and not player_table[player]["moving_x"]:
        animation_info = AniPy.retrieve_static_texture_info("crouching", direction)
        player.texture = animation_info["texture"]
    elif player_table[player]["crouching"] and player_table[player]["moving_x"]:
        if player_table[player]["crawling_animation_buffer"] == 0:
            player_table[player]["crawling_animation_buffer"] += 1
            player_table[player]["crawling_animation_frame"] += 1
            if player_table[player]["crawling_animation_frame"] == 5:
                player_table[player]["crawling_animation_frame"] = 1
            frame = player_table[player]["crawling_animation_frame"]
            string_frame = str(frame)
            animation_info = AniPy.retrieve_dynamic_animation_info("crawling", direction, string_frame)
            player.texture = animation_info["texture"]
        elif player_table[player]["crawling_animation_buffer"] == 10:
            player_table[player]["crawling_animation_buffer"] = 0
        else:
            player_table[player]["crawling_animation_buffer"] += 1

    elif player_table[player]["moving_x"] and not player_table[player]["in_air"] and not player_table[player]["crouching"]:
        if player_table[player]["walking_animation_buffer"] != 1:
            player_table[player]["walking_animation_buffer"] += 1
            player_table[player]["walking_animation_frame"] += 1
            if player_table[player]["walking_animation_frame"] == 19:
                player_table[player]["walking_animation_frame"] = 1
            frame = player_table[player]["walking_animation_frame"]
            string_frame = str(frame)
            animation_info = AniPy.retrieve_dynamic_animation_info("walking", direction, string_frame)
            player.texture = animation_info["texture"]
        else:
            player_table[player]["walking_animation_buffer"] = 0

    else:
        if player_table[player]["standing_animation_buffer"] == 0:
            player_table[player]["standing_animation_buffer"] += 1
            player_table[player]["standing_animation_frame"] += 1
            if player_table[player]["standing_animation_frame"] == 5:
                player_table[player]["standing_animation_frame"] = 1
            frame = player_table[player]["standing_animation_frame"]
            string_frame = str(frame)
            animation_info = AniPy.retrieve_dynamic_animation_info("standing", direction, string_frame)
            player.texture = animation_info["texture"]
        elif player_table[player]["standing_animation_buffer"] == 10:
            player_table[player]["standing_animation_buffer"] = 0
        else:
            player_table[player]["standing_animation_buffer"] += 1


def collision(player, width, height):
    next_x = player.center_x + player.change_x
    next_y = player.center_y + player.change_y
    collision_detection(player, [next_x, next_y], width, height, player_table["wall_list"])


def coin_collision(player, width, height):
    next_x = player.center_x + player.change_x
    next_y = player.center_y + player.change_y
    return coin_collision_detection(player, [next_x, next_y], width, height, player_table["coin_list"])


def pystone_collision(player, width, height):
    next_x = player.center_x + player.change_x
    next_y = player.center_y + player.change_y
    return coin_collision_detection(player, [next_x, next_y], width, height, player_table["pystone_list"])


def update_gravity(player):
    if player.change_y - GRAVITY < 40:
        player.change_y -= GRAVITY


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
        if player_table[player]["crouching"]:
            player.change_x = SPEED * (2 / 3)
        else:
            player.change_x = SPEED

    elif player_table[player]["left_input"] and not player_table[player]["right_input"]:
        player_table[player]["direction"] = "left"
        if player_table[player]["crouching"]:
            player.change_x = -SPEED * (2 / 3)
        else:
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


def jump(player, asset_list):
    if not player_table[player]["in_air"] and not player_table[player]["falling"]:
        player_table[player]["jumping"] = True
        player_table[player]["in_air"] = True
        if player_table[player]["crouching"]:
            player.change_y = JUMP_POWER * 1.2
        else:
            player.change_y = JUMP_POWER
        player_table[player]["crouching"] = False
    elif player_table[player]["in_air"] and player_table[player]["can_double_jump"]:
        player_table[player]["jumping"] = True
        player_table[player]["in_air"] = True
        player_table[player]["can_double_jump"] = False
        player.change_y = JUMP_POWER
        double_jump_mark = DoubleJumpMark("double_jump_mark.png", 1, player)
        asset_list.append(double_jump_mark)


def crouch(player, boolean):
    if boolean:
        player_table[player]["down_key"] = True
    else:
        player_table[player]["down_key"] = False

    if not player_table[player]["in_air"] and boolean:
        player_table[player]["crouching"] = True

    elif not boolean:
        player_table[player]["crouching"] = False


def can_uncrouch(player):
    collision_bool = animation_change_collision_detection(player, player.center_y + 17, 32, 104, player_table["wall_list"])
    if collision_bool:
        return True
    else:
        return False


def landed(player):
    player_table[player]["can_move_y"] = False
    player_table[player]["can_double_jump"] = True
    player_table[player]["in_air"] = False


def collision_detection(player, next_position, width, height, list_to_check):
    player_table[player]["can_move_x"] = True
    player_table[player]["can_move_y"] = True
    for object in list_to_check:
        if (width / 2) + (object.width / 2) > abs(next_position[0] - object.center_x) and \
                (height / 2) + (object.height / 2) > abs(player.center_y - object.center_y):
            player.change_x = 0
            player_table[player]["can_move_x"] = False
            if player.center_x > object.center_x:
                player.center_x = object.center_x + (object.width / 2) + (width / 2)
            else:
                player.center_x = object.center_x - (object.width / 2) - (width / 2)

        if (height / 2) + (object.height / 2) > abs(next_position[1] - object.center_y) and \
                (width / 2) + (object.width / 2) > abs(player.center_x - object.center_x):
            player.change_y = 0
            if player.center_y > object.center_y:
                player.center_y = object.center_y + (object.height / 2) + (height / 2)
                landed(player)
            else:
                player.center_y = object.center_y - (object.height / 2) - (height / 2)
        if player.change_y != 0:
            player_table[player]["in_air"] = True


def coin_collision_detection(player, next_position, width, height, list_to_check):
    for object in list_to_check:
        if (width / 2) + (object.width / 2) > abs(next_position[0] - object.center_x) and \
                (height / 2) + (object.height / 2) > abs(player.center_y - object.center_y) and \
                (height / 2) + (object.height / 2) > abs(next_position[1] - object.center_y) and \
                (width / 2) + (object.width / 2) > abs(player.center_x - object.center_x):
            return object
    return False


def coin_handler(obj, game):
    if obj:
        obj.remove_from_sprite_lists()
        game.current_level_points += 100


def animation_change_collision_detection(player, center_y, width, height, list_to_check):
    for object in list_to_check:
        if (height / 2) + (object.height / 2) > abs(center_y - object.center_y) and \
                (width / 2) + (object.width / 2) > abs(player.center_x - object.center_x):
            return False

    return True
