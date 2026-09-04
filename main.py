
import pyautogui
import time
import keyboard
import tkinter as tk
import threading


# ============================================================
# CONFIG
# ============================================================

safe_odds = ["evens", 2, 3, 4]

MAX_BET = 10000
MIN_BET = 100

running = False

money_earned = 0
races_won = 0
start_time = None


# ============================================================
# INPUT HELPERS
# ============================================================

def ezmouse_click():
    pyautogui.mouseDown(button="left")
    pyautogui.mouseUp(button="left")


def ez_tab():
    keyboard.press("tab")
    time.sleep(0.1)
    keyboard.release("tab")


def ez_esc():
    keyboard.press("esc")
    time.sleep(0.1)
    keyboard.release("esc")


# ============================================================
# IMAGE HELPERS
# ============================================================

def find_image(image):
    try:
        return pyautogui.locateOnScreen(
            image,
            confidence=0.9
        )
    except pyautogui.ImageNotFoundException:
        return None


def wait_for_image(image):
    while running:

        result = find_image(image)

        if result:
            return result

        time.sleep(0.05)

    return None


# ============================================================
# ODDS / MONEY
# ============================================================

def get_odds_value(odds):

    if odds == "evens":
        return 1

    return odds


def calculate_profit(odds, bet):

    odds_value = get_odds_value(odds)

    return bet * odds_value


# ============================================================
# GUI UPDATE
# ============================================================

def update_gui():
    global running, start_time, money_earned, races_won

    if running and start_time is not None:

        elapsed = int(time.time() - start_time)

        hours = elapsed // 3600
        minutes = (elapsed % 3600) // 60
        seconds = elapsed % 60

        time_label.config(
            text=f"Time Running: {hours:02d}:{minutes:02d}:{seconds:02d}"
        )

    money_label.config(
        text=f"Money Earned: ${money_earned:,}"
    )

    races_won_label.config(
        text=f"Races Won: {races_won}"
    )

    root.after(250, update_gui)


def add_money(amount):
    global money_earned

    money_earned += amount

    print(
        f"Money change: ${amount:+,}"
    )

    print(
        f"Total money earned: ${money_earned:,}"
    )


# ============================================================
# MAIN BOT
# ============================================================

def bot():
    global running
    global races_won

    while running:

        # 1. OPEN INSIDE TRACK

        print("Waiting for Open UI...")

        open_ui = wait_for_image(
            "templates/placebet-openui.png"
        )

        if not running:
            return

        if open_ui:

            pyautogui.moveTo(
                pyautogui.center(open_ui)
            )

            ezmouse_click()

            print("Open UI clicked.")

        # 2. FIND LOWEST ODDS

        found_odds = None

        odds_list = (
            ["evens"]
            + list(range(2, 11))
            + list(range(12, 31))
        )

        for odds in odds_list:

            if not running:
                return

            result = find_image(
                f"templates/{odds}.png"
            )

            if result:

                found_odds = odds

                print(
                    f"Found lowest odds: {odds}"
                )

                pyautogui.moveTo(
                    pyautogui.center(result)
                )

                ezmouse_click()

                print("Horse selected.")

                break

        if not running:
            return

        # 3. DETERMINE BET AMOUNT

        if found_odds in safe_odds:

            bet_amount = MAX_BET

            print(
                f"Safe odds ({found_odds}) - betting ${MAX_BET:,}"
            )

            ez_tab()

        else:

            bet_amount = MIN_BET

            print(
                f"Unsafe odds ({found_odds}) - betting ${MIN_BET:,}"
            )

        if not running:
            return

        # 4. PLACE BET / START RACE

        print(
            "Waiting for Place Bet / Start Race..."
        )

        placebet = wait_for_image(
            "templates/placebet-startrace.png"
        )

        if not running:
            return

        if placebet:

            pyautogui.moveTo(
                pyautogui.center(placebet)
            )

            ezmouse_click()

            print(
                f"Race started. Bet: ${bet_amount:,}"
            )

        # 5. WAIT FOR RESULTS

        print("Waiting for results...")

        results = wait_for_image(
            "templates/results-page.png"
        )

        if not running:
            return

        if results:

            print("Results detected.")

            time.sleep(2)

            if not running:
                return

            # 6. CHECK IF RACE WAS LOST

            print(
                "Checking for race-lost.png..."
            )

            race_lost = find_image(
                "templates/race-lost.png"
            )

            if race_lost:

                # LOST

                add_money(-bet_amount)

                print(
                    f"RACE LOST - ${bet_amount:,}"
                )

            else:

                # WON

                races_won += 1

                profit = calculate_profit(
                    found_odds,
                    bet_amount
                )

                add_money(profit)

                print(
                    f"RACE WON - {found_odds}/1"
                )

                print(
                    f"Races Won: {races_won}"
                )

                print(
                    f"Bet: ${bet_amount:,}"
                )

                print(
                    f"Profit: +${profit:,}"
                )

            # 7. CLOSE RESULTS

            print("Sending ESC...")

            ez_esc()

            print("ESC sent.")

            time.sleep(0.5)

            print("Results closed.")
            print("Starting next cycle...")


