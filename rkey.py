import pyautogui
import time
from enum import IntEnum
from isaac_log_parser import IsaacLogParser
from PIL import Image
from emailer import send_email
from ids_to_quality import get_item_ids_to_quality, get_player_starting_items
from game_setup import borderless_fullscreen_window
import config_reader

id_to_quality = get_item_ids_to_quality()
starting_items = get_player_starting_items()
movement_to_shooting = {"w": "up", "a": "left", "s": "down", "d": "right"}
target_quality = config_reader.get_data("target_quality")
sample_point = config_reader.get_data("sample_point")
email_recipient = config_reader.get_data("email_recipient")
screenshot_region = config_reader.get_data("screenshot_region")


class BotStates(IntEnum):
    SEARCHING = 0
    RKEYING = 1
    MOVING = 2
    FOUND = 3


def move(key, sleep_time):
    pyautogui.keyDown(key)
    time.sleep(sleep_time)
    pyautogui.keyUp(key)


def move_around_block(xdir=None, ydir=None):
    if xdir != None:
        move("w", 0.3)
        move(xdir, 0.3)
        move("s", 0.3)
    elif ydir != None:
        move("d", 0.3)
        move(xdir, 0.3)
        move("a", 0.3)
    else:
        raise TypeError


def main():
    print("STARTING!")
    time.sleep(3)
    borderless_fullscreen_window("Binding of Isaac: Repentance")
    treasure_room_icon = Image.open("data/treasure_room_icon.png")
    parser = IsaacLogParser()
    current_state = BotStates.SEARCHING
    dirx = None
    diry = None

    while True:
        if current_state == BotStates.RKEYING:
            move("r", 2)
            current_state = BotStates.SEARCHING
            continue
        elif current_state == BotStates.SEARCHING:
            minimap_capture = None
            result = None
            dirx = None
            diry = None
            minimap_capture = pyautogui.screenshot(
                region=(
                    screenshot_region["x"],
                    screenshot_region["y"],
                    screenshot_region["width"],
                    screenshot_region["height"],
                )
            )
            result = pyautogui.locate(
                treasure_room_icon, minimap_capture, grayscale=True, confidence=0.9
            )
            if result != None:
                minimap_center = (
                    result.left + result.width / 2,
                    result.top + result.height / 2,
                )
                deltax = (minimap_center[0] + screenshot_region["x"]) - sample_point[
                    "x"
                ]
                deltay = (minimap_center[1] + screenshot_region["y"]) - sample_point[
                    "y"
                ]
                if abs(deltax) > abs(deltay):
                    dirx = "d" if deltax >= 0 else "a"
                else:
                    diry = "s" if deltay >= 0 else "w"
                current_state = BotStates.MOVING
                continue
            else:
                current_state = BotStates.RKEYING
                continue
        elif current_state == BotStates.MOVING:
            if dirx != None:
                shoot_dir = movement_to_shooting[dirx]
                pyautogui.keyDown(shoot_dir)
                move("w", 0.3)
                move(dirx, 5)
                pyautogui.keyUp(shoot_dir)
            elif diry != None:
                shoot_dir = movement_to_shooting[diry]
                pyautogui.keyDown(shoot_dir)
                move(diry, 5)
                pyautogui.keyUp(shoot_dir)
            else:
                raise ValueError
            parser.parse()
            try:
                item_id, item_name, player_name = parser.get_most_recent_item()
            except ValueError:
                if dirx != None:
                    move_around_block(xdir=dirx)
                elif diry != None:
                    move_around_block(ydir=diry)
                parser.parse()
                try:
                    item_id, item_name, player_name = parser.get_most_recent_item()
                except ValueError:
                    current_state = BotStates.RKEYING
                    continue

            if (
                id_to_quality[item_id] == target_quality
                and starting_items[player_name] != item_id
            ):
                current_state = BotStates.FOUND
                continue
            else:
                current_state = BotStates.RKEYING
                continue
        elif current_state == BotStates.FOUND:
            print("dance")
            pyautogui.press("esc")
            send_email(item_name, email_recipient)
            break


if __name__ == "__main__":
    main()
