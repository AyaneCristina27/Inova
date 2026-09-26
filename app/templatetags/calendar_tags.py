from datetime import timedelta, timezone as dt_timezone
from urllib.parse import urlencode

from django import template

register = template.Library()


@register.simple_tag
def google_calendar_link(titulo, data_inicio, data_fim=None, local='', descricao='', duracao_horas=1):
    if data_fim is None:
        data_fim = data_inicio + timedelta(hours=duracao_horas)

    fmt = '%Y%m%dT%H%M%SZ'
    inicio_str = data_inicio.astimezone(dt_timezone.utc).strftime(fmt)
    fim_str = data_fim.astimezone(dt_timezone.utc).strftime(fmt)

    params = {
        'action': 'TEMPLATE',
        'text': titulo,
        'dates': f'{inicio_str}/{fim_str}',
        'details': descricao or '',
        'location': local or '',
    }
    return 'https://calendar.google.com/calendar/render?' + urlencode(params)