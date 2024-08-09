import arcade
import GoPy2
import PyMap
import PyPhy
import Pydle
from pyglet.image import load as pyglet_load

PLAY_SOUND = True
CLOUDS = True
MENU_SONG = arcade.load_sound("src/sound/menu_screen_piano.mp3")


class Crate(arcade.Sprite):
    def __init__(self, file, scaling):
        super().__init__(file, scaling)


blocks = {
    1: ["src/blocks/dirt_tile.png", "wall"],
    2: ["src/blocks/dirt_grass_top_tile.png", "wall"],
    3: ["src/blocks/stone_tile.png", "wall"],
    4: ["src/blocks/ww_to_doublejump.png", "asset"],
    5: ["src/blocks/w_to_jump.png", "asset"],
    6: ["src/blocks/coins_is_points.png", "asset"],
    7: ["src/blocks/wasd.png", "asset"],
    8: ["src/blocks/flag.png", "pystone"],
    9: ["src/blocks/coin.png", "coin"],
    10: ["src/blocks/s_to_crouch.png", "asset"],
    11: ["src/blocks/complete_level.png", "asset"],
}


def play_menu_music():
    if PLAY_SOUND:
        MENU_SONG.play()


def load_walls(map, wall_list, coin_list, pystone_list, asset_list, game):
    for row_number, row_list in enumerate(map):
        for column_number, object_block in enumerate(row_list):
            crate_info = blocks.get(object_block, None)
            if object_block == 666:
                game.kill_y = 20 + 40 * row_number
            elif crate_info is not None:
                crate = Crate(crate_info[0], 1)

                crate.center_x = 20 + 40 * column_number
                crate.center_y = 20 + 40 * row_number
                type = crate_info[1]
                if type == "wall":
                    wall_list.append(crate)
                elif type == "asset":
                    asset_list.append(crate)
                elif type == "pystone":
                    pystone_list.append(crate)
                elif type == "coin":
                    coin_list.append(crate)



class Player(arcade.Sprite):
    def __init__(self, file, scaling, game):
        super().__init__(file, scaling)
        self.center_y = 800
        self.center_x = 400

        self.game = game

    def update(self):
        PyPhy.update(self, self.game)


def draw_points(points, game, player, y_offset):
    size = game.get_size()
    size_x = size[0]
    size_y = size[1]
    arcade.draw_text(points, player.center_x - (size_x / 2) + 10, game.bottom_y + 10 + y_offset, (255, 255, 255), 40)


class Button(arcade.Sprite):
    def __init__(self, file, scaling, x, y, button):
        super().__init__(file, scaling)
        self.button = button
        self.center_x = x
        self.center_y = y

    def clicked(self, game):
        GoPy2.clicked_button(game, self.button)


class Graphic(arcade.Sprite):
    def __init__(self, file, scaling, x, y):
        super().__init__(file, scaling)
        self.center_x = x
        self.center_y = y


