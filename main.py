import subprocess
import sys

try:
    from secret import dev_code
    from getpass import getpass
except ModuleNotFoundError:
    dev_code = ""

try:
    import webbrowser
    import json
    import random
    import colorama
    import os
    import pygame
except ModuleNotFoundError as exception:
    print(
        f"Unable to import requirements. Error : {exception} \nTrying auto-install..."
    )
    command = [sys.executable, "-m", "pip", "install", "-r", "requirements.txt"]

    try:
        result = subprocess.run(
            command, check=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE
        )

        print("Dependencies installed successfully.")

        import webbrowser
        import sys
        import json
        import random
        import colorama
        import pygame

        print("All modules imported successfully.")
        input("Press Enter to continue...")
    except subprocess.CalledProcessError as e:
        print("Failed to install dependencies.")
        print(f"Error details:\n{e.stderr.decode('utf-8')}")
        sys.exit(1)


def resource_path(relative_path):
    """Get a correct file path for compiled EXE"""
    try:
        # Temp folder PyInstaller
        base_path = sys._MEIPASS  # type: ignore
    except AttributeError:
        # Standard mode (launched via Python)
        base_path = os.path.dirname(os.path.abspath(__file__))
    return os.path.join(base_path, relative_path)


with open(resource_path("hiscore.txt"), "r") as file:
    high_score = float(file.read())

with open(resource_path("settings.json"), "r") as file:
    settings = json.load(file)

developer_mode = False
colorama.init(autoreset=True)
pygame.mixer.init()

error_sound = pygame.mixer.Sound("sound/error.mp3")
choose_sound = pygame.mixer.Sound("sound/choose.mp3")


def clear():
    """Generate command to clear screen depends on os type"""
    os.system("cls" if os.name == "nt" else "clear")


def calculate_score(min_num, max_num, spent_attempts, attempts_amount):
    """Calculate score with anti-cheat measures"""
    range_size = max_num - min_num + 1
    base_score = (range_size**0.5) / spent_attempts

    # Anti-cheat measures
    if range_size < 10:
        return 0.0  # Block too easy
    if spent_attempts == 1 and range_size == 2:
        return 1.0

    # Main logic
    if attempts_amount != "infinity":
        if spent_attempts <= attempts_amount * 0.5:
            bonus = 1.2
        else:
            bonus = 1.0
    else:
        if spent_attempts > 10:
            penalty = 0.5
        else:
            penalty = 1.0
        bonus = penalty

    final_score = base_score * bonus
    return round(final_score, 2)


def rainbow_text(text):
    """Get rainbow text"""
    colors = [
        colorama.Fore.RED,
        colorama.Fore.YELLOW,
        colorama.Fore.GREEN,
        colorama.Fore.CYAN,
        colorama.Fore.BLUE,
        colorama.Fore.MAGENTA,
    ]

    result = ""
    for i, char in enumerate(text):
        color = colors[i % len(colors)]
        result += f"{color}{char}"

    return result + colorama.Style.RESET_ALL


def color_text(text, color):
    """
    Returns colored text

    :param text: String that needs to be colored
    :param color: Color name ('red', 'blue', 'green', etc.)
    :return: Colored text
    """

    color_map = {
        "red": colorama.Fore.RED,
        "green": colorama.Fore.GREEN,
        "yellow": colorama.Fore.YELLOW,
        "blue": colorama.Fore.BLUE,
        "magenta": colorama.Fore.MAGENTA,
        "cyan": colorama.Fore.CYAN,
        "white": colorama.Fore.WHITE,
        "black": colorama.Fore.BLACK,
        "reset": colorama.Fore.RESET,  # Color reset
    }

    selected_color = color_map.get(color.lower(), colorama.Fore.RESET)

    return f"{selected_color}{text}{colorama.Style.RESET_ALL}"


def settings_menu():
    while True:
        clear()
        print(
            rainbow_text(
                "============================ Settings Menu ============================"
            )
        )
        print()
        print("[1] Set attempts count")
        print("[2] Set random number range")
        print("[3] Hints")
        print("[4] Back to main menu")
        choice = input("Your choice >>>")
        if choice == "1":
            choose_sound.play()
            print()
            attempts = input('Enter attempts count or "infinity" >>>')
            try:
                settings["attempts_count"] = int(attempts)
            except ValueError:
                if attempts.lower() == "infinity":
                    settings["attempts_count"] = "infinity"
                    with open(resource_path("settings.json"), "w") as file:
                        json.dump(settings, file)
                    input("Success! Press Enter to continue...")
                    continue
                error_sound.play()
                print("Invalid input. Must be a number.")
                input("Press Enter to continue...")
                continue

            with open(resource_path("settings.json"), "w") as file:
                json.dump(settings, file)
            input("Success! Press Enter to continue...")
        if choice == "2":
            choose_sound.play()
            print()
            min_num = input("Enter min number (inclusive) >>>")
            max_num = input("Enter max number (inclusive) >>>")
            try:
                min_num = int(min_num)
                max_num = int(max_num)
                if max_num <= min_num:
                    error_sound.play()
                    print("Invalid input: max number must be greater than min number.")
                    input("Press Enter to continue...")
                    continue

                settings["random_number_range_1"] = int(min_num)
                settings["random_number_range_2"] = int(max_num)

                with open(resource_path("settings.json"), "w") as file:
                    json.dump(settings, file)
                input("Success! Press Enter to continue...")
                continue
            except ValueError:
                error_sound.play()
                print("Invalid input. Must be number.")
                input("Press Enter to continue...")
                continue
        if choice == "3":
            choose_sound.play()
            print()
            print("[1] Enable hints")
            print("[2] Disable hints")
            choice = input("Enter your choice >>>")
            if choice == "1":
                choose_sound.play()
                settings["hints_enabled"] = True
                with open(resource_path("settings.json"), "w") as file:
                    json.dump(settings, file)
                input("Success! Press Enter to continue...")
            if choice == "2":
                choose_sound.play()
                settings["hints_enabled"] = False
                with open(resource_path("settings.json"), "w") as file:
                    json.dump(settings, file)
                input("Success! Press Enter to continue...")
            else:
                error_sound.play()
                input("Invalid input. Press Enter to continue...")
        if choice == "4":
            choose_sound.play()
            break


