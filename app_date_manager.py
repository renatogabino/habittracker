from datetime import date, timedelta

_current_app_date = date.today()

def get_current_app_date() -> date:
    """Retorna a data atualmente configurada para o aplicativo."""
    global _current_app_date
    return _current_app_date

def set_current_app_date(new_date: date):
    """Define manualmente a data do aplicativo, não permitindo datas futuras."""
    global _current_app_date
    if new_date > date.today():
        _current_app_date = date.today()
    else:
        _current_app_date = new_date

def advance_day():
    """Avança a data do aplicativo em um dia, se não ultrapassar o dia de hoje."""
    global _current_app_date
    if _current_app_date < date.today():
        _current_app_date += timedelta(days=1)
    # Garante que, mesmo que algo dê errado, não passe de hoje
    elif _current_app_date > date.today():
         _current_app_date = date.today()


def rewind_day():
    """Retrocede a data do aplicativo em um dia."""
    global _current_app_date
    # Aqui você poderia adicionar um limite inferior, se desejado, mas não foi solicitado.
    _current_app_date -= timedelta(days=1)

def reset_to_today():
    """Reseta a data do aplicativo para o dia atual real."""
    global _current_app_date
    _current_app_date = date.today()