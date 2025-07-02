# test_habit_logic.py
import pytest
from datetime import date, timedelta
from habit_logic import Habit, HabitTracker

TODAY = date(2025, 6, 9)
YESTERDAY = TODAY - timedelta(days=1)
DAY_BEFORE = YESTERDAY - timedelta(days=1)

# Testes de Criação e Gestão de Hábitos
def test_add_new_habit():
    tracker = HabitTracker()
    assert tracker.add_habit("Ler livro")
    assert len(tracker.habits) == 1
    assert tracker.habits[0].name == "Ler livro"

def test_add_duplicate_habit_fails():
    tracker = HabitTracker()
    tracker.add_habit("Beber água")
    assert not tracker.add_habit("Beber água")
    assert len(tracker.habits) == 1

def test_delete_habit():
    tracker = HabitTracker()
    tracker.add_habit("Correr")
    tracker.delete_habit("Correr")
    assert len(tracker.habits) == 0

def test_delete_nonexistent_habit():
    tracker = HabitTracker()
    tracker.add_habit("Correr")
    tracker.delete_habit("Nadar")
    assert len(tracker.habits) == 1

def test_get_habit_by_name():
    tracker = HabitTracker()
    tracker.add_habit("Meditar")
    habit = tracker.get_habit("Meditar")
    assert habit is not None
    assert habit.name == "Meditar"

# Testes de Conclusão de Hábitos
def test_mark_habit_complete():
    tracker = HabitTracker()
    tracker.add_habit("Estudar")
    tracker.mark_complete("Estudar", TODAY)
    assert tracker.is_complete_today("Estudar", TODAY)

def test_mark_and_unmark_habit():
    tracker = HabitTracker()
    tracker.add_habit("Limpar")
    tracker.mark_complete("Limpar", TODAY)
    assert tracker.is_complete_today("Limpar", TODAY)
    tracker.mark_incomplete("Limpar", TODAY)
    assert not tracker.is_complete_today("Limpar", TODAY)

def test_is_complete_on_different_days():
    tracker = HabitTracker()
    tracker.add_habit("Alongar")
    tracker.mark_complete("Alongar", YESTERDAY)
    assert not tracker.is_complete_today("Alongar", TODAY)
    assert tracker.get_habit("Alongar").completions == {YESTERDAY}

def test_completing_nonexistent_habit():
    tracker = HabitTracker()
    tracker.mark_complete("Inexistente", TODAY)
    assert tracker.get_habit("Inexistente") is None

# Testes da Lógica de Sequência (Streak)
def test_streak_shows_previous_day_streak_if_not_done_today():
    tracker = HabitTracker()
    tracker.add_habit("Escrever")
    tracker.mark_complete("Escrever", YESTERDAY)
    tracker.mark_complete("Escrever", DAY_BEFORE)
    assert tracker.get_current_streak("Escrever", TODAY) == 2

def test_streak_is_zero_if_not_done_today_and_no_streak_yesterday():
    tracker = HabitTracker()
    tracker.add_habit("Desenhar")
    tracker.mark_complete("Desenhar", DAY_BEFORE)
    assert tracker.get_current_streak("Desenhar", TODAY) == 0

def test_streak_is_one_if_done_only_today():
    tracker = HabitTracker()
    tracker.add_habit("Pintar")
    tracker.mark_complete("Pintar", TODAY)
    tracker.mark_complete("Pintar", DAY_BEFORE) 
    assert tracker.get_current_streak("Pintar", TODAY) == 1

def test_correctly_calculates_streak_of_three_when_done_today():
    tracker = HabitTracker()
    tracker.add_habit("Caminhar")
    tracker.mark_complete("Caminhar", TODAY)
    tracker.mark_complete("Caminhar", YESTERDAY)
    tracker.mark_complete("Caminhar", DAY_BEFORE)
    assert tracker.get_current_streak("Caminhar", TODAY) == 3

def test_streak_is_zero_for_new_habit_not_done_today():
    tracker = HabitTracker()
    tracker.add_habit("Organizar")
    # Não foi feito hoje, e é novo, então streak de ontem é 0.
    assert tracker.get_current_streak("Organizar", TODAY) == 0

def test_streak_for_nonexistent_habit_is_zero():
    tracker = HabitTracker()
    assert tracker.get_current_streak("Inexistente", TODAY) == 0

def test_streak_across_month_boundary_when_done_today():
    tracker = HabitTracker()
    tracker.add_habit("Yoga")
    last_of_may = date(2025, 5, 31)
    first_of_june = date(2025, 6, 1)
    tracker.mark_complete("Yoga", first_of_june)
    tracker.mark_complete("Yoga", last_of_may)
    assert tracker.get_current_streak("Yoga", first_of_june) == 2

def test_streak_across_month_boundary_not_done_today():
    tracker = HabitTracker()
    tracker.add_habit("Meditar")
    day_before_last_of_may = date(2025, 5, 30)
    last_of_may = date(2025, 5, 31)
    first_of_june = date(2025, 6, 1)

    tracker.mark_complete("Meditar", last_of_may)
    tracker.mark_complete("Meditar", day_before_last_of_may)
    assert tracker.get_current_streak("Meditar", first_of_june) == 2

def test_invalid_habit_name_value_raises_error():
    with pytest.raises(ValueError):
        Habit(name="")