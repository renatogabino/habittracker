# main_gui.py
import flet as ft
from datetime import date # Manter para tipagem e fallback inicial
from habit_logic import HabitTracker # Se HabitControl for ft.Column, importe Habit também
from persistence import save_data, load_data
from app_date_manager import get_current_app_date, advance_day, rewind_day, reset_to_today

class HabitControl(ft.Row): # Mantendo ft.Row conforme o arquivo fornecido. Se você mudou para ft.Column, mantenha sua alteração.
    """Um controle de UI customizado para representar um único hábito."""
    # Modificar o construtor para aceitar a data atual do app
    def __init__(self, habit_name: str, tracker: HabitTracker, current_app_date: date, on_change):
        super().__init__()
        self.habit_name = habit_name
        self.tracker = tracker
        self.current_app_date = current_app_date # Usar a data passada
        self.on_change = on_change
        # self.today = date.today() # Remover esta linha

        self.checkbox = ft.Checkbox(
            # Usar current_app_date
            value=self.tracker.is_complete_today(self.habit_name, self.current_app_date),
            label=self.habit_name,
            on_change=self.toggle_completion,
        )
        # Usar current_app_date
        self.streak_text = ft.Text(f"🔥 {self.tracker.get_current_streak(self.habit_name, self.current_app_date)}")
        self.delete_button = ft.IconButton(
            icon=ft.Icons.DELETE_OUTLINE,
            tooltip="Deletar hábito",
            on_click=self.delete_habit_click,
            icon_color=ft.Colors.with_opacity(0.5, ft.Colors.RED_ACCENT_700), # Cor um pouco mais forte
            icon_size=20
        )

        self.controls = [self.checkbox, self.streak_text, self.delete_button]
        self.alignment = ft.MainAxisAlignment.SPACE_BETWEEN
        self.vertical_alignment = ft.CrossAxisAlignment.CENTER


    def toggle_completion(self, e):
        """Marca ou desmarca o hábito como concluído para a data atual do app."""
        if self.checkbox.value:
            # Usar current_app_date
            self.tracker.mark_complete(self.habit_name, self.current_app_date)
        else:
            # Usar current_app_date
            self.tracker.mark_incomplete(self.habit_name, self.current_app_date)
        self.on_change()

    def delete_habit_click(self, e):
        """Deleta o hábito."""
        self.tracker.delete_habit(self.habit_name)
        self.on_change()

