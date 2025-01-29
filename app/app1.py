import dash_bootstrap_components as dbc
import numpy as np
import pandas as pd
import plotly.express as px
from dash import Dash, Input, Output, State, callback, clientside_callback, dcc, html
from dash.exceptions import PreventUpdate
from dash_bootstrap_templates import load_figure_template
from plotly.graph_objects import Figure

dbc_css = "https://cdn.jsdelivr.net/gh/AnnMarieW/dash-bootstrap-templates/dbc.min.css"  # Provides class "dbc"
dbc_class = "dbc"

# Pick other themes from "https://dash-bootstrap-components.opensource.faculty.ai/docs/themes/explorer/"
dbc_light_theme = "lumen"
dbc_dark_theme = "darkly"


resorts = pd.read_csv("data/resorts.csv", encoding="ISO-8859-1").assign(
    country_elevation_rank=lambda x: x.groupby("Country", as_index=False)["Highest point"].rank(ascending=False),
    country_price_rank=lambda x: x.groupby("Country", as_index=False)["Price"].rank(ascending=False),
    country_slope_rank=lambda x: x.groupby("Country", as_index=False)["Total slopes"].rank(ascending=False),
    country_cannon_rank=lambda x: x.groupby("Country", as_index=False)["Snow cannons"].rank(ascending=False),
)


app1 = Dash(
    __name__,
    external_stylesheets=[
        dbc_css,
        getattr(dbc.themes, dbc_light_theme.upper()),
        dbc.icons.BOOTSTRAP,
    ],
)
app1.title = "Interactive Dashboard Demo"

load_figure_template([dbc_dark_theme, dbc_light_theme])


html_map_title_id = "html-map-title"
dcc_price_slider_id = "dcc-price-slider"
dcc_summer_ski_checklist_id = "dcc-summer-ski-checklist"
dcc_night_ski_checklist_id = "dcc-night-ski-checklist"
dcc_snow_park_checklist_id = "dcc-snow-park-checklist"
dcc_resort_map_graph_id = "dcc-resort-map"

html_country_title_id = "html-country-title"
dcc_continent_dropdown_id = "dcc-continent-dropdown"
dcc_country_dropdown_id = "dcc-country-dropdown"
dcc_col_picker_dropdown_id = "dcc-col-picker-dropdown"
dcc_metric_bar_graph_id = "dcc-metric-bar-graph"
dbc_resort_name_card_id = "dbc-resort-name-card"
dbc_elevation_kpi_card_id = "dbc-elevation-kpi-card"
dbc_price_kpi_card_id = "dbc-price-kpi-card"
dbc_slope_kpi_card_id = "dbc-slope-kpi-card"
dbc_cannon_kpi_card_id = "dbc-cannon-kpi-card"

nav_bar_id = "nav-bar"
nav_bar_toggler_id = "nav-bar-toggler"
nav_bar_collapse_id = "nav-bar-collapse"
color_mode_switch_id = "color-mode-switch"

color_mode_switch = html.Span(
    children=[
        dbc.Label(class_name="bi bi-moon mb-0", html_for=color_mode_switch_id),
        dbc.Switch(id=color_mode_switch_id, value=False, class_name="d-inline-block ms-1", persistence=True),
        dbc.Label(class_name="bi bi-sun mb-0", html_for=color_mode_switch_id),
    ],
)

nav_bar = dbc.Navbar(
    dbc.Container(
        children=[
            dbc.NavbarBrand("Janus", href="https://drxaero.github.io/"),
            dbc.NavbarToggler(id=nav_bar_toggler_id, n_clicks=0),
            dbc.Collapse(
                children=[
                    dbc.Nav(
                        children=[
                            dbc.NavItem(dbc.NavLink("CV", href="https://www.linkedin.com/in/januscheng/")),
                        ],
                        navbar=True,
                        class_name="me-auto",
                    ),
                    color_mode_switch,
                ],
                id=nav_bar_collapse_id,
                navbar=True,
            ),
        ],
    ),
    id=nav_bar_id,
    sticky="top",
    class_name="navbar-expand mb-1",
)


