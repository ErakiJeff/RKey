import pyautogui
import time
from enum import IntEnum
from isaac_log_parser import IsaacLogParser
from PIL import Image
from emailer import send_email
from game_data import get_item_ids_to_quality, get_player_starting_items
from game_setup import borderless_fullscreen_window
from config_reader import get_data

id_to_quality = get_item_ids_to_quality()
starting_items = get_player_starting_items()
movement_to_shooting = {"w": "up", "a": "left", "s": "down", "d": "right"}
target_quality = get_data("target_quality")
sample_point = get_data("sample_point")
screenshot_region = get_data("screenshot_region")
do_send_email = get_data("do_send_email")
start_delay = get_data("start_delay")


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
        move(ydir, 0.3)
        move("a", 0.3)
    else:
        raise TypeError


def main():
    print("STARTING!")
    time.sleep(start_delay)
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
            parser.flush_new_lines()
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
                raise TypeError
            parser.parse()
            try:
                item_id, item_name, character_name = parser.get_most_recent_item()
            except TypeError:
                print("Should be moving around block")
                if dirx != None:
                    move_around_block(xdir=dirx)
                elif diry != None:
                    move_around_block(ydir=diry)
                parser.parse()
                try:
                    item_id, item_name, character_name = parser.get_most_recent_item()
                except TypeError:
                    current_state = BotStates.RKEYING
                    continue

            if (
                id_to_quality[item_id] == target_quality
                and item_id not in starting_items[character_name]
            ):
                current_state = BotStates.FOUND
                continue
            else:
                current_state = BotStates.RKEYING
                continue
        elif current_state == BotStates.FOUND:
            print("dance")
            pyautogui.press("esc")
            if do_send_email:
                send_email(item_name)
            break


if __name__ == "__main__":
    main()
