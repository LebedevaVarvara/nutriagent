from typing import Optional

from agent.models import UserProfile


class AppState:
    def __init__(self) -> None:
        self.profile: Optional[UserProfile] = None
        self.norms: dict[str, float] = {}
        self.today_food_kcal: float = 0.0
        self.today_water_ml: float = 0.0

        # Встроенная мини-база продуктов (ккал на 100г)
        self.food_db: dict[str, int] = {
            "яйцо": 70,
            "овсянка": 350,
            "банан": 90,
            "курица": 165,
            "рис": 130,
            "творог": 120,
            "тост": 250,
            "масло": 700,
            "яблоко": 52,
            "хлеб": 265,
            "сыр": 400,
            "картошка": 80,
            "шоколад": 550,
            "вода": 0,
        }

    def set_profile(self, profile: UserProfile) -> None:
        self.profile = profile
        self.norms = profile.calculate_norms()
        # Сбрасываем дневник при смене профиля
        self.today_food_kcal = 0.0
        self.today_water_ml = 0.0