class Game(arcade.Window):
    def __init__(self, width, height, title):
        super().__init__(width, height, title, resizable=True)
        self.set_icon(pyglet_load("src/image/pyteriaicon.png"))
        size = self.get_size()
        self.set_viewport(0, size[0], 0, size[1])
        self.left = 0
        self.bottom_y = 0
        self.button_list = arcade.SpriteList()
        self.data = False
        self.sky = Graphic("src/image/sky.png", 1, 1920 / 2, 1080 / 2)
        self.kill_y = None
        # data
        self.levels = None
        self.total_points = None
        self.level_points = None
        save_data, self.data = Pydle.load_file()
        self.load_data(save_data)
        self.pause_button = Button("src/pyteria_menu_imgs/settings_icon.png", 1, 1920 / 2, 1017 / 2 - 250, "pause")

        self.current_level_points = 0

        arcade.set_background_color((100, 200, 255))
        self.clouds = Graphic("src/blocks/clouds.png", 1, 1920 / 2, 1080 / 2)
        self.clouds2 = Graphic("src/blocks/clouds.png", 1, 1920 / 2 + 1920, 1080 / 2)
        self.clouds_x = 0
        self.map = None
        self.level = None
        self.holding_pystone = False
        self.wall_list = arcade.SpriteList()
        self.player_list = arcade.SpriteList()
        self.player = None
        self.asset_list = arcade.SpriteList()
        self.coins_list = arcade.SpriteList()
        self.pystone_list = arcade.SpriteList()
        self.settings_icon = arcade.Sprite("src/pyteria_menu_imgs/settings_icon.png", 1)
        self.settings_icon.center_x = 60
        self.settings_icon.center_y = 950
        # pause_menu
        self.pause_menu = arcade.SpriteList()
        self.pause_screen = arcade.Sprite("src/pyteria_menu_imgs/pause_menu.png", 1)
        self.pause_menu.append(self.pause_screen)
        self.quit_level = arcade.Sprite("src/pyteria_menu_imgs/quit_level.png", 1)
        self.pause_menu.append(self.quit_level)

        # menu stuff
        self.playing = False
        self.paused = False
        self.start_menu_list = None
        play_menu_music()

    def load_data(self, data):
        self.levels = {
            "level_1_unlocked": True,
            "level_2_unlocked": data["level_2"],
            "level_3_unlocked": data["level_3"]
        }
        self.total_points = data["total_points"]
        self.level_points = {
            "level_1_points": data["level_points"]["level_1"],
            "level_2_points": data["level_points"]["level_2"],
            "level_3_points": data["level_points"]["level_3"]
        }

    def on_close(self):
        save_table = {
            "level_2": self.levels["level_2_unlocked"],
            "level_3": self.levels["level_3_unlocked"],
            "total_points": self.total_points,
            "level_points": {
                "level_1": self.level_points["level_1_points"],
                "level_2": self.level_points["level_2_points"],
                "level_3": self.level_points["level_3_points"]
            }
        }
        Pydle.save_data(save_table)
        self.close()

    def on_mouse_press(self, x: float, y: float, button: int, modifiers: int):
        viewport = self.get_viewport()
        if not self.playing:
            for button in self.button_list:
                if button.center_x - (button.width / 2) < x < button.center_x + (button.width / 2) and \
                        button.center_y - (button.height / 2) < y < button.center_y + (button.height / 2):
                    button.clicked(self)
        else:
            if 10 < x < 110 and 907 < y < 1007:
                self.pause_game()

    def start_menu(self):
        self.playing = False
        arcade.set_viewport(0, 1920, 0, 1017)
        self.start_menu_list = arcade.SpriteList()
        self.button_list = arcade.SpriteList()
        background = Graphic("src/pyteria_menu_imgs/background.png", 1, 1920 / 2, 1017 / 2)
        self.start_menu_list.append(background)
        pyteria = Graphic("src/pyteria_menu_imgs/pyteria.png", 1, 1920 / 2, 1017 / 2 + 300)
        self.start_menu_list.append(pyteria)
        new_game = Button("src/pyteria_menu_imgs/new_game.png", 1, 1920 / 2, 1017 / 2, "new_game")
        self.start_menu_list.append(new_game)
        self.button_list.append(new_game)
        if self.data:
            continue_button = Button("src/pyteria_menu_imgs/continue.png", 1, 1920 / 2, 1017 / 2 - 200, "continue")
        else:
            continue_button = Button("src/pyteria_menu_imgs/disabled_continue.png", 1, 1920 / 2, 1017 / 2 - 200, "continue")
        self.start_menu_list.append(continue_button)
        self.button_list.append(continue_button)

    def new_game_menu(self):
        self.playing = False
        arcade.set_viewport(0, 1920, 0, 1017)
        self.start_menu_list = arcade.SpriteList()
        self.button_list = arcade.SpriteList()
        background = Graphic("src/pyteria_menu_imgs/background.png", 1, 1920 / 2, 1017 / 2)
        self.start_menu_list.append(background)
        are_you_sure = Graphic("src/pyteria_menu_imgs/new_game_menu.png", 1, 1920 / 2, 1017 / 2)
        self.start_menu_list.append(are_you_sure)
        no = Button("src/pyteria_menu_imgs/no.png", 1, 1920 / 2 - 250, 1017 / 2 - 250, "no")
        self.start_menu_list.append(no)
        self.button_list.append(no)
        yes = Button("src/pyteria_menu_imgs/yes.png", 1, 1920 / 2 + 250, 1017 / 2 - 250, "yes")
        self.start_menu_list.append(yes)
        self.button_list.append(yes)

    def pause_game(self):
        self.playing = False
        arcade.set_viewport(0, 1920, 0, 1017)
        self.start_menu_list = arcade.SpriteList()
        self.button_list = arcade.SpriteList()
        background = Graphic("src/pyteria_menu_imgs/background.png", 1, 1920 / 2, 1017 / 2)
        self.start_menu_list.append(background)
        pause_menu = Graphic("src/pyteria_menu_imgs/pause_menu.png", 1, 1920 / 2, 1017 / 2)
        self.start_menu_list.append(pause_menu)
        quit_level = Button("src/pyteria_menu_imgs/quit_level.png", 1, 1920 / 2, 1017 / 2 + 100, "quit_level")
        self.start_menu_list.append(quit_level)
        self.button_list.append(quit_level)
        return_to_game = Button("src/pyteria_menu_imgs/return_to_game.png", .5, 1920 / 2, 1017 / 2 - 50, "return_to_game")
        self.start_menu_list.append(return_to_game)
        self.button_list.append(return_to_game)

    def want_to_quit(self):
        self.playing = False
        arcade.set_viewport(0, 1920, 0, 1017)
        self.start_menu_list = arcade.SpriteList()
        self.button_list = arcade.SpriteList()
        background = Graphic("src/pyteria_menu_imgs/background.png", 1, 1920 / 2, 1017 / 2)
        self.start_menu_list.append(background)
        pause_menu = Graphic("src/pyteria_menu_imgs/are_you_sure_to_quit.png", 1, 1920 / 2, 1017 / 2)
        self.start_menu_list.append(pause_menu)
        yes_quit = Button("src/pyteria_menu_imgs/yes.png", 1, 1920 / 2 + 250, 1017 / 2 - 250, "yes_quit")
        self.start_menu_list.append(yes_quit)
        self.button_list.append(yes_quit)
        no_quit = Button("src/pyteria_menu_imgs/no.png", 1, 1920 / 2 - 250, 1017 / 2 - 250, "no_quit")
        self.start_menu_list.append(no_quit)
        self.button_list.append(no_quit)

    def quit(self):
        self.current_level_points = 0
        self.asset_list = arcade.SpriteList()
        self.wall_list = arcade.SpriteList()
        self.start_menu_list = arcade.SpriteList()
        self.button_list = arcade.SpriteList()
        self.pystone_list = arcade.SpriteList()
        self.level_select()

    def level_select(self):
        self.playing = False
        self.asset_list = arcade.SpriteList()
        arcade.set_viewport(0, 1920, 0, 1017)
        self.pystone_list = arcade.SpriteList()
        self.start_menu_list = arcade.SpriteList()
        self.button_list = arcade.SpriteList()
        background = Graphic("src/pyteria_menu_imgs/background.png", 1, 1920 / 2, 1017 / 2)
        self.start_menu_list.append(background)
        level_select_menu = Graphic("src/pyteria_menu_imgs/level_select_menu.png", 1, 1920 / 2, 1017 / 2)
        self.start_menu_list.append(level_select_menu)
        level_1 = Button("src/pyteria_menu_imgs/level_1.png", 1, 1920 / 2 - 60, 1017 / 2 + 50, "level_1")
        self.start_menu_list.append(level_1)
        self.button_list.append(level_1)
        if self.levels["level_2_unlocked"]:
            level_2 = Button("src/pyteria_menu_imgs/level_2.png", 1, 1920 / 2 + 60, 1017 / 2 + 50, "level_2")
        else:
            level_2 = Button("src/pyteria_menu_imgs/level_2_not_unlocked.png", 1, 1920 / 2 + 60, 1017 / 2 + 50, "level_2")
        self.start_menu_list.append(level_2)
        self.button_list.append(level_2)

        return_to_start_screen = Button("src/pyteria_menu_imgs/return_to_start_screen.png", .5, 1920 / 2, 1017 / 2 - 200,
                                        "return_to_start_screen")
        self.start_menu_list.append(return_to_start_screen)
        self.button_list.append(return_to_start_screen)

    def play(self, level):
        self.asset_list = arcade.SpriteList()
        self.level = level
        self.button_list = arcade.SpriteList()
        #pause_button
        self.button_list.append(self.pause_button)
        # clear_lists
        self.player_list = arcade.SpriteList()
        self.holding_pystone = False
        # Loading Level / Map
        self.map = PyMap.load_map(level)
        self.wall_list = arcade.SpriteList()
        self.coins_list = arcade.SpriteList()
        load_walls(self.map, self.wall_list, self.coins_list, self.pystone_list, self.asset_list, self)
        PyPhy.map_file(self.map, self.wall_list, self.coins_list, self.pystone_list)
        # Creating Player (Important to do this after loading map)
        self.player = Player("src/image/player_front.png", 1, self)
        self.player_list.append(self.player)
        PyPhy.initiate(self.player)
        self.playing = True

    def win(self):
        if self.current_level_points > self.level_points[f"level_{self.level}_points"]:
            self.total_points = self.total_points - self.level_points[
                f"level_{self.level}_points"] + self.current_level_points
            self.level_points[f"level_{self.level}_points"] = self.current_level_points
        self.current_level_points = 0
        if self.level < 3:
            self.levels[f"level_{self.level + 1}_unlocked"] = True
        self.playing = False
        arcade.set_viewport(0, 1920, 0, 1017)
        self.start_menu_list = arcade.SpriteList()
        self.button_list = arcade.SpriteList()
        background = Graphic("src/pyteria_menu_imgs/background.png", 1, 1920 / 2, 1017 / 2)
        self.start_menu_list.append(background)
        you_won = Graphic("src/pyteria_menu_imgs/you_won.png", 1, 1920 / 2, 1017 / 2)
        self.start_menu_list.append(you_won)
        return_to_level_select = Button("src/pyteria_menu_imgs/return_to_level_select.png", .5, 1920 / 2, 1017 / 2,
                                        "return_to_level_select")
        self.start_menu_list.append(return_to_level_select)
        self.button_list.append(return_to_level_select)

    def on_resize(self, width: int, height: int):
        original_viewport = self.get_viewport()
        if height < 560:
            self.set_size(width, 560)
        if width % 2 == 1:
            self.set_size(width + 1, height)

        self.set_viewport(original_viewport[0],
                          original_viewport[0] + width,
                          original_viewport[2],
                          original_viewport[2] + height)

    def on_draw(self):
        arcade.start_render()
        self.sky.draw()
        if CLOUDS:
            self.clouds.draw()
            self.clouds2.draw()

        if self.playing:
            self.asset_list.draw()
            self.player_list.draw()
            self.wall_list.draw()
            self.coins_list.draw()
            self.pystone_list.draw()
            self.pause_button.draw()
            draw_points(f"Points: {self.current_level_points}", self, self.player, 0)
            level = f"level_{self.level}_points"
            draw_points(f"High Score: {self.level_points[level]}", self, self.player, 40)
            if self.paused:
                self.pause_menu.draw()
        else:
            self.start_menu_list.draw()
            arcade.draw_text(f"Total Points: {self.total_points}", 10, 10, (255, 255, 255), 30)

    def on_key_press(self, symbol: int, modifiers: int):
        if symbol == arcade.key.UP or symbol == arcade.key.W or symbol == arcade.key.SPACE:
            PyPhy.jump(self.player, self.asset_list)
        elif symbol == arcade.key.DOWN or symbol == arcade.key.S:
            PyPhy.crouch(self.player, True)
        elif symbol == arcade.key.LEFT or symbol == arcade.key.A:
            PyPhy.left_input(self.player, True)
        elif symbol == arcade.key.RIGHT or symbol == arcade.key.D:
            PyPhy.right_input(self.player, True)
        elif symbol == arcade.key.ESCAPE:
            self.start_menu()

    def on_key_release(self, symbol: int, modifiers: int):
        if symbol == arcade.key.LEFT or symbol == arcade.key.A:
            PyPhy.left_input(self.player, False)
        elif symbol == arcade.key.RIGHT or symbol == arcade.key.D:
            PyPhy.right_input(self.player, False)
        elif symbol == arcade.key.DOWN or symbol == arcade.key.S:
            PyPhy.crouch(self.player, False)

    def on_update(self, delta_time: float):
        if self.playing and not self.paused:
            self.player_list.update()
            if self.player.center_y < self.kill_y:
                self.quit()
            if not self.playing:
                return

            self.clouds_x += .3
            if self.clouds_x > 1920:
                self.clouds_x = 0
            self.clouds.center_x = self.player.center_x - self.clouds_x
            self.clouds2.center_x = self.clouds.center_x + 1920
            self.asset_list.update()
            size = self.get_size()
            size_x = size[0]
            size_y = size[1]
            margin_space = 280
            if self.player.center_y > (self.bottom_y + size_y - margin_space):
                difference = int(self.player.center_y - (self.bottom_y + size_y - margin_space))
                self.bottom_y += difference
            elif self.player.center_y < (self.bottom_y + margin_space):
                difference = int(self.player.center_y - (self.bottom_y + margin_space))
                self.bottom_y += difference
            self.clouds.center_y = self.bottom_y + (1920 / 4)
            self.clouds2.center_y = self.clouds.center_y
            arcade.set_viewport(self.player.center_x - (size_x / 2), self.player.center_x + (size_x / 2), self.bottom_y,
                                size_y + self.bottom_y)
            self.pause_button.center_x = self.player.center_x - size_x / 2 + 60
            self.pause_button.center_y = self.bottom_y + size_y - 60
            self.sky.center_x = self.player.center_x
            self.sky.center_y = 1080 / 2 + self.bottom_y


def main():
    window = Game(1920, 1017, "Pyteria")
    window.maximize()
    window.start_menu()
    arcade.run()


if __name__ == '__main__':
    main()
