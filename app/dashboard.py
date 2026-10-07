"""
Dashboard do ecossistema regional de inovação.

Busca os dados no banco e monta os indicadores (cartões) e as figuras
Plotly. Quem usa estas funções é o app Dash, em dash_app.py.
"""

import plotly.graph_objects as go
from django.db.models import Count, Q

from .models import Ator, CasoSucesso, Evento, Municipio, Projeto, Startup

# Cores do dashboard (as mesmas do Power BI)
LARANJA = "#E07B39"
PRETO = "#1C1C1C"
BEGE = "#F2C18D"
FONTE = "Segoe UI, Arial, sans-serif"

# Nomes das categorias de atores, iguais aos cadastrados no admin
CATEGORIA_EMPRESA = "Empresa"
CATEGORIAS_AMBIENTE = ["Incubadora de Empresa", "Coworking", "Espaço Maker"]

# A ordem abaixo é a ordem em que aparecem nos gráficos e legendas:
# do começo ao fim da jornada, com as cores indo do mais claro ao mais escuro.
ESTAGIOS = {
    "ideacao": ("Ideação", BEGE),
    "validacao": ("Validação", LARANJA),
    "tracao": ("Tração", PRETO),
}

STATUS_PROJETO = {
    "planejado": ("Planejado", BEGE),
    "em_andamento": ("Em andamento", LARANJA),
    "concluido": ("Concluído", PRETO),
}

# Coordenadas aproximadas (latitude, longitude) do centro de cada município.
# Se cadastrar um município novo, acrescente aqui para ele aparecer no mapa.
COORDENADAS = {
    "Arceburgo": (-21.3636, -46.9403),
    "Bom Jesus da Penha": (-21.0136, -46.5256),
    "Cabo Verde": (-21.4722, -46.3958),
    "Guaranésia": (-21.3000, -46.8028),
    "Guaxupé": (-21.3050, -46.7128),
    "Itamoji": (-21.0772, -47.0469),
    "Itamogi": (-21.0772, -47.0469),
    "Jacuí": (-21.0144, -46.7406),
    "Juruaia": (-21.2536, -46.5747),
    "Monte Santo de Minas": (-21.1897, -46.9803),
    "Muzambinho": (-21.3761, -46.5256),
    "Nova Resende": (-21.1286, -46.4156),
    "São Sebastião do Paraíso": (-20.9167, -46.9914),
    "São Tomás de Aquino": (-20.7792, -47.0983),
    "São Pedro da União": (-21.1311, -46.6128),
}


def _estilo(fig, titulo, altura=320):
    fig.update_layout(
        title={"text": titulo, "font": {"size": 14, "color": PRETO}, "x": 0.02},
        height=altura,
        margin={"l": 20, "r": 20, "t": 50, "b": 20},
        paper_bgcolor="white",
        plot_bgcolor="white",
        font={"family": FONTE, "color": "#444"},
        legend={"orientation": "h", "y": -0.15},
    )
    return fig


def _sem_dados(fig):
    fig.add_annotation(
        text="Sem dados para este filtro",
        showarrow=False,
        font={"size": 13, "color": "#999"},
        xref="paper",
        yref="paper",
        x=0.5,
        y=0.5,
    )
    fig.update_xaxes(visible=False)
    fig.update_yaxes(visible=False)
    return fig