def game_over(
    spent_attempts: int,
    attempts_amount: int,
    correct_random_number: int,
    user_suggestions: list,
    system_answers: list,
):
    clear()
    print(
        color_text(
            "============================ GAME OVER ============================", "red"
        )
    )
    print()
    print(f"Spent attempts: {spent_attempts}")
    print(f"Total attempts: {attempts_amount}")
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


def winner(
    spent_attempts: int,
    attempts_amount,
    correct_random_number: int,
    user_suggestions: list,
    system_answers: list,
    number_range: list,
):
    global high_score
    score = calculate_score(
        number_range[0], number_range[1], spent_attempts, attempts_amount
    )

    clear()
    print(
        color_text(
            "============================ YOU WON ============================", "green"
        )
    )
    print()
    print(f"Spent attempts: {spent_attempts} / {attempts_amount}")
    print(f"Your score: {score}")
    if score > high_score:
        high_score = score
        print(f"NEW HIGH SCORE!")
        with open(resource_path("hiscore.txt"), "w") as file:
            file.write(str(high_score))
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
    with open("settings.json", 'r') as file:
        settings = json.load(file)
    clear()
    print(
        rainbow_text(
            "============================ Guess a number ============================"
        )
    )
    print()
    print(
        f"You have {settings["attempts_count"]} attempts to guess the number in range from {settings["random_number_range_1"]} to {settings["random_number_range_2"]}."
    )
    ready = input("Are you ready? (y/n) >>>")
    if ready.lower() == "y":
        correct_random_num = random.randint(
            settings["random_number_range_1"], settings["random_number_range_2"]
        )
        current_attempts_amount = settings["attempts_count"]
        attempts_amount_counter = current_attempts_amount
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
                rainbow_text(
                    "============================ Guess a number ============================"
                )
            )
            print()
            if developer_mode:
                print(
                    "Welcome, developer. Here is all current game variables you may need:"
                )
                print("Correct answer :", correct_random_num)
                print()
            print(f"{attempts_amount_counter} attempts left.")
            print(f"You spent {spent_attempts_counter} attempts so far.")
            print()
            if settings["hints_enabled"]:
                print("Your last suggestions:", end="\n")
                for i in range(len(user_suggestions)):
                    print(user_suggestions[i] + ":", end=system_answers[i] + ";\n")
                print()
            user_suggestion = input("Enter your number >>>")
            try:
                user_suggestion = int(user_suggestion)
            except ValueError:
                error_sound.play()
                print("Invalid input. Must be number.")
                input("Press Enter to continue...")
                continue
            if user_suggestion in user_suggestions:
                error_sound.play()
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
                    [
                        settings["random_number_range_1"],
                        settings["random_number_range_2"],
                    ],
                )
                break
            elif user_suggestion < correct_random_num:
                system_answers.append("higher")
                user_suggestions.append(str(user_suggestion))
                spent_attempts_counter += 1
                try:
                    attempts_amount_counter -= 1
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
                    attempts_amount_counter -= 1
                except TypeError:
                    pass
                print("Must be lower!")
                input("Press Enter to continue...")
                continue


while True:
    clear()
    print(
        rainbow_text(
            "============================ Guess a number ============================"
        )
    )
    print()
    if developer_mode:
        print("Welcome, developer!")
    print("[1] Start game")
    print("[2] Settings")
    print("[3] Exit")
    print("[4] Contact developer")
    choice = input("Enter your choice >>>")
    if choice == "1":
        choose_sound.play()
        game()
    if choice == "2":
        choose_sound.play()
        settings_menu()
    if choice == "3":
        choose_sound.play()
        print("Goodbye!")
        sys.exit(0)
    if choice == "4":
        choose_sound.play()
        clear()
        print("[1] Contact developer")
        print("[2] Enable developer mode")
        print("[3] Return to main menu")
        choice = input("Enter your choice >>>")
        if choice == "1":
            choose_sound.play()
            webbrowser.open("t.me/shukolza", new=2)
        elif choice == "2":
            choose_sound.play()
            if dev_code:
                code = getpass("Enter developer code >>>")  # type: ignore
                if code == dev_code:
                    choose_sound.play()
                    developer_mode = True
                    print("Welcome, developer!")
                    input("Press Enter to continue...")
                else:
                    error_sound.play()
                    print("Incorrect developer code!")
                    input("Press Enter to continue")
            else:
                error_sound.play()
                print("Seems like you shouldn't be here...")
                input("Press Enter to continue...")
        elif choice == "3":
            choose_sound.play()
