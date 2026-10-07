import unicodedata

from django import template

register = template.Library()

# Ordem importa: a primeira palavra-chave encontrada no texto "vence".
# Ajuste/adicione entradas livremente conforme surgirem novos setores.
# São classes do Font Awesome (a mesma biblioteca já usada no resto do site).
SETOR_ICONE_MAP = [
    ("agro", "fas fa-seedling"),
    ("educa", "fas fa-graduation-cap"),
    ("saude", "fas fa-heartbeat"),
    ("financ", "fas fa-coins"),
    ("sustent", "fas fa-recycle"),
    ("servic", "fas fa-cogs"),
    ("comerc", "fas fa-shopping-cart"),
    ("varejo", "fas fa-shopping-cart"),
    ("tecnolog", "fas fa-laptop-code"),
    ("industr", "fas fa-industry"),
    ("turismo", "fas fa-suitcase-rolling"),
    ("aliment", "fas fa-utensils"),
    ("logist", "fas fa-truck"),
    ("energia", "fas fa-bolt"),
    ("constru", "fas fa-hard-hat"),
    ("moda", "fas fa-tshirt"),
    ("esporte", "fas fa-medal"),
]

SETOR_ICONE_PADRAO = "fas fa-rocket"

ESTAGIO_ICONE_MAP = {
    "ideacao": "fas fa-lightbulb",
    "validacao": "fas fa-search",
    "tracao": "fas fa-chart-line",
    "escala": "fas fa-rocket",
}

ESTAGIO_ICONE_PADRAO = "fas fa-briefcase"


def _normalizar(texto):
    """Minúsculo e sem acentos, pra facilitar a comparação por palavra-chave."""
    texto = texto.lower()
    texto = unicodedata.normalize("NFKD", texto)
    return "".join(c for c in texto if not unicodedata.combining(c))


@register.filter
def setor_icone(setor_atuacao):
    """Recebe o texto livre do setor_atuacao e devolve a classe do ícone Font Awesome."""
    if not setor_atuacao:
        return SETOR_ICONE_PADRAO

    texto_normalizado = _normalizar(setor_atuacao)

    for palavra_chave, icone in SETOR_ICONE_MAP:
        if palavra_chave in texto_normalizado:
            return icone

    return SETOR_ICONE_PADRAO


@register.filter
def estagio_icone(estagio):
    """Recebe o valor bruto do campo estagio (ex: 'tracao') e devolve a classe do ícone."""
    if not estagio:
        return ESTAGIO_ICONE_PADRAO
    return ESTAGIO_ICONE_MAP.get(estagio, ESTAGIO_ICONE_PADRAO)