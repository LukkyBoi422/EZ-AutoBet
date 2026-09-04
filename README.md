# EZ-AutoBet
This is an improved and way better version of my previous EZAutoBet for GTA 5 Online, while very much simpler it's way better in performance and making money.

This works on both GTA 5 Legacy and Enhanced

This works by having a list of safe odds that are safe to bet 10k max bet on like
Evens, 2/1, 3/1, 4/1
As the chances of winning are higher on those what it does is it checks going from evens
all the way to 30/1 and clicks the lowest possible bet


# Keybinds
F10 START
F9 STOP

![Banner](gh-media/example.png)  

# Build it yourself?
Pyinstaller Commmand:
python -m PyInstaller --onedir --noconsole --add-data "templates;templates" --add-data "icon.ico;." --icon=icon.ico --name EZAutoBet main.py

When it builds put the icon.ico in the directory of the build so it doesn't crash

Python Version:
Python 3.13.15