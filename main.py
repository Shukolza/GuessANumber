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
    print(f"Библиотеки не обнаружены. Ошибка: {exception} \nЗапускаю автоустановку...")
    command = [sys.executable, "-m", "pip", "install", "-r", "requirements.txt"]

    try:
        result = subprocess.run(
            command, check=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE
        )

        print("Зависимости успешно установлены")

        import webbrowser
        import sys
        import json
        import random
        import colorama
        import pygame

        print("Все модули успешно импортированы")
        input("Нажмите Enter, чтобы продолжить...")
    except subprocess.CalledProcessError as e:
        print("Не удалось установить зависимости(")
        print(
            "Попробуйте вручную запустить команду: \n pip install -r requirements.txt"
        )
        print(f"Детали ошибки:\n{e.stderr.decode('utf-8')}")
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
    if attempts_amount != "бесконечность":
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
                "============================ Меню настроек ============================"
            )
        )
        print()
        print("[1] Установить количество попыток")
        print("[2] Установить границы случайного числа")
        print("[3] Подсказки")
        print("[4] Вернуться в главное меню")
        choice = input("Ваш выбор >>>")
        if choice == "1":
            choose_sound.play()
            print()
            attempts = input(
                'Введите кол-во попыток или "бесконечность" >>>'
            )  # TODO - infinity -> бесконечность
            try:
                settings["attempts_count"] = int(attempts)
            except ValueError:
                if attempts.lower() == "бесконечность":
                    settings["attempts_count"] = "бесконечность"
                    with open(resource_path("settings.json"), "w") as file:
                        json.dump(settings, file)
                    input("Успех! Нажмите Enter, чтобы продолжить...")
                    continue
                error_sound.play()
                print("Неправильный ввод. Нужно ввести число")
                input("Нажмите Enter чтобы продолжить...")
                continue

            with open(resource_path("settings.json"), "w") as file:
                json.dump(settings, file)
            input("Успех! Нажмите Enter, чтобы продолжить...")
        if choice == "2":
            choose_sound.play()
            print()
            min_num = input("Введите нижнюю границу (включительно) >>>")
            max_num = input("Введите верхнюю границу (включительно) >>>")
            try:
                min_num = int(min_num)
                max_num = int(max_num)
                if max_num <= min_num:
                    error_sound.play()
                    print(
                        "Неправильный ввод. Нижняя граница должна быть меньше верхней."
                    )
                    input("Нажмите Enter чтобы продолжить...")
                    continue

                settings["random_number_range_1"] = int(min_num)
                settings["random_number_range_2"] = int(max_num)

                with open(resource_path("settings.json"), "w") as file:
                    json.dump(settings, file)
                input("Успех! Нажмите Enter, чтобы продолжить...")
                continue
            except ValueError:
                error_sound.play()
                print("Неправильный ввод. Нужно ввести число.")
                input("Нажмите Enter чтобы продолжить...")
                continue
        if choice == "3":
            choose_sound.play()
            print()
            print("[1] Включить подсказки")
            print("[2] Выключить подсказки")
            choice = input("Введите ваш выбор >>>")
            if choice == "1":
                choose_sound.play()
                settings["hints_enabled"] = True
                with open(resource_path("settings.json"), "w") as file:
                    json.dump(settings, file)
                input("Успех! Нажмите Enter, чтобы продолжить...")
            if choice == "2":
                choose_sound.play()
                settings["hints_enabled"] = False
                with open(resource_path("settings.json"), "w") as file:
                    json.dump(settings, file)
                input("Успех! Нажмите Enter, чтобы продолжить...")
            else:
                error_sound.play()
                input("Неправильный ввод. Нажмите Enter чтобы продолжить...")
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
            "============================ ИГРА ОКОНЧЕНА ============================",
            "red",
        )
    )
    print()
    print(f"Потраченные попытки: {spent_attempts}")
    print(f"Всего попыток: {attempts_amount}")
    print("Ваши предположения:")
    tmp_counter = 1
    for suggestion in range(len(user_suggestions)):
        print(
            f"[{tmp_counter}] {user_suggestions[suggestion]} : {system_answers[suggestion]}"
        )
        tmp_counter += 1
    print()
    print(f"Правильный ответ: {correct_random_number}")
    input("Нажмите Enter, чтобы продолжить")


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
            "============================ ВЫ ВЫИГРАЛИ ============================",
            "green",
        )
    )
    print()
    print(f"Потрачено попыток: {spent_attempts} / {attempts_amount}")
    print(f"Счет: {score}")
    if score > high_score:
        high_score = score
        print(f"НОВЫЙ РЕКОРД!")
        with open(resource_path("hiscore.txt"), "w") as file:
            file.write(str(high_score))
    print("Ваши предположения:")
    tmp_counter = 1
    for suggestion in range(len(user_suggestions)):
        print(
            f"[{tmp_counter}] {user_suggestions[suggestion]} : {system_answers[suggestion]}"
        )
        tmp_counter += 1
    print()
    print(f"Правильный ответ был: {correct_random_number}")
    input("Нажмите Enter, чтобы продолжить")


