from PIL import Image
import time


def can_find_treasure_room_test():
    import pyautogui

    while True:
        for result in pyautogui.locateAllOnScreen("treasureroomicon.png"):
            print(result)
        time.sleep(".1")


def can_screenshot_test():
    import pyautogui

    time.sleep(5)
    pyautogui.screenshot("screenshot.png")


def in_game_screenshot_test():
    import pyautogui

    time.sleep(3)
    pyautogui.keyDown("r")
    for x in range(50):
        time.sleep(1)
        minimap_capture = None
        minimap_capture = pyautogui.screenshot(region=(1651, 99, 115, 115))
        minimap_capture.save(f"test_screenshots/debug{x}.png")
    pyautogui.keyUp("r")


if __name__ == "__main__":
    in_game_screenshot_test()
