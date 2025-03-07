# Угадай число

Простая игра, цель - угадать случайное число.

## Оглавление

- [Описание](#описание)
- [Возможности](#возможности)
- [Установка](#установка)
- [Использование](#использование)
- [Настройки](#настройки)
- [Связаться](#связаться)

---

## Описание

Угадай число это консольная игра, где игрок пытается угадать случайно сгенерированное число в заданном диапазоне. Игра дает подсказки ("больше" или "меньше") чтобы
помочь игроку угадать правильный ответ. Игрок может настраивать игровые параметры такие как кол-во попыток, диапазон случайных чисел и включение подсказок.

---

## Возможности

- **Настройки**: Управляйте количеством попыток, диапазоном случайных чисел и другими параметрами.
- **Система счета**: Игра считает счет по специальной формуле и отслеживает рекорды.
- **Дружелюбный интерфейс**: Простой и интуитивно понятный консольный интерфейс.
- **Кроссплатформенность**: Работает на любых устройствах где установлен (и даже не установлен) Python.

---

## Установка

---

### Установка через исходный код (для проффессионалов) (нужен Python и git)

1. **Клонируйте репозиторий**:

   ``` bash
   git clone https://github.com/shukolza/GuessANumber.git
   cd GuessANumber
   ```

2. **Установите зависимости**:
   Убедитесь, что у вас установлен Python 3.10+. Затем, установите необходимые зависимости:

   ``` bash
   pip install -r requirements.txt
   ```

3. **Запустите игру**:
   Запустите главный скрипт чтобы начать игру:

   ``` bash
   python main.py
   ```

---

### Установка готового скомпилированного EXE. (ДЛЯ НЕ ПРОФФЕССИОНАЛОВ) не требует python или git

1. **Перейдите на страницу последнего релиза, откройте вкладку 'assets' и скачайте файл .exe**:
   [Страница релизов](https://github.com/Shukolza/GuessANumber/releases)

2. **Запустите скачанный файл** 🎉🎉🎉

---

## Использование

### Главное меню

Когда вы запустите игру, Вы увидите следующие опции:

``` output
============================ Угадай число ============================

[1] Начать игру
[2] Настройки
[3] Игры
[4] Связаться с разработчиком
```

- **Начать игру**: Начать игру.
- **Настройки**: Настраивайте игровые праметры (например, кол-во попыток, Диапазон случайного числа).
- **Выход**: Выход из игры.
- **Связаться с разработчиком**: Перейти в телеграм разработчика.

### Игровой процесс

1. Игра генерирует случайное число в заданном диапазоне.
2. Вы вводите свое предположение.
3. После каждой попытки, игра предлагает обратную связь:
   - "Больше": Ваше число ниже загаданного.
   - "Меншьше": Ваше число выше загаданного.
4. Игра заканчивается когда вы угадываете число или у вас заканчиваются попытки.

---

## Настройки

**Вы также можете изменять эти настройки через меню в игре.**

Настройки игры сохранены в файле `settings.json`. Вы можете изменять следующие параметры:

- **Кол-во попыток**: Установите количество попыток (`attempts_count`). Используйте `"infinity"` для бесконечных попыток.
- **Диапазон случайного числа**: Устанавливайте диапазон угадываемого числа (`random_number_range_1` и `random_number_range_2`).

Пример `settings.json` (параметры по умолчанию):

``` JSON
{
    "attempts_count": "infinity",
    "random_number_range_1": 1,
    "random_number_range_2": 100,
    "hints_enabled": false
}
```

---

## Contributing (для проффессионалов, обычным пользователям не нужно)

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

## Связаться

If you have any questions or suggestions, feel free to reach out:

- **Telegram**: [@shukolza](https://t.me/shukolza)
- **GitHub**: [shukolza](https://github.com/shukolza)
- **Email**: [shukolza@gmail.com]

---

## Additional Notes (для проффессионалов)

- The `.gitignore` file ensures that unnecessary files (e.g., `__pycache__`, environment files) are not tracked by Git.
- The `python-app.yml` workflow automates testing and packaging for the project. It includes steps for code formatting, dependency installation, and creating a distributable archive.
