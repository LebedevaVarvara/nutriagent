from agent.storage import AppState


def op_set_profile(state: AppState, args: list[str]) -> str:
    # Ожидаем: profile пол возраст вес рост активность
    if len(args) != 5:
        raise ValueError("Формат: profile <пол> <возраст> <вес_кг> <рост_см> <активность>")
    try:
        sex, age, weight, height, activity = args
        from agent.models import UserProfile

        profile = UserProfile(
            sex=sex, age=int(age), weight=float(weight), height=float(height), activity=activity
        )
        state.set_profile(profile)
        n = state.norms
        return (
            f"Профиль сохранен!\nВаша норма: {n['calories']} ккал, "
            f"Б: {n['proteins']}г, Ж: {n['fats']}г, У: {n['carbs']}г. "
            f"Вода: {n['water']} мл."
        )
    except ValueError:
        raise ValueError("Возраст, вес и рост должны быть числами.") from None


def op_eat(state: AppState, args: list[str]) -> str:
    # Ожидаем: eat <продукт> <граммы>
    if not state.profile:
        raise ValueError("Сначала настройте профиль командой 'profile'.")
    if len(args) != 2:
        raise ValueError("Формат: eat <продукт> <граммы>")

    food_name = args[0].lower()
    try:
        grams = float(args[1])
    except ValueError:
        raise ValueError("Граммы должны быть числом.") from None

    if food_name not in state.food_db:
        raise ValueError(
            f"Продукт '{food_name}' не найден. Доступны: {', '.join(state.food_db.keys())}"
        )

    kcal_per_100g = state.food_db[food_name]
    eaten_kcal = (kcal_per_100g / 100) * grams
    state.today_food_kcal += eaten_kcal

    remain = state.norms["calories"] - state.today_food_kcal
    return (
        f"Записано: {food_name} ({grams}г) = {round(eaten_kcal)} ккал. "
        f"Съедено за день: {round(state.today_food_kcal)} ккал. "
        f"Осталось: {round(remain)} ккал."
    )


def op_water(state: AppState, args: list[str]) -> str:
    # Ожидаем: water <мл>
    if not state.profile:
        raise ValueError("Сначала настройте профиль командой 'profile'.")
    if len(args) != 1:
        raise ValueError("Формат: water <миллилитры>")

    try:
        ml = float(args[0])
    except ValueError:
        raise ValueError("Миллилитры должны быть числом.") from None

    state.today_water_ml += ml
    remain = state.norms["water"] - state.today_water_ml
    if remain > 0:
        return (
            f"Выпито {int(ml)} мл. Всего: {int(state.today_water_ml)} мл "
            f"из {int(state.norms['water'])} мл. Осталось: {int(remain)} мл."
        )
    return (
        f"Выпито {int(ml)} мл. Всего: {int(state.today_water_ml)} мл. Вы выполнили норму воды! 🎉"
    )


def op_status(state: AppState, args: list[str]) -> str:
    if not state.profile:
        return "Профиль не настроен. Используйте команду 'profile'."
    n = state.norms
    return (
        f"--- Статус на сегодня ---\n"
        f"Калории: съедено {round(state.today_food_kcal)} / {n['calories']} ккал\n"
        f"Вода: выпито {int(state.today_water_ml)} / {int(n['water'])} мл"
    )