app1.layout = dbc.Container(
    children=[
        nav_bar,
        dbc.Row(
            dbc.Tabs(
                children=[
                    dbc.Tab(
                        label="Resort Map",
                        children=[
                            html.H1(id=html_map_title_id, style={"textAlign": "center"}),
                            dbc.Row(
                                [
                                    dbc.Col(
                                        [
                                            dbc.Card(
                                                [
                                                    html.Div("Price Limit"),
                                                    dcc.Slider(
                                                        id=dcc_price_slider_id,
                                                        min=0,
                                                        max=150,
                                                        step=25,
                                                        value=150,
                                                        className=dbc_class,
                                                    ),
                                                    html.Hr(),
                                                    html.Div("Feature Preferences"),
                                                    dcc.Checklist(
                                                        id=dcc_summer_ski_checklist_id,
                                                        options=[{"label": "Has Summer Skiing", "value": "Yes"}],
                                                        value=[],
                                                    ),
                                                    dcc.Checklist(
                                                        id=dcc_night_ski_checklist_id,
                                                        options=[{"label": "Has Night Skiing", "value": "Yes"}],
                                                        value=[],
                                                    ),
                                                    dcc.Checklist(
                                                        id=dcc_snow_park_checklist_id,
                                                        options=[{"label": "Has Snow Park", "value": "Yes"}],
                                                        value=[],
                                                    ),
                                                ]
                                            ),
                                        ],
                                        lg=3,
                                        class_name="mb-5",
                                    ),
                                    dbc.Col([dcc.Graph(id=dcc_resort_map_graph_id)], lg=9, class_name="mb-5"),
                                ]
                            ),
                        ],
                    ),
                    dbc.Tab(
                        label="Country Profiler",
                        children=[
                            html.H1(id=html_country_title_id, style={"textAlign": "center"}),
                            dbc.Row(
                                [
                                    dbc.Col(
                                        [
                                            html.Div("Select A Continent:"),
                                            dcc.Dropdown(
                                                id=dcc_continent_dropdown_id,
                                                options=resorts["Continent"].unique(),
                                                value="Europe",
                                                className=dbc_class,
                                            ),
                                            html.Hr(),
                                            html.Div("Select A Country:"),
                                            dcc.Dropdown(
                                                id=dcc_country_dropdown_id,
                                                value="Norway",
                                                className=dbc_class,
                                            ),
                                            html.Hr(),
                                            html.Div("Select A Metric to Plot:"),
                                            dcc.Dropdown(
                                                id=dcc_col_picker_dropdown_id,
                                                options=resorts.select_dtypes("number").columns[3:],
                                                value="Price",
                                                className=dbc_class,
                                            ),
                                        ],
                                        md=3,
                                        class_name="mb-5",
                                    ),
                                    dbc.Col(
                                        [
                                            dcc.Graph(
                                                id=dcc_metric_bar_graph_id,
                                                hoverData={"points": [{"customdata": ["Hemsedal"]}]},
                                            ),
                                        ],
                                        md=6,
                                        class_name="mb-5",
                                    ),
                                    dbc.Col(
                                        [
                                            html.Div("Resort Report Card"),
                                            dbc.Card(
                                                id=dbc_resort_name_card_id,
                                                style={"texAlign": "center", "fontSize": 20},
                                            ),
                                            dbc.Row(
                                                [
                                                    dbc.Col(
                                                        [
                                                            dbc.Card(id=dbc_elevation_kpi_card_id),
                                                            dbc.Card(id=dbc_price_kpi_card_id),
                                                        ]
                                                    ),
                                                    dbc.Col(
                                                        [
                                                            dbc.Card(id=dbc_slope_kpi_card_id),
                                                            dbc.Card(id=dbc_cannon_kpi_card_id),
                                                        ]
                                                    ),
                                                ]
                                            ),
                                        ],
                                        md=3,
                                        class_name="mb-5",
                                    ),
                                ],
                            ),
                        ],
                    ),
                ],
            ),
        ),
    ],
)


