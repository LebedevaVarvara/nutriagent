from dataclasses import dataclass


@dataclass
class UserProfile:
    sex: str
    age: int
    weight: float
    height: float
    activity: str

    def calculate_norms(self) -> dict[str, float]:
        # Формула Миффлина - Сан Жеора
        base = (10 * self.weight) + (6.25 * self.height) - (5 * self.age)

        is_male = self.sex.lower() in ["м", "муж", "мужской", "male"]
        calories = base + 5 if is_male else base - 161

        activity_map = {
            "низкая": 1.2,
            "min": 1.2,
            "средняя": 1.55,
            "med": 1.55,
            "высокая": 1.725,
            "max": 1.725,
        }
        multiplier = activity_map.get(self.activity.lower(), 1.2)
        total_calories = calories * multiplier

        # Распределение БЖУ (30% белки, 30% жиры, 40% углеводы)
        proteins = (total_calories * 0.3) / 4
        fats = (total_calories * 0.3) / 9
        carbs = (total_calories * 0.4) / 4

        # Вода: 30 мл на кг веса
        water_ml = self.weight * 30

        return {
            "calories": round(total_calories),
            "proteins": round(proteins, 1),
            "fats": round(fats, 1),
            "carbs": round(carbs, 1),
            "water": round(water_ml),
        }
