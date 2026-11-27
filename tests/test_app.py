import os
import unittest
from pathlib import Path

from agent import logic
from agent.models import UserProfile
from agent.storage import AppState


class TestNutriAgent(unittest.TestCase):
    def setUp(self):
        # Для тестов используем отдельный файл, чтобы не ломать реальные данные
        self.test_file = "test_state.json"
        self.state = AppState(filepath=self.test_file)
        # Очищаем данные перед каждым тестом
        self.state.profile = None
        self.state.norms = {}
        self.state.today_food_kcal = 0.0
        self.state.today_water_ml = 0.0

    def tearDown(self):
        # Удаляем временный файл после теста
        if Path(self.test_file).exists():
            os.remove(self.test_file)

    def test_profile_calculation(self):
        profile = UserProfile(sex="ж", age=25, weight=60, height=165, activity="средняя")
        norms = profile.calculate_norms()
        self.assertEqual(norms["calories"], 2085)
        self.assertEqual(norms["water"], 1800)

    def test_invalid_profile(self):
        with self.assertRaises(ValueError):
            UserProfile(sex="неизвестно", age=25, weight=60, height=165, activity="средняя")
        with self.assertRaises(ValueError):
            UserProfile(sex="ж", age=-25, weight=60, height=165, activity="средняя")

    def test_logic_add_food(self):
        logic.op_set_profile(self.state, ["ж", "25", "60", "165", "средняя"])
        logic.op_eat(self.state, ["яблоко", "100"])
        self.assertAlmostEqual(self.state.today_food_kcal, 52.0)

    def test_logic_invalid_food(self):
        logic.op_set_profile(self.state, ["ж", "25", "60", "165", "средняя"])
        with self.assertRaises(ValueError):
            logic.op_eat(self.state, ["банан", "-100"])
        with self.assertRaises(ValueError):
            logic.op_eat(self.state, ["банан", "inf"])

    def test_save_and_load(self):
        # Настраиваем профиль и добавляем еду
        logic.op_set_profile(self.state, ["ж", "25", "60", "165", "средняя"])
        logic.op_eat(self.state, ["банан", "100"])  # 90 ккал
        logic.op_water(self.state, ["500"])

        # Сохраняем
        self.state.save()

        # Создаем НОВЫЙ объект, который должен загрузить данные с диска
        new_state = AppState(filepath=self.test_file)

        self.assertIsNotNone(new_state.profile)
        self.assertEqual(new_state.profile.weight, 60.0)
        self.assertAlmostEqual(new_state.today_food_kcal, 90.0)
        self.assertAlmostEqual(new_state.today_water_ml, 500.0)


if __name__ == "__main__":
    unittest.main()
