import os
import json

def load_file():
    if not os.path.exists("PushOver_Save.txt"):
        print("Creating new save file")
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
        json_string = json.dumps(new_save_table)
        file = open("PushOver_Save.txt", 'x')
        file.close()

        write_file = open("PushOver_Save.txt", 'w')
        write_file.write(json_string)
        write_file.close()

        return new_save_table, False
    else:
        print("Already had save file")
    save_file = open("PushOver_Save.txt")
    json_string = save_file.read()
    save_table = json.loads(json_string)
    save_file.close()
    return save_table, True

def save_data(data):
    print("saving_data")
    if not os.path.exists("PushOver_Save.txt"):
        json_string = json.dumps(data)
        file = open("PushOver_Save.txt", 'x')
        file.close()

        save_file = open("PushOver_Save.txt", 'w')
        save_file.write(json_string)
        save_file.close()
    else:
        json_string = json.dumps(data)
        save_file = open("PushOver_Save.txt", 'w')
        save_file.write(json_string)
        save_file.close()


