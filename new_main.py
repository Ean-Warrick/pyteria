import arcade
import math
import Pydle
import PyPhy
import PyDow
import GoPy
import PyMap
import os


def update_viewport(player, window):
    size = arcade.get_viewport()
    size_x1 = size[0]
    size_x2 = size[1]
    size_y1 = size[2]
    size_y2 = size[3]

    size_y = size_y2 - size_y1
    size_x = size_x2 - size_x1

    margin_space = 280
    if player.center_y > (window.bottom_y + size_y - margin_space):
        difference = int(player.center_y - (window.bottom_y + size_y - margin_space))
        window.bottom_y += difference
    elif player.center_y < (window.bottom_y + margin_space):
        difference = int(player.center_y - (window.bottom_y + margin_space))
        window.bottom_y += difference
    arcade.set_viewport(player.center_x - (size_x / 2), player.center_x + (size_x / 2), window.bottom_y, size_y + window.bottom_y)


def load_walls(map, wall_list, coin_list, pystone_list, asset_list):
    for row_number, row_list in enumerate(map):
        for column_number, object_block in enumerate(row_list):
            if object_block == 1:
                crate = Crate("dirt_tile.png", 1)
                crate.center_x = 20 + 40 * column_number
                crate.center_y = 20 + 40 * row_number
                wall_list.append(crate)
            elif object_block == 2:
                crate = Crate("dirt_grass_top_tile.png", 1)
                crate.center_x = 20 + 40 * column_number
                crate.center_y = 20 + 40 * row_number
                wall_list.append(crate)
            elif object_block == 3:
                crate = Crate("stone_tile.png", 1)
                crate.center_x = 20 + 40 * column_number
                crate.center_y = 20 + 40 * row_number
                wall_list.append(crate)
            elif object_block == 4:
                pass
            elif object_block == 5:
                pass
            elif object_block == 6:
                pass
            elif object_block == 7:
                pass
            elif object_block == 8:
                pystone = Crate("pystone.png", 1)
                pystone.center_x = 20 + 40 * column_number
                pystone.center_y = 20 + 40 * row_number
                pystone_list.append(pystone)

                pystone_holder = Crate("pystone_holder.png", 1)
                pystone_holder.center_x = 20 + 40 * column_number
                pystone_holder.center_y = 20 + 40 * row_number
                asset_list.append(pystone_holder)
            elif object_block == 9:
                coin = Crate("coin.png", 1)
                coin.center_x = 20 + 40 * column_number
                coin.center_y = 20 + 40 * row_number
                coin_list.append(coin)


class Crate(arcade.Sprite):
    def __init__(self, file, scaling):
        super().__init__(file, scaling)


class Player(arcade.Sprite):
    def __init__(self, file, scaling, game):
        super().__init__(file, scaling)
        self.center_y = 800
        self.center_x = 400
        self.game = game

    def update(self):
        PyPhy.update(self, self.game)


def draw_points(points, game, player):
    size = game.get_size()
    size_x = size[0]
    size_y = size[1]
    arcade.draw_text(f"Points: {points}", player.center_x - (size_x / 2) + 10, game.bottom_y + 10, (255, 255, 255), 40)


