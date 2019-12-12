import arcade


def click_mouse(x, y, button_list, game):
    size_x, size_y = get_game_size(game)
    print(x, y)
    if game.menu_window == "start_menu":
        if (1920 / 2) - 250 < x < (1920 / 2) + 250 and 500 - 80 < y < 500 + 80:
            new_save_table = {
                "level_2": False,
                "level_3": False,
                "total_points": 0,
                "level_points": {
                    "level_1": 0,
                    "level_2": 0,
                    "level_3": 0
                }
            }

            game.load_data(new_save_table)
            game.level_select()
            game.data = True
        elif (1920 / 2) - 250 < x < (1920 / 2) + 250 and 300 - 80 < y < 300 + 80 and game.data:
            game.level_select()
    elif game.menu_window == "level_select":
        if (1920 / 2) - 175 < x < (1920 / 2) - 75 and (1080 / 2) - 50 < y < (1080 / 2) + 50:
            game.play(1)
        elif (1920 / 2) - 50 < x < (1920 / 2) + 50 and (1080 / 2) - 50 < y < (1080 / 2) + 50:
            if game.levels["level_2_unlocked"]:
                game.play(2)
        elif (1920 / 2) + 75 < x < (1920 / 2) + 175 and (1080 / 2) - 50 < y < (1080 / 2) + 50:
            if game.levels["level_3_unlocked"]:
                game.play(3)


def create_start_menu(game):
    start_menu_list = arcade.SpriteList()

    background = arcade.Sprite("pyteria_menu_imgs/background.png", 1)
    background.center_x = 1920 / 2
    background.center_y = 1080 / 2
    start_menu_list.append(background)

    pyteria = arcade.Sprite("pyteria_menu_imgs/pyteria.png", 1)
    pyteria.center_x = 1920 / 2
    pyteria.center_y = 800
    start_menu_list.append(pyteria)

    new_game = arcade.Sprite("pyteria_menu_imgs/new_game.png", 1)
    new_game.center_x = 1920 / 2
    new_game.center_y = 500
    start_menu_list.append(new_game)

    if game.data:
        continue_game = arcade.Sprite("pyteria_menu_imgs/continue.png", 1)
        continue_game.center_x = 1920 / 2
        continue_game.center_y = 300
        start_menu_list.append(continue_game)
    else:
        continue_game = arcade.Sprite("pyteria_menu_imgs/disabled_continue.png", 1)
        continue_game.center_x = 1920 / 2
        continue_game.center_y = 300
        start_menu_list.append(continue_game)

    child_list = [new_game, continue_game]

    return start_menu_list, child_list


def create_level_select(game):
    start_menu_list = arcade.SpriteList()

    background = arcade.Sprite("pyteria_menu_imgs/background.png", 1)
    background.center_x = 1920 / 2
    background.center_y = 1080 / 2
    start_menu_list.append(background)

    level_select_menu = arcade.Sprite("pyteria_menu_imgs/level_select_menu.png", 1)
    level_select_menu.center_x = 1920 / 2
    level_select_menu.center_y = 1080 / 2
    start_menu_list.append(level_select_menu)

    for i in range(3):
        if game.levels[f"level_{i + 1}_unlocked"]:
            level_select_menu = arcade.Sprite(f"pyteria_menu_imgs/level_{i + 1}.png", 1)
            level_select_menu.center_x = 1920 / 2 + (-125 + (125 * i))
            level_select_menu.center_y = (1080 / 2)
            start_menu_list.append(level_select_menu)
        else:
            x, y = get_game_size(game)
            print(f"level {i + 1} is not unlocked")
            level_select_menu = arcade.Sprite(f"pyteria_menu_imgs/level_{i + 1}_not_unlocked.png", 1)
            level_select_menu.center_x = 1920 / 2 + (-125 + (125 * i))
            level_select_menu.center_y = (1080 / 2)
            start_menu_list.append(level_select_menu)


    return start_menu_list


def game_pause(x, y, game):
    size = game.get_size()
    size_x = size[0]
    size_y = size[1]
    pause_button_x = 60
    pause_button_y = size_y - 60
    if pause_button_x - 50 < x < pause_button_x + 50 and pause_button_y - 50 < y < pause_button_y + 50:
        if game.paused:
            game.paused = False
        else:
            game.paused = True


def get_game_size(game):
    size = game.get_size()
    return size[0], size[1]