def _grafico_municipios(atores):
    dados = list(
        atores.filter(
            Q(categoria__nome=CATEGORIA_EMPRESA)
            | Q(categoria__nome__in=CATEGORIAS_AMBIENTE)
        )
        .values("municipio__nome")
        .annotate(
            empresas=Count("id", filter=Q(categoria__nome=CATEGORIA_EMPRESA)),
            ambientes=Count("id", filter=Q(categoria__nome__in=CATEGORIAS_AMBIENTE)),
        )
        .order_by("municipio__nome")
    )
    fig = go.Figure()
    if dados:
        nomes = [d["municipio__nome"] for d in dados]
        # Barras finas: cada barra ocupa 18% do espaço de cada município
        fig.add_bar(
            name="Empresas inovadoras",
            x=nomes,
            y=[d["empresas"] for d in dados],
            marker_color=LARANJA,
            width=0.18,
            offset=-0.2,
            hovertemplate="%{x}<br>Empresas: %{y}<extra></extra>",
        )
        fig.add_bar(
            name="Ambientes de inovação",
            x=nomes,
            y=[d["ambientes"] for d in dados],
            marker_color=PRETO,
            width=0.18,
            offset=0.02,
            hovertemplate="%{x}<br>Ambientes: %{y}<extra></extra>",
        )
        fig.update_layout(barmode="overlay")
        fig.update_yaxes(dtick=1, gridcolor="#eee")
    else:
        _sem_dados(fig)
    return _estilo(fig, "Empresas e ambientes de inovação por município")


def _ordenar(dados, campo, ordem):
    """Coloca os dados na ordem definida em ESTAGIOS ou STATUS_PROJETO."""
    posicao = {chave: i for i, chave in enumerate(ordem)}
    return sorted(dados, key=lambda d: posicao.get(d[campo], len(posicao)))


def _rosca(dados, campo, rotulos_cores, unidade, buraco=0.6):
    """Gráfico de rosca (ou de pizza, com buraco=0) com só a porcentagem nas fatias.
    Na rosca, o total aparece no meio."""
    fig = go.Figure()
    if not dados:
        return _sem_dados(fig)
    dados = _ordenar(dados, campo, rotulos_cores)
    rotulos = [rotulos_cores.get(d[campo], (d[campo], "#999"))[0] for d in dados]
    cores = [rotulos_cores.get(d[campo], (d[campo], "#999"))[1] for d in dados]
    valores = [d["total"] for d in dados]
    fig.add_pie(
        labels=rotulos,
        values=valores,
        hole=buraco,
        marker={"colors": cores, "line": {"color": "white", "width": 2}},
        textinfo="percent",
        textposition="inside",
        insidetextfont={"size": 12},
        hovertemplate="%{label}: %{value} " + unidade + "<extra></extra>",
        sort=False,
        direction="clockwise",
    )
    if buraco:
        fig.add_annotation(
            text=f"<b>{sum(valores)}</b><br><span style='font-size:11px;color:#888'>total</span>",
            showarrow=False,
            font={"size": 24, "color": PRETO},
        )
    return fig


def _grafico_estagios(startups):
    dados = list(startups.values("estagio").annotate(total=Count("id")))
    return _estilo(
        _rosca(dados, "estagio", ESTAGIOS, "startup(s)"), "Startups por estágio"
    )


def _grafico_instituicoes(projetos):
    dados = list(
        projetos.exclude(instituicoes__nome=None)
        .values("instituicoes__nome")
        .annotate(total=Count("id", distinct=True))
        .order_by("total")
    )
    fig = go.Figure()
    if dados:
        fig.add_bar(
            x=[d["total"] for d in dados],
            y=[d["instituicoes__nome"] for d in dados],
            orientation="h",
            marker_color=LARANJA,
            width=0.3,
            hovertemplate="%{y}: %{x} projeto(s)<extra></extra>",
        )
        fig.update_xaxes(dtick=1, gridcolor="#eee")
    else:
        _sem_dados(fig)
    return _estilo(fig, "Projetos por instituição")


