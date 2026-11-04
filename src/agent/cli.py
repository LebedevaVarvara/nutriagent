import shlex
from typing import Callable

from agent import logic
from agent.storage import AppState

Handler = Callable[[AppState, list[str]], str]


def run_agent() -> None:
    state = AppState()

    commands: dict[str, tuple[Handler, str, str]] = {
        "profile": (
            logic.op_set_profile,
            "profile <пол> <возраст> <вес> <рост> <активность>",
            "Настроить профиль",
        ),
        "eat": (logic.op_eat, "eat <продукт> <граммы>", "Записать прием пищи"),
        "water": (logic.op_water, "water <мл>", "Записать воду"),
        "status": (logic.op_status, "status", "Показать прогресс за день"),
    }

    print("🥗 Добро пожаловать в NutriAgent!")
    print("Введите 'help' для списка команд или 'exit' для выхода.\n")

    while True:
        try:
            raw_input = input("nutri> ").strip()
        except (EOFError, KeyboardInterrupt):
            print("\nДо встречи!")
            break

        if not raw_input:
            continue

        try:
            parts = shlex.split(raw_input)
        except ValueError:
            print("Ошибка: неверный формат ввода (проверьте кавычки).")
            continue

        cmd, args = parts[0].lower(), parts[1:]

        if cmd in ["exit", "quit"]:
            print("До встречи!")
            break

        if cmd == "help":
            print("\nДоступные команды:")
            for _, usage, desc in commands.items():
                print(f"  {usage:<40} - {desc}")
            print(f"  {'help':<40} - Показать эту справку")
            print(f"  {'exit':<40} - Выйти из программы\n")
            continue

        if cmd not in commands:
            print(f"Ошибка: неизвестная команда '{cmd}'. Введите 'help'.")
            continue

        handler = commands[cmd][0]
        try:
            result = handler(state, args)
            print(result)
        except ValueError as e:
            print(f"Ошибка: {e}")
