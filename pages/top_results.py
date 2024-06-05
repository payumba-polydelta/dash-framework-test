import dash
from dash import Input, Output, callback
import pandas as pd
import plotly.express as px


dash.register_page(__name__)


layout = dash.html.Div(
    className = "result-page-container",
    children = [
        dash.html.Div(
            className = "top-result-slider-container",
            children = [
                dash.html.Div("Choose Number of Top Results to Graph", style = {"margin-bottom": 20}),
                dash.dcc.Slider(id = "num-graphed-slider",
                                min = 1,
                                step = 1
                )
            ]
        ),
        dash.html.Div(
            className = "results-tabs-border-container",
            children = dash.dcc.Tabs(
                colors = {"border": "#000000", "primary": "#006ec7", "background": "#FFFFFF"},
                parent_style = {"width": "100%"},
                children = [
                    dash.dcc.Tab(
                        label = "Revenue",
                        selected_style = {"color": "#006ec7"},
                        children = [
                            dash.html.Div(
                                className = "result-graph-tab-content",
                                children = [
                                    dash.html.Div("Revenue Graphs"),
                                    dash.dcc.Graph(
                                        id = "revenue-graphs",
                                        style = {"width" : "100%", "hight": "70%"}
                                    )
                                ]
                            )
                        ]
                    ),
                    dash.dcc.Tab(
                        label = "Valuation",
                        selected_style = {"color": "#006ec7"},
                        children = [
                            dash.html.Div(
                                className = "result-graph-tab-content",
                                children = [
                                    dash.html.Div("Valuation Graphs"),
                                    dash.dcc.Graph(
                                        id = "valuation-graphs",
                                        style = {"width" : "100%", "hight": "70%"}
                                    )
                                ]
                            )
                        ]
                    ),
                    dash.dcc.Tab(
                        label = "Profits",
                        selected_style = {"color": "#006ec7"},
                        children = [
                            dash.html.Div(
                                className = "result-graph-tab-content",
                                children = [
                                    dash.html.Div("Profits Graphs"),
                                    dash.dcc.Graph(
                                        id = "profit-graphs",
                                        style = {"width" : "100%", "hight": "70%"}
                                    )
                                ]
                            )
                        ]
                    ),
                    dash.dcc.Tab(
                        label = "Profits Percentage of Sales",
                        selected_style = {"color": "#006ec7"},
                        children = [
                            dash.html.Div(
                                className = "result-graph-tab-content",
                                children = [
                                    dash.html.Div("Profits Percentage of Sales Graphs"),
                                    dash.dcc.Graph(
                                        id = "percent-profits-graphs",
                                        style = {"width" : "100%", "hight": "70%"}
                                    )
                                ]
                            )
                        ]
                    ),
                    dash.dcc.Tab(
                        label = "Number of Employees",
                        selected_style = {"color": "#006ec7"},
                        children = [
                            dash.html.Div(
                                className = "result-graph-tab-content",
                                children = [
                                    dash.html.Div("Number of Employees Graphs"),
                                    dash.dcc.Graph(
                                        id = "num-employees-graphs",
                                        style = {"width" : "100%", "hight": "70%"}
                                    )
                                ]
                            )
                        ]
                    )
                ]
            )
        )
    ]
)


@callback (
    Output(component_id = "num-graphed-slider", component_property = "max"),
    Output(component_id = "num-graphed-slider", component_property = "value"),
    Input(component_id = "df-store", component_property = "data"))
def load_filter_df(stored_df):
    df = pd.DataFrame(stored_df)
    slider_max = min(20, len(df))
    return slider_max, slider_max

@callback (
    Output(component_id = "revenue-graphs", component_property = "figure"),
    Output(component_id = "valuation-graphs", component_property = "figure"),
    Output(component_id = "profit-graphs", component_property = "figure"),
    Output(component_id = "percent-profits-graphs", component_property = "figure"),
    Output(component_id = "num-employees-graphs", component_property = "figure"),
    Input(component_id = "df-store", component_property = "data"),
    Input(component_id = "num-graphed-slider", component_property = "value"))
def set_graphs(stored_df, num_companies):
    df = pd.DataFrame(stored_df)
    sliced_df = df[:num_companies]
    revenue_graph = px.bar(sliced_df, x = "Company", y = "Revenue (millions)", color_discrete_sequence = ["#006ec7"])
    valuation_graph = px.bar(sliced_df, x = "Company", y = "Valuation (millions)", color_discrete_sequence = ["#006ec7"])
    profit_graph = px.bar(sliced_df, x = "Company", y = "Profits (millions)", color_discrete_sequence = ["#006ec7"])
    profit_percent_sales_graph = px.bar(sliced_df, x = "Company", y = "Profits (% of Sales)", color_discrete_sequence = ["#006ec7"])
    num_employees_graph = px.bar(sliced_df, x = "Company", y = "Number of Employees", color_discrete_sequence = ["#006ec7"])
    return revenue_graph, valuation_graph, profit_graph, profit_percent_sales_graph, num_employees_graph

