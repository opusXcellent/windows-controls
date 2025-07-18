import time
import json
import os
import ctypes
import getpass
import datetime
import subprocess

DATA_FILE = "C:\\ParentalControl\\user_time_limits.json"

def load_limits():
    with open(DATA_FILE, "r") as f:
        return json.load(f)

def save_limits(data):
    with open(DATA_FILE, "w") as f:
        json.dump(data, f, indent=4)

def disable_account(user):
    subprocess.call(["net", "user", user, "/active:no"])

def enable_account(user):
    subprocess.call(["net", "user", user, "/active:yes"])

def force_logout():
    ctypes.windll.user32.ExitWindowsEx(0, 1)

def main():
    user = getpass.getuser()
    while True:
        try:
            limits = load_limits()
            now = datetime.datetime.now()
            today_str = now.strftime("%Y-%m-%d")

            if user not in limits:
                time.sleep(60)
                continue

            user_data = limits[user]

            # Reset usage daily
            if user_data["last_login_date"] != today_str:
                user_data["minutes_used_today"] = 0
                user_data["last_login_date"] = today_str

                if user_data["account_disabled"]:
                    enable_account(user)
                    user_data["account_disabled"] = False

            if user_data["minutes_used_today"] >= user_data["daily_limit_minutes"]:
                if not user_data["account_disabled"]:
                    disable_account(user)
                    user_data["account_disabled"] = True
                    save_limits(limits)
                    force_logout()
                time.sleep(60)
                continue

            # Time remaining
            remaining = user_data["daily_limit_minutes"] - user_data["minutes_used_today"]

            # Send remaining time to overlay
            with open("C:\\ParentalControl\\time_left.txt", "w") as f:
                f.write(str(remaining))

            if remaining == 15:
                show_warning_popup()

            user_data["minutes_used_today"] += 1
            save_limits(limits)

            time.sleep(60)
        except Exception as e:
            with open("C:\\ParentalControl\\error.log", "a") as err:
                err.write(str(e) + "\n")
            time.sleep(60)

def show_warning_popup():
    from tkinter import Tk, messagebox
    root = Tk()
    root.withdraw()
    messagebox.showinfo("Parental Control", "Only 15 minutes remaining. Click OK to continue.")
    root.destroy()

if __name__ == "__main__":
    main()
