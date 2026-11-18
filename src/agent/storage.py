import json
from dataclasses import asdict
from pathlib import Path
from typing import Optional

from agent.models import UserProfile


class AppState:
    def __init__(self, filepath: str = "state.json") -> None:
        self.filepath = Path(filepath)
        self.profile: Optional[UserProfile] = None
        self.norms: dict[str, float] = {}
        self.today_food_kcal: float = 0.0
        self.today_water_ml: float = 0.0

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

        # Пытаемся загрузить состояние при старте
        self.load()

    def set_profile(self, profile: UserProfile) -> None:
        self.profile = profile
        self.norms = profile.calculate_norms()
        self.today_food_kcal = 0.0
        self.today_water_ml = 0.0

    def save(self) -> None:
        """Сохраняет текущее состояние в файл."""
        data = {
            "profile": asdict(self.profile) if self.profile else None,
            "today_food_kcal": self.today_food_kcal,
            "today_water_ml": self.today_water_ml,
        }
        try:
            with open(self.filepath, "w", encoding="utf-8") as f:
                json.dump(data, f, ensure_ascii=False, indent=4)
        except OSError as e:
            print(f"\n[Ошибка] Не удалось сохранить данные: {e}")

    def load(self) -> None:
        """Загружает состояние из файла, если он существует."""
        if not self.filepath.exists():
            return  # Первый запуск, файла нет

        try:
            with open(self.filepath, encoding="utf-8") as f:
                data = json.load(f)

            if data.get("profile"):
                self.profile = UserProfile(**data["profile"])
                self.norms = self.profile.calculate_norms()

            self.today_food_kcal = data.get("today_food_kcal", 0.0)
            self.today_water_ml = data.get("today_water_ml", 0.0)

        except (OSError, json.JSONDecodeError, TypeError, KeyError) as e:
            print(f"\n[Ошибка] Файл состояния поврежден ({e}). Начинаем с пустого состояния.")
            self.profile = None
            self.norms = {}
            self.today_food_kcal = 0.0
            self.today_water_ml = 0.0
