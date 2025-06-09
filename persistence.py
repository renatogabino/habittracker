# persistence.py
import json
from datetime import date
from habit_logic import Habit, HabitTracker

DATA_FILE = "habits_data.json"

def save_data(tracker: HabitTracker):
    """Salva os dados dos hábitos em um arquivo JSON."""
    data_to_save = {
        "habits": [
            {
                "name": habit.name,
                "completions": [d.isoformat() for d in habit.completions]
            }
            for habit in tracker.habits
        ]
    }
    with open(DATA_FILE, "w") as f:
        json.dump(data_to_save, f, indent=2)

def load_data() -> HabitTracker:
    """Carrega os dados dos hábitos do arquivo JSON."""
    tracker = HabitTracker()
    try:
        with open(DATA_FILE, "r") as f:
            data = json.load(f)
            for habit_data in data.get("habits", []):
                completions = {date.fromisoformat(d_str) for d_str in habit_data["completions"]}
                habit = Habit(name=habit_data["name"], completions=completions)
                tracker.habits.append(habit)
    except (FileNotFoundError, json.JSONDecodeError):
        # Se o arquivo não existe ou está corrompido, retorna um tracker vazio
        pass
    return tracker