@callback(
    Output(nav_bar_id, "color"),
    Output(html_map_title_id, "children"),
    Output(dcc_resort_map_graph_id, "figure"),
    Input(color_mode_switch_id, "value"),
    Input(dcc_price_slider_id, "value"),
    Input(dcc_summer_ski_checklist_id, "value"),
    Input(dcc_night_ski_checklist_id, "value"),
    Input(dcc_snow_park_checklist_id, "value"),
)
def snow_map(switch_on: bool, price: int, summer_ski: str, night_ski: str, snow_park: str) -> tuple[str, Figure]:
    if not price:
        raise PreventUpdate

    title = f"Resorts with a ticket price less than ${price}."

    df = resorts.loc[(resorts["Price"] <= price)]

    if "Yes" in summer_ski:
        df = df.loc[(df["Summer skiing"] == "Yes")]

    if "Yes" in night_ski:
        df = df.loc[(df["Nightskiing"] == "Yes")]

    if "Yes" in snow_park:
        df = df.loc[(df["Snowparks"] == "Yes")]

    fig = px.density_map(
        df,
        lat="Latitude",
        lon="Longitude",
        z="Total slopes",
        hover_name="Resort",
        center={"lat": 45, "lon": -100},
        zoom=2.5,
        height=600,
        map_style="open-street-map",
        color_continuous_scale="blues",
        template=get_template(switch_on),
        opacity=0.8,
    ).update_layout(margin_t=40, margin_r=40, margin_b=40, margin_l=40)

    color = "light" if switch_on else "dark"

    return color, title, fig


@callback(Output(dcc_country_dropdown_id, "options"), Input(dcc_continent_dropdown_id, "value"))
def country_select(continent: str) -> list[str]:
    return np.sort(resorts.query(f"Continent == '{continent}'")["Country"].unique())


@callback(
    Output(html_country_title_id, "children"),
    Output(dcc_metric_bar_graph_id, "figure"),
    Input(color_mode_switch_id, "value"),
    Input(dcc_country_dropdown_id, "value"),
    Input(dcc_col_picker_dropdown_id, "value"),
)
def plot_bar(switch_on: bool, country: str, metric: str) -> tuple[str, Figure]:
    if not country and metric:
        raise PreventUpdate

    title = f"Top Resort Metrics in {country} by {metric}"

    df = resorts.query("Country == @country").sort_values(metric, ascending=False)
    fig = (
        px.bar(df, x="Resort", y=metric, custom_data=["Resort"], template=get_template(switch_on))
        .update_xaxes(showticklabels=False)
        .update_layout(margin_t=60, margin_r=60, margin_b=60, margin_l=60)
    )

    return title, fig


def get_template(switch_on: bool) -> str:
    return dbc_light_theme if switch_on else dbc_dark_theme


@callback(
    Output(dbc_resort_name_card_id, "children"),
    Output(dbc_elevation_kpi_card_id, "children"),
    Output(dbc_price_kpi_card_id, "children"),
    Output(dbc_slope_kpi_card_id, "children"),
    Output(dbc_cannon_kpi_card_id, "children"),
    Input(dcc_metric_bar_graph_id, "hoverData"),
)
def update_line(hoverData) -> tuple[str, str, str, str, str]:

    resort = hoverData["points"][0]["customdata"][0]
    df = resorts.query(f"Resort == '{resort}'")

    resort_name = df["Resort"]

    elev_rank = f"Elevation Rank: {int(df['country_elevation_rank'].iloc[0])}"
    price_rank = f"Price Rank: {int(df['country_price_rank'].iloc[0])}"
    slope_rank = f"Slope Rank: {int(df['country_slope_rank'].iloc[0])}"
    cannon_rank = f"Cannon Rank: {int(df['country_cannon_rank'].iloc[0])}"

    return resort_name, elev_rank, price_rank, slope_rank, cannon_rank


@callback(
    Output(nav_bar_collapse_id, "is_open"),
    [Input(nav_bar_toggler_id, "n_clicks")],
    [State(nav_bar_collapse_id, "is_open")],
)
def toggle_navbar_collapse(n: int, is_open: bool) -> bool:
    if n:
        return not is_open
    return is_open


clientside_callback(
    """
    (switchOn) => {
       document.documentElement.setAttribute('data-bs-theme', switchOn ? 'light' : 'dark');
       return window.dash_clientside.no_update
    }
    """,
    Output(color_mode_switch_id, "id"),
    Input(color_mode_switch_id, "value"),
)


@app1.server.route("/ping")
def ping():
    """
    To enable health check
    """
    data = {"status": "ok"}
    return data, 200


if __name__ == "__main__":
    app1.run_server(debug=True)  # `host="0.0.0.0"` or `port=8051` or `debug=True` or `height=800` or `width="80%"`
