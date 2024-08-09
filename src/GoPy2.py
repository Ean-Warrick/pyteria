import arcade


def clicked_button(game, button):
    if button == "new_game":
        if game.data:
            game.new_game_menu()
        else:
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
            game.data = True
            game.level_select()
    elif button == "yes":
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
        game.data = True
        game.level_select()
    elif button == "no":
        game.start_menu()
    elif button == "continue":
        game.level_select()
    elif button == "level_1":
        game.play(1)
    elif button == "level_2":
        if game.levels["level_2_unlocked"]:
            game.play(2)
    elif button == "level_3":
        if game.levels["level_3_unlocked"]:
            game.play(3)
    elif button == "return_to_level_select":
        game.level_select()
    elif button == "return_to_start_screen":
        game.start_menu()
    elif button == "return_to_game":
        game.playing = True
    elif button == "quit_level":
        game.want_to_quit()
    elif button == "yes_quit":
        game.quit()
    elif button == "no_quit":
        game.pause_game()


