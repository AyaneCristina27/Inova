"""
App Dash do dashboard do ecossistema regional de inovação.

Ele é registrado com o nome "DashboardInova" e aparece na página pelo
template _dashboard.html, com a tag {% plotly_direct name="DashboardInova" %}.

Como a interação funciona (callbacks):
- clicar numa barra do gráfico de municípios ou num ponto do mapa
  escolhe aquele município no filtro;
- o botão "Limpar filtro" volta para todos os municípios;
- sempre que o filtro muda, os cartões e todos os gráficos são atualizados,
  sem recarregar a página.
"""

import dash
from dash import Input, Output, dcc, html, no_update
from django_plotly_dash import DjangoDash

from .dashboard import lista_municipios, montar_dashboard

app = DjangoDash("DashboardInova")

CONFIG_GRAFICO = {"displaylogo": False}


def _cartao(rotulo, valor, icone):
    """Cartão com ícone e rótulo em cima e o número embaixo."""
    return html.Div(
        className="dash-kpi",
        children=[
            html.Div(
                className="dash-kpi-topo",
                children=[
                    html.Span(html.I(className=icone), className="dash-kpi-icone"),
                    html.Span(rotulo, className="dash-kpi-rotulo"),
                ],
            ),
            html.Strong(valor, className="dash-kpi-valor"),
        ],
    )


def _cartao_detalhe(rotulo, valor, detalhe):
    """Cartão largo com o número e uma explicação na mesma linha."""
    return html.Div(
        className="dash-kpi",
        children=[
            html.Span(rotulo, className="dash-kpi-rotulo"),
            html.Div(
                className="dash-kpi-linha",
                children=[html.Strong(valor, className="dash-kpi-valor"), html.Small(detalhe)],
            ),
        ],
    )


def _grafico(id_grafico, largo=False):
    classe = "dash-card dash-largo" if largo else "dash-card"
    return html.Div(
        dcc.Graph(id=id_grafico, config=CONFIG_GRAFICO, style={"height": "330px"}),
        className=classe,
    )


app.layout = html.Div(
    className="inova-dash-app",
    children=[
        html.Div(
            className="dash-topo",
            children=[
                html.Div(
                    [
                        html.H2(["Dashboard do ecossistema regional de ", html.Span("inovação")]),
                        html.P("Sudoeste de Minas Gerais"),
                    ]
                ),
                html.Div(html.I(className="fas fa-lightbulb"), className="dash-topo-icone"),
            ],
        ),
        html.Div(
            className="dash-filtros",
            children=[
                html.Label("Município:", htmlFor="filtro-municipio"),
                dcc.Dropdown(
                    id="filtro-municipio",
                    placeholder="Todos os municípios",
                    clearable=True,
                    className="dash-dropdown",
                ),
                html.Button("Limpar filtro", id="limpar-filtro", n_clicks=0, className="dash-limpar"),
                html.Span(
                    "Dica: clique numa barra ou num ponto do mapa para filtrar.",
                    className="dash-dica",
                ),
            ],
        ),
        html.Div(id="cartoes-indicadores", className="dash-kpis dash-kpis-principais"),
        html.P("Empresas e ambientes de inovação", className="dash-secao"),
        html.Div(id="cartoes-empresas", className="dash-kpis dash-kpis-duplo"),
        html.Div(
            className="dash-graficos",
            children=[
                _grafico("grafico-municipios", largo=True),
                _grafico("grafico-estagios"),
                _grafico("grafico-instituicoes"),
                _grafico("grafico-mapa"),
                _grafico("grafico-status"),
            ],
        ),
    ],
)


@app.callback(
    Output("filtro-municipio", "value"),
    Input("grafico-municipios", "clickData"),
    Input("grafico-mapa", "clickData"),
    Input("limpar-filtro", "n_clicks"),
    prevent_initial_call=True,
)
def escolher_municipio(clique_barras, clique_mapa, _cliques_limpar):
    """Transforma um clique num gráfico em uma escolha no filtro."""
    # O django-plotly-dash guarda aqui qual componente disparou o callback
    disparos = dash.callback_context.triggered or []
    origem = disparos[0]["prop_id"].split(".")[0] if disparos else None
    if origem == "limpar-filtro":
        return None
    if origem == "grafico-municipios" and clique_barras:
        return clique_barras["points"][0]["x"]
    if origem == "grafico-mapa" and clique_mapa:
        return clique_mapa["points"][0]["customdata"]
    return no_update


@app.callback(
    Output("filtro-municipio", "options"),
    Output("cartoes-indicadores", "children"),
    Output("cartoes-empresas", "children"),
    Output("grafico-municipios", "figure"),
    Output("grafico-estagios", "figure"),
    Output("grafico-instituicoes", "figure"),
    Output("grafico-mapa", "figure"),
    Output("grafico-status", "figure"),
    Input("filtro-municipio", "value"),
)
def atualizar_dashboard(municipio):
    """Busca os dados (com ou sem filtro) e redesenha tudo."""
    dados = montar_dashboard(municipio)
    graficos = dados["graficos"]
    opcoes = [{"label": nome, "value": nome} for nome in lista_municipios()]
    cartoes = [_cartao(i["rotulo"], i["valor"], i["icone"]) for i in dados["indicadores"]]
    cartoes_empresas = [
        _cartao_detalhe(i["rotulo"], i["valor"], i["detalhe"]) for i in dados["empresas_ambientes"]
    ]
    return (
        opcoes,
        cartoes,
        cartoes_empresas,
        graficos["municipios"],
        graficos["estagios"],
        graficos["instituicoes"],
        graficos["mapa"],
        graficos["status"],
    )