def main(page: ft.Page):
    page.title = "Rastreador de Hábitos"
    page.horizontal_alignment = ft.CrossAxisAlignment.CENTER
    page.window_width = 420 
    page.window_height = 700 
    page.padding = ft.padding.all(15)
    # page.theme_mode = ft.ThemeMode.DARK # Descomente para tema escuro

    tracker = load_data()

    # --- Controles de Data Estilizados ---
    current_date_display = ft.Text(
        " ", # Placeholder, será atualizado
        weight=ft.FontWeight.BOLD,
        size=16,
        text_align=ft.TextAlign.CENTER,
        # selectable=True # Se quiser que o usuário possa copiar a data
    )

    # Botões são definidos antes para que update_date_controls_state possa referenciá-los
    prev_day_button = ft.IconButton(
        ft.Icons.ARROW_BACK_IOS_NEW_ROUNDED,
        on_click=lambda e: handle_date_change(rewind_day),
        tooltip="Dia Anterior"
    )
    next_day_button = ft.IconButton(
        ft.Icons.ARROW_FORWARD_IOS_ROUNDED,
        on_click=lambda e: handle_date_change(advance_day),
        tooltip="Próximo Dia"
    )
    reset_day_button = ft.TextButton(
        content=ft.Row(
            [ft.Icon(ft.Icons.TODAY_ROUNDED, color=ft.Colors.PRIMARY), ft.Text("Hoje", color=ft.Colors.PRIMARY, weight=ft.FontWeight.W_500)],
            alignment=ft.MainAxisAlignment.CENTER,
            spacing=5,
        ),
        on_click=lambda e: handle_date_change(reset_to_today),
        tooltip="Ir para Hoje"
    )

    def update_date_controls_visual_state():
        """Atualiza o texto da data e o estado (habilitado/desabilitado) dos botões de data."""
        app_date = get_current_app_date()
        today_real = date.today()

        # Formato da data: "09/06/2025 (Seg)"
        # Para um formato mais longo e localizado (ex: "Segunda-feira, 09 de Junho"), 
        # você pode usar app_date.strftime("%A, %d de %B").capitalize(),
        # mas certifique-se de que o locale do sistema está configurado para português.
        current_date_display.value = app_date.strftime("%d/%m/%Y (%a)")
        
        next_day_button.disabled = (app_date >= today_real)
        reset_day_button.disabled = (app_date == today_real)
        
        # Atualiza os controles se já estiverem na página
        if current_date_display.page: current_date_display.update()
        if next_day_button.page: next_day_button.update()
        if reset_day_button.page: reset_day_button.update()


    def handle_date_change(action_function):
        """Executa a ação de mudança de data e atualiza toda a UI."""
        action_function() # Executa rewind_day, advance_day ou reset_to_today
        update_date_controls_visual_state() # Atualiza os botões de data primeiro
        update_and_save() # Atualiza a lista de hábitos e salva

    date_navigation_row = ft.Row(
        [
            prev_day_button,
            ft.Container(current_date_display, expand=True, alignment=ft.alignment.center),
            next_day_button,
        ],
        alignment=ft.MainAxisAlignment.SPACE_BETWEEN,
        vertical_alignment=ft.CrossAxisAlignment.CENTER,
    )

    full_date_controls_container = ft.Column(
        [
            date_navigation_row,
            ft.Row([reset_day_button], alignment=ft.MainAxisAlignment.CENTER) # Botão "Hoje" abaixo
        ],
        spacing=5
    )
    # --- Fim dos Controles de Data ---

    def update_and_save():
        """Função central que atualiza a lista de hábitos, salva os dados e atualiza a página."""
        build_habit_list() 
        save_data(tracker)
        page.update()

    def add_habit_click(e):
        habit_name = new_habit_field.value.strip()
        if habit_name:
            if tracker.add_habit(habit_name):
                new_habit_field.value = ""
                new_habit_field.error_text = None
                new_habit_field.update()
                # A atualização da lista de hábitos e salvamento é feita por handle_date_change ou update_and_save
                # Se adicionar um hábito não deve mudar a data, chame update_and_save diretamente
                update_and_save() 
            else:
                new_habit_field.error_text = "Este hábito já existe."
                new_habit_field.update()
        else:
            new_habit_field.error_text = "Nome do hábito não pode ser vazio."
            new_habit_field.update()
    
    def on_field_change(e):
        new_habit_field.error_text = None
        new_habit_field.update()

    new_habit_field = ft.TextField(
        hint_text="Novo hábito...",
        expand=True,
        on_change=on_field_change,
        border_radius=20,
        filled=True,
        border_color=ft.Colors.TRANSPARENT,
        focused_border_color=ft.Colors.PRIMARY,
        dense=True,
        content_padding=ft.padding.symmetric(horizontal=15, vertical=10)
    )
    add_button = ft.IconButton(
        icon=ft.Icons.ADD_CIRCLE_OUTLINE, 
        on_click=add_habit_click, 
        tooltip="Adicionar Hábito",
        icon_size=28,
        icon_color=ft.Colors.PRIMARY
    )
    
    habits_view_title = ft.Text(
        "Meus Hábitos", 
        size=18, 
        weight=ft.FontWeight.BOLD, 
        text_align=ft.TextAlign.CENTER,
        color=ft.Colors.PRIMARY
    )
    habits_view = ft.ListView(
        expand=True, 
        spacing=8, 
        auto_scroll=True,
        padding=ft.padding.only(top=5)
    )
    no_habits_message = ft.Text(
        "Nenhum hábito ainda. Adicione um novo!", 
        italic=True, 
        text_align=ft.TextAlign.CENTER, 
        color=ft.Colors.OUTLINE,
        visible=False 
    )

    def build_habit_list():
        habits_view.controls.clear()
        app_date = get_current_app_date()
        
        sorted_user_habits = sorted(tracker.habits, key=lambda h: h.name)

        if not sorted_user_habits:
            no_habits_message.visible = True
            habits_view.visible = False
        else:
            no_habits_message.visible = False
            habits_view.visible = True
            for habit in sorted_user_habits:
                habits_view.controls.append(HabitControl(habit.name, tracker, app_date, update_and_save)) # Passa update_and_save como callback

    # --- Layout da Página ---
    page.add(
        ft.Column(
            [
                full_date_controls_container,
                ft.Divider(height=12, thickness=1),
                ft.Row(
                    [new_habit_field, add_button], 
                    alignment=ft.MainAxisAlignment.SPACE_BETWEEN,
                    vertical_alignment=ft.CrossAxisAlignment.CENTER
                ),
                ft.Divider(height=12, thickness=1),
                habits_view_title,
                no_habits_message, 
                habits_view, 
            ],
            expand=True,
            scroll=ft.ScrollMode.ADAPTIVE,
            spacing=10 
        )
    )

    # Configuração inicial da UI e estado dos controles de data
    update_date_controls_visual_state() # Define o texto da data e o estado dos botões
    update_and_save() # Constrói a lista de hábitos e atualiza a página

if __name__ == "__main__":
    ft.app(target=main)