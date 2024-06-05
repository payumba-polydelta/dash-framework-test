
import dash
from dash import Input, Output, State, callback
import dash_bootstrap_components as dbc
import pandas as pd
from helper import load_data, fileter_search

app = dash.Dash(__name__, external_stylesheets = [dbc.themes.BOOTSTRAP], use_pages = True)

logo_path = "assets/pd_logo_dark_mode.png"

company_df, unique_industries, unique_states = load_data("fortune-500.csv")
search_page_clicks = [0]

app.layout = dbc.Container(
    style = {"max-width": "100%", "width": "100%", "margin": 0, "padding": 0},
    children = [
        dash.html.Div(
            className = "page-layout",
            children = [
                dash.dcc.Store(id = "df-store", storage_type = "session"),
                dash.html.Div(
                    className = "page-header",
                    children = [
                        dash.html.H1("Fortune 500 Query Tool"),
                        dash.html.Img(src = logo_path, width = "280px")
                    ]
                ),
                dash.html.Div(
                    className = "page-sidebar",
                    children = [
                        dash.dcc.Link(
                            href = "/",
                            children = dash.html.Button("Configure Search", id = "search-page", n_clicks = 0, className = "active-page-button")   
                        ),
                        dash.dcc.Link(
                            href = dash.page_registry['pages.top_results']['path'],
                            children = dash.html.Button("Top Results", id = "top-results-page", n_clicks = 0, className = "page-button")
                        )
                    ]
                ),
                dash.html.Div(
                    className = "main-content-area",
                    children = dash.page_container
                )
            ]
        )
    ]
)


@callback(
    Output(component_id = "search-page", component_property = "className"),
    Output(component_id = "top-results-page", component_property = "className"),
    Input(component_id = "search-page", component_property = "n_clicks"),
    Input(component_id = "top-results-page", component_property = "n_clicks"),
    prevent_initial_call = True)
def activate_page_button(num_search_page_clicks, num_top_result_page_clicks, save_search_page_clicks = search_page_clicks):
    if num_search_page_clicks > save_search_page_clicks[0]:
        save_search_page_clicks[0] += 1
        return "active-page-button", "page-button"
    else:
        return "page-button", "active-page-button"


if __name__ == "__main__":
    app.run(host = '127.0.0.1', port = '8050', debug = True, dev_tools_hot_reload=True)
    
