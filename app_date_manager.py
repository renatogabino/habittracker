from datetime import date, timedelta

# Função que retorna a data real.
def _get_real_today():
    return date.today()

# Por padrão, a função que define "hoje" é a que retorna a data real.
# Os testes poderão substituir esta função.
_today_func = _get_real_today
_current_app_date = _today_func()

def get_current_app_date() -> date:
    """Retorna a data atualmente configurada para o aplicativo."""
    global _current_app_date
    return _current_app_date

def set_current_app_date(new_date: date):
    """Define manualmente a data do aplicativo, não permitindo datas futuras."""
    global _current_app_date
    today = _today_func() # Usa a função controlável
    if new_date > today:
        _current_app_date = today
    else:
        _current_app_date = new_date

def advance_day():
    """Avança a data do aplicativo em um dia, se não ultrapassar o dia de hoje."""
    global _current_app_date
    today = _today_func() # Usa a função controlável
    if _current_app_date < today:
        _current_app_date += timedelta(days=1)
    # Garante que, mesmo que algo dê errado, não passe de hoje
    elif _current_app_date > today:
         _current_app_date = today


def rewind_day():
    """Retrocede a data do aplicativo em um dia."""
    global _current_app_date
    # Aqui você poderia adicionar um limite inferior, se desejado, mas não foi solicitado.
    _current_app_date -= timedelta(days=1)

def reset_to_today():
    """Reseta a data do aplicativo para o dia atual real."""
    global _current_app_date
    _current_app_date = _today_func() # Usa a função controlável