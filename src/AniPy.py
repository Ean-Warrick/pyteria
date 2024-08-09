import arcade

animation_table = {
    # Handles Static Animations
    "static": {
        "falling": {
            "left": {"texture": arcade.load_texture("src/textures/player_falling_right.png", 0, 0, 60, 104, True, False, False), "height": 104, "width": 32},
            "right": {"texture": arcade.load_texture("src/textures/player_falling_right.png", 0, 0, 60, 104, False, False, False), "height": 104, "width": 32}
        },
        "jumping": {
            "left": {"texture": arcade.load_texture("src/textures/player_jumping_right.png", 0, 0, 60, 104, True, False, False), "height": 104, "width": 32},
            "right": {"texture": arcade.load_texture("src/textures/player_jumping_right.png", 0, 0, 60, 104, False, False, False), "height": 104, "width": 32}
        },
        "crouching": {
            "left": {"texture": arcade.load_texture("src/textures/player_crouching_right.png", 0, 0, 60, 104, True, False, False), "height": 73, "width": 32},
            "right": {"texture": arcade.load_texture("src/textures/player_crouching_right.png", 0, 0, 60, 104, False, False, False), "height": 73, "width": 32}
        },
        "standing": {
            "left": {"texture": arcade.load_texture("src/textures/player_right_1.png", 0, 0, 60, 104, True, False, False), "height": 104, "width": 32},
            "right": {"texture": arcade.load_texture("src/textures/player_right_1.png", 0, 0, 60, 104, False, False, False), "height": 104, "width": 32}
        },
    },
    # Handles Dynamic Animations
    "dynamic": {
        "walking": {
            "1": {"left": {"texture": arcade.load_texture("src/textures/player_right_1.png", 0, 0, 60, 104, True, False, False), "height": 104, "width": 32},
                  "right": {"texture": arcade.load_texture("src/textures/player_right_1.png", 0, 0, 60, 104, False, False, False), "height": 104, "width": 32}
            },
            "2": {"left": {"texture": arcade.load_texture("src/textures/player_right_2.png", 0, 0, 60, 104, True, False, False), "height": 104, "width": 32},
                  "right": {"texture": arcade.load_texture("src/textures/player_right_2.png", 0, 0, 60, 104, False, False, False), "height": 104, "width": 32}
            },
            "3": {"left": {"texture": arcade.load_texture("src/textures/player_right_3.png", 0, 0, 60, 104, True, False, False), "height": 104, "width": 32},
                  "right": {"texture": arcade.load_texture("src/textures/player_right_3.png", 0, 0, 60, 104, False, False, False), "height": 104, "width": 32}
            },
            "4": {"left": {"texture": arcade.load_texture("src/textures/player_right_4.png", 0, 0, 60, 104, True, False, False), "height": 104, "width": 32},
                  "right": {"texture": arcade.load_texture("src/textures/player_right_4.png", 0, 0, 60, 104, False, False, False), "height": 104, "width": 32}
            },
            "5": {"left": {"texture": arcade.load_texture("src/textures/player_right_5.png", 0, 0, 60, 104, True, False, False), "height": 104, "width": 32},
                  "right": {"texture": arcade.load_texture("src/textures/player_right_5.png", 0, 0, 60, 104, False, False, False), "height": 104, "width": 32}
            },
            "6": {"left": {"texture": arcade.load_texture("src/textures/player_right_4.png", 0, 0, 60, 104, True, False, False), "height": 104, "width": 32},
                  "right": {"texture": arcade.load_texture("src/textures/player_right_4.png", 0, 0, 60, 104, False, False, False), "height": 104, "width": 32}
            },
            "7": {"left": {"texture": arcade.load_texture("src/textures/player_right_3.png", 0, 0, 60, 104, True, False, False), "height": 104, "width": 32},
                  "right": {"texture": arcade.load_texture("src/textures/player_right_3.png", 0, 0, 60, 104, False, False, False), "height": 104, "width": 32}
            },
            "8": {"left": {"texture": arcade.load_texture("src/textures/player_right_2.png", 0, 0, 60, 104, True, False, False), "height": 104, "width": 32},
                  "right": {"texture": arcade.load_texture("src/textures/player_right_2.png", 0, 0, 60, 104, False, False, False), "height": 104, "width": 32}
            },
            "9": {"left": {"texture": arcade.load_texture("src/textures/player_right_1.png", 0, 0, 60, 104, True, False, False), "height": 104, "width": 32},
                  "right": {"texture": arcade.load_texture("src/textures/player_right_1.png", 0, 0, 60, 104, False, False, False), "height": 104, "width": 32}
            },
            "10": {"left": {"texture": arcade.load_texture("src/textures/player_right_6.png", 0, 0, 60, 104, True, False, False), "height": 104, "width": 32},
                  "right": {"texture": arcade.load_texture("src/textures/player_right_6.png", 0, 0, 60, 104, False, False, False), "height": 104, "width": 32}
            },
            "11": {"left": {"texture": arcade.load_texture("src/textures/player_right_7.png", 0, 0, 60, 104, True, False, False), "height": 104, "width": 32},
                  "right": {"texture": arcade.load_texture("src/textures/player_right_7.png", 0, 0, 60, 104, False, False, False), "height": 104, "width": 32}
            },
            "12": {"left": {"texture": arcade.load_texture("src/textures/player_right_8.png", 0, 0, 60, 104, True, False, False), "height": 104, "width": 32},
                  "right": {"texture": arcade.load_texture("src/textures/player_right_8.png", 0, 0, 60, 104, False, False, False), "height": 104, "width": 32}
            },
            "13": {"left": {"texture": arcade.load_texture("src/textures/player_right_9.png", 0, 0, 60, 104, True, False, False), "height": 104, "width": 32},
                  "right": {"texture": arcade.load_texture("src/textures/player_right_9.png", 0, 0, 60, 104, False, False, False), "height": 104, "width": 32}
            },
            "14": {"left": {"texture": arcade.load_texture("src/textures/player_right_10.png", 0, 0, 60, 104, True, False, False), "height": 104, "width": 32},
                  "right": {"texture": arcade.load_texture("src/textures/player_right_10.png", 0, 0, 60, 104, False, False, False), "height": 104, "width": 32}
            },
            "15": {"left": {"texture": arcade.load_texture("src/textures/player_right_9.png", 0, 0, 60, 104, True, False, False), "height": 104, "width": 32},
                  "right": {"texture": arcade.load_texture("src/textures/player_right_9.png", 0, 0, 60, 104, False, False, False), "height": 104, "width": 32}
            },
            "16": {"left": {"texture": arcade.load_texture("src/textures/player_right_8.png", 0, 0, 60, 104, True, False, False), "height": 104, "width": 32},
                  "right": {"texture": arcade.load_texture("src/textures/player_right_8.png", 0, 0, 60, 104, False, False, False), "height": 104, "width": 32}
             },
            "17": {"left": {"texture": arcade.load_texture("src/textures/player_right_7.png", 0, 0, 60, 104, True, False, False), "height": 104, "width": 32},
                  "right": {"texture": arcade.load_texture("src/textures/player_right_7.png", 0, 0, 60, 104, False, False, False), "height": 104, "width": 32}
            },
            "18": {"left": {"texture": arcade.load_texture("src/textures/player_right_6.png", 0, 0, 60, 104, True, False, False), "height": 104, "width": 32},
                  "right": {"texture": arcade.load_texture("src/textures/player_right_6.png", 0, 0, 60, 104, False, False, False), "height": 104, "width": 32}
            },
        },
        "crawling": {
            "1": {
                "left": {"texture": arcade.load_texture("src/textures/player_crawling_right_1.png", 0, 0, 90, 71, True, False, False), "height": 104, "width": 32},
                "right": {"texture": arcade.load_texture("src/textures/player_crawling_right_1.png", 0, 0, 90, 71, False, False, False), "height": 104, "width": 32}
            },
            "2": {
                "left": {"texture": arcade.load_texture("src/textures/player_crawling_right_2.png", 0, 0, 90, 71, True, False, False), "height": 104, "width": 32},
                "right": {"texture": arcade.load_texture("src/textures/player_crawling_right_2.png", 0, 0, 90, 71, False, False, False), "height": 104, "width": 32}
            },
            "3": {
                "left": {"texture": arcade.load_texture("src/textures/player_crawling_right_1.png", 0, 0, 90, 71, True, False, False), "height": 104, "width": 32},
                "right": {"texture": arcade.load_texture("src/textures/player_crawling_right_1.png", 0, 0, 90, 71, False, False, False), "height": 104, "width": 32}
            },
            "4": {
                "left": {"texture": arcade.load_texture("src/textures/player_crawling_right_3.png", 0, 0, 90, 71, True, False, False), "height": 104, "width": 32},
                "right": {"texture": arcade.load_texture("src/textures/player_crawling_right_3.png", 0, 0, 90, 71, False, False, False), "height": 104, "width": 32}
            }
        },
        "standing": {
            "1": {
                "left": {"texture": arcade.load_texture("src/textures/player_right_standing_1.png", 0, 0, 60, 104, True, False, False), "height": 104, "width": 32},
                "right": {"texture": arcade.load_texture("src/textures/player_right_standing_1.png", 0, 0, 60, 104, False, False, False), "height": 104, "width": 32}
            },
            "2": {
                "left": {"texture": arcade.load_texture("src/textures/player_right_standing_2.png", 0, 0, 60, 104, True, False, False), "height": 104, "width": 32},
                "right": {"texture": arcade.load_texture("src/textures/player_right_standing_2.png", 0, 0, 60, 104, False, False, False), "height": 104, "width": 32}
            },
            "3": {
                "left": {"texture": arcade.load_texture("src/textures/player_right_standing_1.png", 0, 0, 60, 104, True, False, False), "height": 104, "width": 32},
                "right": {"texture": arcade.load_texture("src/textures/player_right_standing_1.png", 0, 0, 60, 104, False, False, False), "height": 104, "width": 32}
            },
            "4": {
                "left": {"texture": arcade.load_texture("src/textures/player_right_standing_4.png", 0, 0, 60, 104, True, False, False), "height": 104, "width": 32},
                "right": {"texture": arcade.load_texture("src/textures/player_right_standing_4.png", 0, 0, 60, 104, False, False, False), "height": 104, "width": 32}
            },
        }
    }
}


def retrieve_static_texture_info(action, direction):
    return animation_table["static"][action][direction]


def retrieve_dynamic_animation_info(action, direction, frame):
    return animation_table["dynamic"][action][frame][direction]
