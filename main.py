import webbrowser
import sys
import os
import json
import random

try:
    os.system("black -q .")
except ModuleNotFoundError:
    os.system("pip install -r requirements.txt")
    try:
        os.system("black -q .")
    except ModuleNotFoundError:
        print(
            "Error: unable to auto-install black. Please try manually \n pip install -r requirements.txt \n It is not necessary, but recommended"
        )
        print("[1] Ignore and continue")
        print("[2] Exit")
        choice = input("Enter your choice: ")
        if choice == "1":
            pass
        else:
            sys.exit(0)


def resource_path(relative_path):
    """Get a correct file pah for compiled EXE"""
    try:
        # Temp folder PyInstaller
        base_path = sys._MEIPASS
    except AttributeError:
        # Standard mode (launched via Python)
        base_path = os.path.dirname(os.path.abspath(__file__))
    return os.path.join(base_path, relative_path)


with open(resource_path("hiscore.txt"), "r") as file:
    high_score = int(file.read())

with open(resource_path("settings.json"), "r") as file:
    settings = json.load(file)


def clear():
    """Generate command to clear screen depends on os type"""
    os.system("cls" if os.name == "nt" else "clear")


def settings_menu():
    while True:
        clear()
        print("Settings Menu")
        print()
        print("[1] Set attempts count")
        print("[2] Set random number range")
        print("[3] Back to main menu")
        choice = input("Your choice >>>")
        if choice == "1":
            attempts = input('Enter attempts count or "infinity" >>>')
            try:
                settings["attempts_count"] = int(attempts)
            except ValueError:
                if attempts.lower() == "infinity":
                    settings["attempts_count"] = "infinity"
                    with open("settings.json", "w") as file:
                        json.dump(settings, file)
                    input("Success! Press Enter to continue...")
                    continue
                print("Invalid input. Must be number.")
                input("Press Enter to continue...")
                continue

            with open("settings.json", "w") as file:
                json.dump(settings, file)
            input("Success! Press Enter to continue...")
        if choice == "2":
            min_num = input("Enter min number (inclusive) >>>")
            max_num = input("Enter max number (inclusive) >>>")
            try:
                if max_num <= min_num:
                    print("Invalid input. Max number must be greater than min number.")
                    input("Press Enter to continue...")
                    continue

                settings["random_number_range_1"] = int(min_num)
                settings["random_number_range_2"] = int(max_num)

                with open("settings.json", "w") as file:
                    json.dump(settings, file)
                input("Success! Press Enter to continue...")
                continue
            except ValueError:
                print("Invalid input. Must be number.")
                input("Press Enter to continue...")
                continue
        if choice == "3":
            break


def game_over(
    spent_attempts: int,
    attempts_amount: int,
    correct_random_number: int,
    user_suggestions: list,
    system_answers: list,
):
    clear()
    print("============================ GAME OVER ============================")
    print(f"Spent attempts: {spent_attempts}")
    print(f"Total attempts: {attempts_amount}")
    print("Your suggestions:")
    tmp_counter = 1
    for suggestion in len(user_suggestions):
        print(
            f"[{tmp_counter}] {user_suggestions[suggestion]} : {system_answers[suggestion]}"
        )
        tmp_counter += 1
    print()
    print(f"Correct answer was : {correct_random_number}")
    input("Press Enter to continue...")


def winner(
    spent_attempts: int,
    attempts_amount: int,
    correct_random_number: int,
    user_suggestions: list,
    system_answers: list,
):
    global high_score
    clear()
    print("============================ YOU WON ============================")
    print(f"Spent attempts: {spent_attempts} / {attempts_amount}")
    if spent_attempts < high_score:
        high_score = spent_attempts
        print(f"NEW HIGH SCORE!")
        with open("hiscore.txt", "w") as file:
            file.write(high_score)
    print("Your suggestions:")
    tmp_counter = 1
    for suggestion in range(len(user_suggestions)):
        print(
            f"[{tmp_counter}] {user_suggestions[suggestion]} : {system_answers[suggestion]}"
        )
        tmp_counter += 1
    print()
    print(f"Correct answer was : {correct_random_number}")
    input("Press Enter to continue...")


def game():
    clear()
    print("============================ Guess a number ============================")
    print(
        f"You have {settings["attempts_count"]} attempts to guess the number in range from {settings["random_number_range_1"]} to {settings["random_number_range_2"]}."
    )
    ready = input("Are you ready? (y/n) >>>")
    if ready.lower() == "y":
        correct_random_num = random.randint(
            settings["random_number_range_1"], settings["random_number_range_2"]
        )
        current_attempts_amount = settings["attempts_count"]
        spent_attempts_counter = 0
        user_suggestions = []
        system_answers = []
        while True:
            clear()
            if current_attempts_amount != "infinity":
                if current_attempts_amount == 0:
                    game_over(
                        spent_attempts_counter,
                        current_attempts_amount,
                        correct_random_num,
                        user_suggestions,
                        system_answers,
                    )
                    break
            print(
                "============================ Guess a number ============================"
            )
            print(f"{current_attempts_amount} attempts left.")
            print(f"You spent {spent_attempts_counter} attempts so far.")
            print()
            print("Your last suggestions:", end="\n")
            for i in range(len(user_suggestions)):
                print(user_suggestions[i] + ":", end=system_answers[i] + ";\n")
            print()
            user_suggestion = input("Enter your number >>>")
            try:
                user_suggestion = int(user_suggestion)
            except ValueError:
                print("Invalid input. Must be number.")
                input("Press Enter to continue...")
                continue
            if user_suggestion in user_suggestions:
                print("You already tried this number.")
                input("Press Enter to continue...")
                continue
            if user_suggestion == correct_random_num:
                system_answers.append("equal!")
                user_suggestions.append(str(user_suggestion))
                spent_attempts_counter += 1
                winner(
                    spent_attempts_counter,
                    current_attempts_amount,
                    correct_random_num,
                    user_suggestions,
                    system_answers,
                )
                break
            elif user_suggestion < correct_random_num:
                system_answers.append("higher")
                user_suggestions.append(str(user_suggestion))
                spent_attempts_counter += 1
                try:
                    current_attempts_amount -= 1
                except TypeError:
                    pass
                print("Must be higher!")
                input("Press Enter to continue...")
                continue
            else:
                system_answers.append("lower")
                user_suggestions.append(str(user_suggestion))
                spent_attempts_counter += 1
                try:
                    current_attempts_amount -= 1
                except TypeError:
                    pass
                print("Must be lower!")
                input("Press Enter to continue...")
                continue


while True:
    clear()
    print("============================ Guess a number ============================")
    print()
    print("[1] Start game")
    print("[2] Settings")
    print("[3] Exit")
    print("[4] Contact developer")
    choice = input("Enter your choice >>>")
    if choice == "1":
        game()
    if choice == "2":
        settings_menu()
    if choice == "3":
        print("Goodbye!")
        sys.exit(0)
    if choice == "4":
        webbrowser.open("t.me/shukolza", new=2)
