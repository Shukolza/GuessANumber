import webbrowser
import sys
import os
import json
import random

with open("hiscore.txt") as file:
    high_score = int(file.read())

with open("settings.json", "r") as file:
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
    pass  # Todo


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
                    # game_over() ToDo!
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
                # winner() ToDo!
                break
            elif user_suggestion < correct_random_num:
                system_answers.append("higher")
                user_suggestions.append(user_suggestion)
                spent_attempts_counter += 1
                current_attempts_amount -= 1
                print("Must be higher!")
                input("Press Enter to continue...")
                continue
            else:
                system_answers.append("lower")
                user_suggestions.append(user_suggestion)
                spent_attempts_counter += 1
                current_attempts_amount -= 1
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
    if choice == "2":
        settings_menu()
    if choice == "3":
        print("Goodbye!")
        sys.exit(0)
    if choice == "4":
        webbrowser.open("t.me/shukolza", new=2)