def game():
    with open("settings.json", "r") as file:
        settings = json.load(file)
    clear()
    print(
        rainbow_text(
            "============================ Угадай число ============================"
        )
    )
    print()
    print(
        f"У тебя есть {settings["attempts_count"]} попыток чтобы угадать число в диапазоне от {settings["random_number_range_1"]} до {settings["random_number_range_2"]}."
    )
    ready = input("Вы готовы? (Д/Н) >>>")
    if ready.lower() == "д":
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
            if current_attempts_amount != "бесконечность":
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
                    "============================ Угадай число ============================"
                )
            )
            print()
            if developer_mode:
                print(
                    "Welcome, developer. Here is all current game variables you may need:"
                )
                print("Correct answer :", correct_random_num)
                print()
            print(f"Попыток осталось: {attempts_amount_counter}.")
            print(f"Вы потратили {spent_attempts_counter} попыток.")
            print()
            if settings["hints_enabled"]:
                print("Ваши предыдущие предположения:", end="\n")
                for i in range(len(user_suggestions)):
                    print(user_suggestions[i] + ":", end=system_answers[i] + ";\n")
                print()
            user_suggestion = input("Введите число >>>")
            try:
                user_suggestion = int(user_suggestion)
            except ValueError:
                error_sound.play()
                print("Неправильный ввод. Должно быть числом.")
                input("Нажмите Enter, чтобы продолжить")
                continue
            if user_suggestion in user_suggestions:
                error_sound.play()
                print("Вы уже пробовали это число.")
                input("Нажмите Enter, чтобы продолжить")
                continue
            if user_suggestion == correct_random_num:
                system_answers.append("равно!")
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
                system_answers.append("больше")
                user_suggestions.append(str(user_suggestion))
                spent_attempts_counter += 1
                try:
                    attempts_amount_counter -= 1
                except TypeError:
                    pass
                print("Больше!")
                input("Нажмите enter, чтобы продолжить")
                continue
            else:
                system_answers.append("меньше")
                user_suggestions.append(str(user_suggestion))
                spent_attempts_counter += 1
                try:
                    attempts_amount_counter -= 1
                except TypeError:
                    pass
                print("Меньше!")
                input("Нажмите enter, чтобы продолжить")
                continue


while True:
    clear()
    print(
        rainbow_text(
            "============================ Угадай число ============================"
        )
    )
    print()
    if developer_mode:
        print("Welcome, developer!")
    print("[1] Начать игру")
    print("[2] Настройки")
    print("[3] Выход")
    print("[4] Связаться с разработчиком")
    choice = input("Введите ваш выбор >>>")
    if choice == "1":
        choose_sound.play()
        game()
    if choice == "2":
        choose_sound.play()
        settings_menu()
    if choice == "3":
        choose_sound.play()
        print("До свидания!")
        sys.exit(0)
    if choice == "4":
        choose_sound.play()
        clear()
        print("[1] Связаться с разработчиком")
        print("[2] Enable developer mode")
        print("[3] Вернуться в главное меню")
        choice = input("Введите ваш выбор >>>")
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