class Game(arcade.Window):
    def __init__(self, width, height, title):
        super().__init__(width, height, title, resizable=True)
        self.old_viewport = self.get_viewport()
        self.bottom_y = 0
        self.button_list = None
        self.data = False
        # data
        self.levels = None
        self.total_points = None
        self.level_points = None
        save_data, self.data = Pydle.load_file()
        self.load_data(save_data)

        self.current_level_points = 0
        PyDow.initiate(self, True, True)
        arcade.set_background_color((100, 200, 255))
        self.map = None
        self.holding_pystone = False
        self.wall_list = arcade.SpriteList()
        self.player_list = arcade.SpriteList()
        self.player = None
        self.asset_list = arcade.SpriteList()
        self.coins_list = arcade.SpriteList()
        self.pystone_list = arcade.SpriteList()
        self.settings_icon = arcade.Sprite("pyteria_menu_imgs/settings_icon.png", 1)
        self.settings_icon.center_x = 60
        self.settings_icon.center_y = 950
        # pause_menu
        self.pause_menu = arcade.SpriteList()
        self.pause_screen = arcade.Sprite("pyteria_menu_imgs/pause_menu.png", 1)
        self.pause_menu.append(self.pause_screen)
        self.quit_level = arcade.Sprite("pyteria_menu_imgs/quit_level.png", 1)
        self.pause_menu.append(self.quit_level)

        # menu stuff
        self.playing = False
        self.paused = False
        self.menu_window = None
        self.start_menu_list = None

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

    def start_menu(self):
        self.start_menu_list, self.button_list = GoPy.create_start_menu(self)
        self.playing = False
        self.menu_window = "start_menu"

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

    def level_select(self):
        self.playing = False
        self.start_menu_list = GoPy.create_level_select(self)
        self.menu_window = "level_select"
        print(self.get_viewport()[0])

    def on_mouse_press(self, x: float, y: float, button: int, modifiers: int):
        print(x, y)
        if not self.playing:
            GoPy.click_mouse(x, y, self.button_list, self)
        else:
            GoPy.game_pause(x, y, self)

    def play(self, level):
        # clear_lists
        self.player_list = arcade.SpriteList()
        self.holding_pystone = False
        # Loading Level / Map
        self.map = PyMap.load_map(level)
        self.wall_list = arcade.SpriteList()
        self.coins_list = arcade.SpriteList()
        load_walls(self.map, self.wall_list, self.coins_list, self.pystone_list, self.asset_list)
        PyPhy.map_file(self.map, self.wall_list, self.coins_list, self.pystone_list)
        # Creating Player (Important to do this after loading map)
        self.player = Player("player_front.png", 1, self)
        self.player_list.append(self.player)
        PyPhy.initiate(self.player)
        self.playing = True


    def on_draw(self):
        arcade.start_render()
        if self.playing:
            self.player_list.draw()
            self.wall_list.draw()
            self.coins_list.draw()
            self.pystone_list.draw()
            self.asset_list.draw()
            self.settings_icon.draw()
            draw_points(self.current_level_points, self, self.player)
            if self.paused:
                self.pause_menu.draw()
        else:
            self.start_menu_list.draw()

    def on_key_press(self, symbol: int, modifiers: int):
        if symbol == arcade.key.UP or symbol == arcade.key.W or symbol == arcade.key.SPACE:
            PyPhy.jump(self.player, self.asset_list)
        elif symbol == arcade.key.DOWN or symbol == arcade.key.S:
            PyPhy.crouch(self.player, True)
        elif symbol == arcade.key.LEFT or symbol == arcade.key.A:
            PyPhy.left_input(self.player, True)
        elif symbol == arcade.key.RIGHT or symbol == arcade.key.D:
            PyPhy.right_input(self.player, True)

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
            self.asset_list.update()
            update_viewport(self.player, self)
            size = self.get_size()
            size_x = size[0]
            size_y = size[1]
            self.settings_icon.center_x = self.player.center_x - (size_x / 2) + 60
            self.settings_icon.center_y = self.bottom_y + size_y - 60
            self.settings_icon.center_x = self.player.center_x - (size_x / 2) + 55
            self.settings_icon.center_y = self.bottom_y + size_y - 55
            self.settings_icon.scale = size_y / 1080
        elif self.playing and self.pause_menu:
            size = self.get_size()
            size_x = size[0]
            size_y = size[1]
            self.pause_screen.center_x = self.player.center_x - int(size_x / 4)
            self.pause_screen.center_y = self.bottom_y + (size_y / 2)
            self.quit_level.center_x = self.player.center_x - int(size_x / 4)
            self.quit_level.center_y = self.bottom_y + (size_y / 2)
            self.pause_screen.scale = size_y / 1080
            self.quit_level.scale = size_y / 1080
            self.settings_icon.center_x = self.player.center_x - (size_x / 2) + 55
            self.settings_icon.center_y = self.bottom_y + size_y - 55
            self.settings_icon.scale = size_y / 1080


def main():
    window = Game(700, 700, "FINAL")
    window.start_menu()
    arcade.run()


if __name__ == '__main__':
    main()
