import pyautogui
import time
import keyboard

safe_odds = ["evens", 2, 3, 4]


def ezmouse_click():
    pyautogui.mouseDown(button="left")
    pyautogui.mouseUp(button="left")


def ez_tab():
    keyboard.press("tab")
    time.sleep(0.1)
    keyboard.release("tab")


time.sleep(3)

found_odds = None

for odds in ["evens"] + list(range(2, 11)) + list(range(12, 31)):
    template = f"templates/{odds}.png"

    try:
        result = pyautogui.locateOnScreen(
            template,
            confidence=0.9
        )

        if result:
            found_odds = odds
            print(f"Found lowest odds: {odds}")

            pyautogui.moveTo(pyautogui.center(result))
            ezmouse_click()

            break

    except pyautogui.ImageNotFoundException:
        pass


if found_odds in safe_odds:
    print("Safe odds - betting $10,000")
    ez_tab()


def click_start_race():
    time.sleep(3)

    try:
        start_race_button = pyautogui.locateOnScreen(
            "templates/placebet-startrace.png",
            confidence=0.9
        )

        if start_race_button:
            pyautogui.moveTo(pyautogui.center(start_race_button))
            ezmouse_click()
            print("Race started.")

        else:
            print("Could not find Place Bet / Start Race button.")

    except pyautogui.ImageNotFoundException:
        print("Could not find Place Bet / Start Race button.")


click_start_race()