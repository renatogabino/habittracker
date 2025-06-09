# habit_logic.py
from datetime import date, timedelta

class Habit:
    """Representa um único hábito com seu nome e datas de conclusão."""
    def __init__(self, name: str, completions: set[date] = None):
        if not name:
            raise ValueError("O nome do hábito não pode ser vazio.")
        self.name = name
        self.completions = completions or set()

class HabitTracker:
    """Gerencia uma lista de hábitos e a lógica de negócio."""
    def __init__(self):
        self.habits: list[Habit] = []

    def add_habit(self, name: str) -> bool:
        """Adiciona um novo hábito, se o nome já não existir."""
        if any(h.name == name for h in self.habits):
            return False  # Hábito já existe
        habit = Habit(name)
        self.habits.append(habit)
        return True

    def delete_habit(self, name: str):
        """Remove um hábito da lista."""
        self.habits = [h for h in self.habits if h.name != name]
    
    def get_habit(self, name: str) -> Habit | None:
        """Retorna um objeto de hábito pelo nome."""
        for habit in self.habits:
            if habit.name == name:
                return habit
        return None

    def mark_complete(self, name: str, completion_date: date):
        """Marca um hábito como concluído em uma data específica."""
        habit = self.get_habit(name)
        if habit:
            habit.completions.add(completion_date)

    def mark_incomplete(self, name: str, completion_date: date):
        """Desmarca um hábito em uma data específica."""
        habit = self.get_habit(name)
        if habit and completion_date in habit.completions:
            habit.completions.remove(completion_date)

    def is_complete_today(self, name: str, today: date) -> bool:
        """Verifica se um hábito foi concluído hoje."""
        habit = self.get_habit(name)
        return habit is not None and today in habit.completions

    def get_current_streak(self, name: str, today: date) -> int:
        """
        Calcula a sequência de dias consecutivos de um hábito.
        - Se o hábito foi concluído 'today', a streak inclui 'today'.
        - Se o hábito NÃO foi concluído 'today', a streak mostrada é a do dia anterior.
        """
        habit = self.get_habit(name)
        if not habit:
            return 0

        # Verifica se o hábito foi concluído 'today'
        if today in habit.completions:
            # Hábito concluído hoje, calcula a streak normalmente incluindo hoje
            streak = 0
            current_day_in_streak = today
            while current_day_in_streak in habit.completions:
                streak += 1
                current_day_in_streak -= timedelta(days=1)
            return streak
        else:
            # Hábito NÃO concluído hoje. Calcular a streak que terminava ontem.
            streak_ending_yesterday = 0
            current_day_in_streak = today - timedelta(days=1) # Começa a contagem a partir de ontem
            while current_day_in_streak in habit.completions:
                streak_ending_yesterday += 1
                current_day_in_streak -= timedelta(days=1)
            return streak_ending_yesterday