# GuessANumber

A simple game where the goal is to guess a random number.

## Table of Contents

- [Description](#description)
- [Features](#features)
- [Installation](#installation)
- [Usage](#usage)
- [Settings](#settings)
- [Contributing](#contributing)
- [Contact](#contact)

---

## Description

GuessANumber is a console-based game where the player tries to guess a randomly generated number within a specified range. The game provides hints ("higher" or "lower") to guide the player toward the correct answer. Players can customize the game settings, such as the number of attempts, range of random numbers and enabling hints.

---

## Features

- **Customizable Settings**: Adjust the number of attempts, the range of random numbers and more.
- **High Score Tracking**: The game tracks the highest score achieved by players.
- **User-Friendly Interface**: Simple and intuitive console-based interface.
- **Cross-Platform Support**: Works on any platform with, or without Python installed.

---

## Installation

---

### Installation (source code) python needed

1. **Clone the Repository**:

   ``` bash
   git clone https://github.com/shukolza/GuessANumber.git
   cd GuessANumber
   ```

2. **Install Dependencies**:
   Ensure you have Python 3.10 or higher installed. Then, install the required dependencies:

   ``` bash
   pip install -r requirements.txt
   ```

3. **Run the Game**:
   Execute the main script to start the game:

   ``` bash
   python main.py
   ```

---

### Installation (ready-to-use compiled EXE) doesn't need python installed

1. **Go to latest release, open 'assets' and download compiled.exe**:
   [Releases link](https://github.com/Shukolza/GuessANumber/releases)

2. Open it! 🎉🎉🎉

---

## Usage

### Main Menu

Upon starting the game, you will see the following options:

``` output
============================ Guess a number ============================

[1] Start game
[2] Settings
[3] Exit
[4] Contact developer
```

- **Start Game**: Begin a new game session.
- **Settings**: Customize game parameters (e.g., number of attempts, random number range).
- **Exit**: Close the game.
- **Contact Developer**: Open a link to contact the developer.

### Gameplay

1. The game generates a random number within the specified range.
2. You are prompted to guess the number.
3. After each guess, the game provides feedback:
   - "Higher": Your guess is too low.
   - "Lower": Your guess is too high.
4. The game ends when you guess the correct number or run out of attempts.

---

## Settings

**You can also adjust these settings through the in-game settings menu.**

The game settings are stored in the `settings.json` file. You can modify the following parameters:

- **Attempts Count**: Set the number of attempts allowed (`attempts_count`). Use `"infinity"` for unlimited attempts.
- **Random Number Range**: Define the range of random numbers (`random_number_range_1` and `random_number_range_2`).

Example `settings.json`:

``` JSON
{
    "attempts_count": "infinity",
    "random_number_range_1": 1,
    "random_number_range_2": 100,
    "hints_enabled": false
}
```

---

## Contributing

Contributions are welcome! If you'd like to contribute to the project, follow these steps:

1. Fork the repository.
2. Create a new branch for your feature or bug fix:

   ``` bash
   git checkout -b feature-name
   ```

3. Commit your changes:

   ``` bash
   git commit -m "Add feature or fix"
   ```

4. Push to your fork:

   ``` bash
   git push origin feature-name
   ```

5. Open a pull request on GitHub.

---

## Contact

If you have any questions or suggestions, feel free to reach out:

- **Telegram**: [@shukolza](https://t.me/shukolza)
- **GitHub**: [shukolza](https://github.com/shukolza)
- **Email**: [shukolza@gmail.com](shukolza@gmail.com)

---

## Additional Notes

- The `.gitignore` file ensures that unnecessary files (e.g., `__pycache__`, environment files) are not tracked by Git.
- The `python-app.yml` workflow automates testing and packaging for the project. It includes steps for code formatting, dependency installation, and creating a distributable archive.
