#описывает структуру данных( профиль )и математику 

from dataclasses import dataclass


@dataclass #характеристики 
class UserProfile:
    sex: str
    age: int
    weight: float
    height: float
    activity: str

    def __post_init__(self): #проверка чисел 
        # 1. СНАЧАЛА проверяем числа (чтобы сразу ловить минусы)
        if self.age <= 0 or self.weight <= 0 or self.height <= 0:
            raise ValueError("Возраст, вес и рост должны быть положительными числами.")

        # 2. ТЕПЕРЬ проверяем пол
        valid_sexes = ["м", "муж", "мужской", "ж", "жен", "женский"]
        if self.sex.strip().lower() not in valid_sexes:
            raise ValueError(f"Недопустимый пол: '{self.sex}'. Введите 'м' или 'ж'.")

        # 3. И в конце активность
        valid_activities = ["низкая", "средняя", "высокая"]
        if self.activity.strip().lower() not in valid_activities:
            # Вот тут мы разбили длинную строку на две
            raise ValueError(
                f"Недопустимая активность: '{self.activity}'. "
                "Введите 'низкая', 'средняя' или 'высокая'."
            )

    def calculate_norms(self) -> dict[str, float]:
        # Шаг 1: Считаем базовый обмен (формула Миффлина-Сан Жеора)
        base = (10 * self.weight) + (6.25 * self.height) - (5 * self.age)
        
        # Шаг 2: Корректируем на пол
        is_male = self.sex.strip().lower() in ["м", "муж", "мужской"]
        calories = base + 5 if is_male else base - 161

        # Шаг 3: Учитываем активность
        activity_map = {
            "низкая": 1.2,
            "средняя": 1.55,
            "высокая": 1.725,
        }
        multiplier = activity_map[self.activity.strip().lower()]
        total_calories = calories * multiplier

        # Шаг 4: Считаем БЖУ (Белки, Жиры, Углеводы)
        proteins = (total_calories * 0.3) / 4
        fats = (total_calories * 0.3) / 9
        carbs = (total_calories * 0.4) / 4
        # Шаг 5: Считаем воду
        water_ml = self.weight * 30
        
        # Шаг 6: Отдаем результат
        return {
            "calories": round(total_calories),
            "proteins": round(proteins, 1),
            "fats": round(fats, 1),
            "carbs": round(carbs, 1),
            "water": round(water_ml),
        }
