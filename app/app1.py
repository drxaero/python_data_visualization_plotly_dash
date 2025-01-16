from dash import dcc, Dash, html, Input, Output
from dash.exceptions import PreventUpdate
from plotly.graph_objects import Figure
import numpy as np
import plotly.express as px
import pandas as pd
import dash_bootstrap_components as dbc
from dash_bootstrap_templates import load_figure_template

dbc_css = "https://cdn.jsdelivr.net/gh/AnnMarieW/dash-bootstrap-templates/dbc.min.css"  # Provides class "dbc"
dbc_class = "dbc"
dbc_style_template = "darkly"  # darkly, slate, cerulean, bootstrap


resorts = pd.read_csv("data/resorts.csv", encoding="ISO-8859-1").assign(
    country_elevation_rank=lambda x: x.groupby("Country", as_index=False)["Highest point"].rank(ascending=False),
    country_price_rank=lambda x: x.groupby("Country", as_index=False)["Price"].rank(ascending=False),
    country_slope_rank=lambda x: x.groupby("Country", as_index=False)["Total slopes"].rank(ascending=False),
    country_cannon_rank=lambda x: x.groupby("Country", as_index=False)["Snow cannons"].rank(ascending=False),
)


app1 = Dash(
    __name__,
    external_stylesheets=[
        getattr(dbc.themes, dbc_style_template.upper()),  # DARKLY, SLATE, CERULEAN
        dbc_css,  # 這裡要參考到外部的 CSS
    ],
)

load_figure_template(dbc_style_template)

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

app1.layout = dbc.Container(
    dcc.Tabs(
        className=dbc_class,
        children=[
            dbc.Tab(
                label="Resort Map",
                children=[
                    html.H1(id=html_map_title_id, style={"text-align": "center"}),
                    dbc.Row(
                        [
                            dbc.Col(
                                [
                                    dbc.Card(
                                        [
                                            dcc.Markdown("**Price Limit**"),
                                            dcc.Slider(
                                                id=dcc_price_slider_id,
                                                min=0,
                                                max=150,
                                                step=25,
                                                value=150,
                                                className=dbc_class,
                                            ),
                                            html.Br(),
                                            dcc.Markdown("**Feature Preferences**"),
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
                                width=3,
                            ),
                            dbc.Col([dcc.Graph(id=dcc_resort_map_graph_id)], width=9),
                        ]
                    ),
                ],
            ),
            dbc.Tab(
                label="Country Profiler",
                children=[
                    html.H1(id=html_country_title_id, style={"text-align": "center"}),
                    dbc.Row(
                        [
                            dbc.Col(
                                [
                                    dcc.Markdown("Select A Continent:"),
                                    dcc.Dropdown(
                                        id=dcc_continent_dropdown_id,
                                        options=resorts["Continent"].unique(),
                                        value="Europe",
                                        className=dbc_class,
                                    ),
                                    html.Br(),
                                    dcc.Markdown("Select A Country:"),
                                    dcc.Dropdown(id=dcc_country_dropdown_id, value="Norway", className=dbc_class),
                                    html.Br(),
                                    dcc.Markdown("Select A Metric to Plot:"),
                                    dcc.Dropdown(
                                        id=dcc_col_picker_dropdown_id,
                                        options=resorts.select_dtypes("number").columns[3:],
                                        value="Price",
                                        className=dbc_class,
                                    ),
                                ],
                                width=3,
                            ),
                            dbc.Col(
                                [
                                    dcc.Graph(
                                        id=dcc_metric_bar_graph_id, hoverData={"points": [{"customdata": ["Hemsedal"]}]}
                                    ),
                                ],
                                width=6,
                            ),
                            dbc.Col(
                                [
                                    dcc.Markdown("### Resort Report Card"),
                                    dbc.Card(
                                        id=dbc_resort_name_card_id, style={"text-align": "center", "fontSize": 20}
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
                                width=3,
                            ),
                        ]
                    ),
                ],
            ),
        ],
    ),
    style={"width": 1300},
)


@app1.callback(
    Output(html_map_title_id, "children"),
    Output(dcc_resort_map_graph_id, "figure"),
    Input(dcc_price_slider_id, "value"),
    Input(dcc_summer_ski_checklist_id, "value"),
    Input(dcc_night_ski_checklist_id, "value"),
    Input(dcc_snow_park_checklist_id, "value"),
)
def snow_map(price: int, summer_ski: str, night_ski: str, snow_park: str) -> (str, Figure):
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

    fig = px.density_mapbox(
        df,
        lat="Latitude",
        lon="Longitude",
        z="Total slopes",
        hover_name="Resort",
        center={"lat": 45, "lon": -100},
        zoom=2.5,
        mapbox_style="open-street-map",
        color_continuous_scale="blues",
        width=800,
        height=600,
    )
    return title, fig


@app1.callback(Output(dcc_country_dropdown_id, "options"), Input(dcc_continent_dropdown_id, "value"))
def country_select(continent: str) -> list[str]:
    return np.sort(resorts.query("Continent == @continent")["Country"].unique())


@app1.callback(
    Output(html_country_title_id, "children"),
    Output(dcc_metric_bar_graph_id, "figure"),
    Input(dcc_country_dropdown_id, "value"),
    Input(dcc_col_picker_dropdown_id, "value"),
)
def plot_bar(country: str, metric: str) -> tuple[str, Figure]:
    if not country and metric:
        raise PreventUpdate

    title = f"Top Resort Metrics in {country} by {metric}"

    df = resorts.query("Country == @country").sort_values(metric, ascending=False)
    fig = px.bar(df, x="Resort", y=metric, custom_data=["Resort"]).update_xaxes(showticklabels=False)

    return title, fig


@app1.callback(
    Output(dbc_resort_name_card_id, "children"),
    Output(dbc_elevation_kpi_card_id, "children"),
    Output(dbc_price_kpi_card_id, "children"),
    Output(dbc_slope_kpi_card_id, "children"),
    Output(dbc_cannon_kpi_card_id, "children"),
    Input(dcc_metric_bar_graph_id, "hoverData"),
)
def update_line(hoverData) -> tuple[str, str, str, str, str]:
    resort = hoverData["points"][0]["customdata"][0]

    df = resorts.query("Resort == @resort")

    resort_name = df["Resort"]

    elev_rank = f"Elevation Rank: {int(df['country_elevation_rank'])}"
    price_rank = f"Price Rank: {int(df['country_price_rank'])}"
    slope_rank = f"Slope Rank: {int(df['country_slope_rank'])}"
    cannon_rank = f"Cannon Rank: {int(df['country_cannon_rank'])}"

    return resort_name, elev_rank, price_rank, slope_rank, cannon_rank


if __name__ == "__main__":
    app1.run_server(
        port=8080, debug=True
    )  # 可以指定 `host="0.0.0.0"` 或 `port=8051` 或 `debug=True` 或 `height=800` 或 `width="80%"`