def _grafico_mapa(startups):
    dados = list(
        startups.values("municipio__nome")
        .annotate(total=Count("id"))
        .order_by("municipio__nome")
    )
    dados = [d for d in dados if d["municipio__nome"] in COORDENADAS]
    fig = go.Figure()
    if dados:
        nomes = [d["municipio__nome"] for d in dados]
        fig.add_trace(
            go.Scattermap(
                lat=[COORDENADAS[n][0] for n in nomes],
                lon=[COORDENADAS[n][1] for n in nomes],
                customdata=nomes,
                text=[f"{d['total']}" for d in dados],
                mode="markers+text",
                marker={
                    "size": [16 + 8 * d["total"] for d in dados],
                    "color": LARANJA,
                    "opacity": 0.85,
                },
                textfont={"color": "white", "size": 12},
                hovertemplate="%{customdata}<br>Startups: %{text}<extra></extra>",
            )
        )
    fig.update_layout(
        map={
            "style": "carto-positron",
            "center": {"lat": -21.15, "lon": -46.75},
            "zoom": 7.2,
        },
    )
    fig = _estilo(fig, "Startups por município")
    fig.update_layout(margin={"l": 0, "r": 0, "t": 50, "b": 0})
    return fig


def _grafico_status(projetos):
    dados = list(projetos.values("status").annotate(total=Count("id", distinct=True)))
    # buraco=0 deixa o gráfico como pizza (sem o furo no meio)
    return _estilo(
        _rosca(dados, "status", STATUS_PROJETO, "projeto(s)", buraco=0),
        "Projetos por status",
    )


def montar_dashboard(municipio=None):
    atores = Ator.objects.filter(ativo=True)
    startups = Startup.objects.filter(ativo=True)
    projetos = Projeto.objects.all()
    eventos = Evento.objects.all()
    casos = CasoSucesso.objects.filter(publicado=True)
    municipios = Municipio.objects.all()

    if municipio:
        atores = atores.filter(municipio__nome=municipio)
        startups = startups.filter(municipio__nome=municipio)
        projetos = projetos.filter(
            Q(instituicoes__municipio__nome=municipio)
            | Q(startups__municipio__nome=municipio)
        ).distinct()
        eventos = eventos.filter(municipio__nome=municipio)
        casos = casos.filter(
            Q(startup__municipio__nome=municipio) | Q(ator__municipio__nome=municipio)
        ).distinct()
        municipios = municipios.filter(nome=municipio)

    indicadores = [
        {
            "rotulo": "Instituições",
            "valor": atores.count(),
            "icone": "fas fa-university",
        },
        {
            "rotulo": "Municípios",
            "valor": municipios.count(),
            "icone": "fas fa-map-marker-alt",
        },
        {"rotulo": "Startups", "valor": startups.count(), "icone": "fas fa-rocket"},
        {
            "rotulo": "Projetos ativos",
            "valor": projetos.filter(status="em_andamento").count(),
            "icone": "fas fa-clipboard-list",
        },
        {
            "rotulo": "Parcerias",
            "valor": atores.filter(eh_parceiro_estrategico=True).count(),
            "icone": "fas fa-handshake",
        },
        {
            "rotulo": "Casos de sucesso",
            "valor": casos.count(),
            "icone": "fas fa-trophy",
        },
        {
            "rotulo": "Eventos realizados",
            "valor": eventos.count(),
            "icone": "fas fa-calendar-alt",
        },
    ]

    empresas_ambientes = [
        {
            "rotulo": "Empresas inovadoras",
            "valor": atores.filter(categoria__nome=CATEGORIA_EMPRESA).count(),
            "detalhe": "atores na categoria Empresa",
        },
        {
            "rotulo": "Ambientes de inovação",
            "valor": atores.filter(categoria__nome__in=CATEGORIAS_AMBIENTE).count(),
            "detalhe": "incubadoras, coworkings e makers",
        },
    ]

    return {
        "indicadores": indicadores,
        "empresas_ambientes": empresas_ambientes,
        "graficos": {
            "municipios": _grafico_municipios(atores),
            "estagios": _grafico_estagios(startups),
            "instituicoes": _grafico_instituicoes(projetos),
            "mapa": _grafico_mapa(startups),
            "status": _grafico_status(projetos),
        },
    }


def lista_municipios():
    return list(Municipio.objects.order_by("nome").values_list("nome", flat=True))
