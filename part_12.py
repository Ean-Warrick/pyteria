import arcade
import math


class PlayerSprite(arcade.Sprite):
    def __init__(self, file, scaling):
        super().__init__(file, scaling)


class Screen(arcade.Sprite):
    def __init__(self, file, scaling):
        super().__init__(file, scaling)
        self.center_x = 400
        self.center_y = 400




class Game(arcade.Window):
    def __init__(self, width, height, title):
        super().__init__(width, height, title, resizable=True)
        self.WIDTH = math.floor(self.screen.width / 2)
        self.HEIGHT = math.floor(self.screen.height / 2)
        self.set_size(self.WIDTH, self.HEIGHT)
        self.scaling = self.HEIGHT / 1080
        self.screen_location = None
        self.maximize()
        self.screen_obj = Screen("dirt_tile.png", self.scaling, self.scaling)
        self.screens = arcade.SpriteList()
        self.screens.append(self.screen_obj)

    def start_screen(self):
        self.screen_location = "start"

    def choose_class(self):
        self.screen_location = "class"

    def on_draw(self):
        self.screens.draw()

    def on_resize(self, width: float, height: float):
        super().on_resize(width, height)
        print(width, height)
        self.scaling = height / 1080
        print(self.scaling)
        self.screens.update(self.scaling)



    def set_up(self):
        pass

    def on_key_press(self, symbol: int, modifiers: int):
        pass
       # if symbol == arcade.key.ESCAPE or symbol == arcade.key.E:
            #self.set_fullscreen(False)
       #elif symbol == arcade.key.F11:
            #self.set_fullscreen()
        #elif symbol == arcade.key.R:
            #self.close()


def main():
    window = Game(400, 400, "Final")
    window.set_up()
    arcade.run()


if __name__ == "__main__":
    main()