# ============================================================
# START / STOP
# ============================================================

def start_bot():
    global running
    global start_time

    if not running:

        running = True

        start_time = time.time()

        status_label.config(
            text="RUNNING",
            fg="#00ff66"
        )

        print("Bot started.")

        threading.Thread(
            target=bot,
            daemon=True
        ).start()


def stop_bot():
    global running

    running = False

    status_label.config(
        text="STOPPED",
        fg="#ff4444"
    )

    print("Bot stopped.")


def on_close():
    stop_bot()
    root.destroy()


# ============================================================
# GLOBAL HOTKEYS
# ============================================================

keyboard.add_hotkey(
    "f10",
    start_bot
)

keyboard.add_hotkey(
    "f9",
    stop_bot
)


# ============================================================
# GUI
# ============================================================

root = tk.Tk()

root.title("EZ AutoBet")
root.geometry("330x290")
root.iconbitmap("icon.ico")
root.resizable(False, False)

# DARK THEME
BG_COLOR = "#121212"
FG_COLOR = "#ffffff"
BUTTON_BG = "#242424"
BUTTON_ACTIVE = "#333333"
STOPPED_COLOR = "#ff4444"
RUNNING_COLOR = "#00ff66"

root.configure(
    bg=BG_COLOR
)


title_label = tk.Label(
    root,
    text="EZ AutoBet",
    font=("Arial", 18, "bold"), 
    bg=BG_COLOR,
    fg=FG_COLOR
)

title_label.pack(
    pady=(15, 8)
)


status_label = tk.Label(
    root,
    text="STOPPED",
    font=("Arial", 12, "bold"),
    bg=BG_COLOR,
    fg=STOPPED_COLOR
)

status_label.pack(
    pady=5
)


time_label = tk.Label(
    root,
    text="Time Running: 00:00:00",
    font=("Arial", 11),
    bg=BG_COLOR,
    fg=FG_COLOR
)

time_label.pack(
    pady=5
)


money_label = tk.Label(
    root,
    text="Money Earned: $0",
    font=("Arial", 11),
    bg=BG_COLOR,
    fg=FG_COLOR
)

money_label.pack(
    pady=5
)


races_won_label = tk.Label(
    root,
    text="Races Won: 0",
    font=("Arial", 11),
    bg=BG_COLOR,
    fg=FG_COLOR
)

races_won_label.pack(
    pady=5
)


start_button = tk.Button(
    root,
    text="START (F10)",
    width=20,
    command=start_bot,
    bg=BUTTON_BG,
    fg=FG_COLOR,
    activebackground=BUTTON_ACTIVE,
    activeforeground=FG_COLOR,
    relief="flat"
)

start_button.pack(
    pady=5
)


stop_button = tk.Button(
    root,
    text="STOP (F9)",
    width=20,
    command=stop_bot,
    bg=BUTTON_BG,
    fg=FG_COLOR,
    activebackground=BUTTON_ACTIVE,
    activeforeground=FG_COLOR,
    relief="flat"
)

stop_button.pack(
    pady=5
)


root.protocol(
    "WM_DELETE_WINDOW",
    on_close
)


root.after(
    250,
    update_gui
)


root.mainloop()
