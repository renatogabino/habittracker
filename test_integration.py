# test_integration.py
import os
import json
from datetime import date, timedelta
from habit_logic import HabitTracker
from persistence import save_data, load_data
import app_date_manager

# --- Fixture para gerenciar o ambiente de teste ---
TEST_DATA_FILE = "test_habits_data.json"

def setup_function(function):
    """Executado antes de cada função de teste."""
    import persistence
    persistence.DATA_FILE = "test_habits_data.json"
    if os.path.exists(persistence.DATA_FILE):
        os.remove(persistence.DATA_FILE)
    app_date_manager._today_func = app_date_manager._get_real_today
    app_date_manager.reset_to_today()

def teardown_function(function):
    """Executado após cada função de teste."""
    if os.path.exists(TEST_DATA_FILE):
        os.remove(TEST_DATA_FILE)
    import persistence
    persistence.DATA_FILE = "habits_data.json"
    app_date_manager._today_func = app_date_manager._get_real_today

# --- Testes de Integração ---

def test_save_and_load_integration():
    """
    Testa se o estado completo de um HabitTracker (com vários hábitos e conclusões)
    é salvo corretamente e depois carregado, recriando o estado idêntico.
    Componentes: HabitTracker <-> persistence.py <-> File System
    """
    # 1. Setup: Cria um estado complexo no HabitTracker
    tracker_original = HabitTracker()
    tracker_original.add_habit("Ler Livro")
    tracker_original.add_habit("Correr")
    
    hoje = date(2025, 7, 1)
    ontem = hoje - timedelta(days=1)
    
    tracker_original.mark_complete("Ler Livro", hoje)
    tracker_original.mark_complete("Ler Livro", ontem)
    tracker_original.mark_complete("Correr", hoje)

    # 2. Ação: Salva os dados
    save_data(tracker_original)

    # 3. Ação: Carrega os dados em uma nova instância
    tracker_carregado = load_data()

    # 4. Verificação: Compara o estado do tracker carregado com o original
    assert len(tracker_carregado.habits) == 2
    habito_leitura = tracker_carregado.get_habit("Ler Livro")
    habito_corrida = tracker_carregado.get_habit("Correr")
    
    assert habito_leitura is not None
    assert habito_corrida is not None
    assert habito_leitura.completions == {hoje, ontem}
    assert habito_corrida.completions == {hoje}

def test_add_habit_persists_after_save():
    """
    Testa se adicionar um novo hábito e salvar resulta na sua correta
    persistência no arquivo JSON.
    Componentes: HabitTracker <-> persistence.py <-> File System
    """
    # 1. Setup: Começa com um tracker vazio e o salva (criando um arquivo vazio)
    tracker = HabitTracker()
    save_data(tracker)

    # 2. Ação: Adiciona um hábito e salva novamente
    tracker.add_habit("Meditar")
    save_data(tracker)

    # 3. Verificação: Carrega os dados e verifica se o hábito existe
    tracker_verificacao = load_data()
    assert len(tracker_verificacao.habits) == 1
    assert tracker_verificacao.get_habit("Meditar") is not None

def test_delete_habit_persists_after_save():
    """
    Testa se deletar um hábito e salvar o remove permanentemente do arquivo JSON.
    Componentes: HabitTracker <-> persistence.py <-> File System
    """
    # 1. Setup: Cria um tracker com dois hábitos e o salva
    tracker = HabitTracker()
    tracker.add_habit("Beber Água")
    tracker.add_habit("Estudar")
    save_data(tracker)

    # 2. Ação: Deleta um dos hábitos e salva
    tracker.delete_habit("Beber Água")
    save_data(tracker)

    # 3. Verificação: Carrega os dados e verifica se o hábito foi removido
    tracker_verificacao = load_data()
    assert len(tracker_verificacao.habits) == 1
    assert tracker_verificacao.get_habit("Beber Água") is None
    assert tracker_verificacao.get_habit("Estudar") is not None

def test_mark_completion_persists_after_save():
    """
    Testa se marcar um hábito como concluído é refletido no arquivo JSON após salvar.
    Componentes: HabitTracker <-> persistence.py <-> File System
    """
    # 1. Setup: Cria um hábito sem conclusões e salva
    tracker = HabitTracker()
    tracker.add_habit("Alongar")
    save_data(tracker)
    
    data_conclusao = date(2025, 6, 30)

    # 2. Ação: Marca o hábito como concluído e salva
    tracker.mark_complete("Alongar", data_conclusao)
    save_data(tracker)

    # 3. Verificação: Carrega os dados e checa o conjunto de conclusões
    tracker_verificacao = load_data()
    habito_alongar = tracker_verificacao.get_habit("Alongar")
    assert habito_alongar is not None
    assert len(habito_alongar.completions) == 1
    assert data_conclusao in habito_alongar.completions

def test_streak_calculation_with_date_manager_integration():
    """
    Testa a integração entre a lógica de cálculo de streak e o gerenciador de data.
    Verifica se a streak é calculada corretamente com base na data "atual" do app.
    Componentes: HabitTracker <-> app_date_manager.py
    """
    # 1. Setup: Cria um hábito com uma sequência de conclusões
    tracker = HabitTracker()
    tracker.add_habit("Yoga")
    
    dia1 = date(2025, 6, 28)
    dia2 = date(2025, 6, 29)
    dia3 = date(2025, 6, 30)
    
    tracker.mark_complete("Yoga", dia1)
    tracker.mark_complete("Yoga", dia2)
    tracker.mark_complete("Yoga", dia3)

    # Mocking da data "hoje" para o teste
    hoje_falso = date(2025, 7, 2)
    app_date_manager._today_func = lambda: hoje_falso

    # 2. Ação e Verificação
    app_date_manager.set_current_app_date(dia3)
    assert tracker.get_current_streak("Yoga", app_date_manager.get_current_app_date()) == 3

    app_date_manager.advance_day()
    assert app_date_manager.get_current_app_date() == date(2025, 7, 1)
    assert tracker.get_current_streak("Yoga", app_date_manager.get_current_app_date()) == 3

    app_date_manager.advance_day() 
    assert app_date_manager.get_current_app_date() == date(2025, 7, 2)
    assert tracker.get_current_streak("Yoga", app_date_manager.get_current_app_date()) == 0

    app_date_manager.advance_day() 
    assert app_date_manager.get_current_app_date() == date(2025, 7, 2)
