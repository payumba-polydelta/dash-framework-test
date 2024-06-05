import dash
from dash import Input, Output, State, callback
import dash_bootstrap_components as dbc
import pandas as pd
from helper import load_data, fileter_search


dash.register_page(__name__, path='/')

company_df, unique_industries, unique_states = load_data("fortune-500.csv")

layout  = dash.html.Div(
    className = "search-page-container",
    children = [
        dash.html.Div(
            className = "search-settings-container",
            children = [
                dash.html.Div("Company Selection Settings", className = "settings-header"),
                dash.html.Div(
                    className = "select-industries-container",
                    children = [
                        dash.html.Div("Inustries to Include in Search"), 
                        dash.dcc.Dropdown(id = "indluded-industries-multiselect", options = unique_industries, value = [], multi = True, placeholder = "Leave Blank to Select All", style = {"width": "100%", "backgroundColor": "#f0f0f0"})
                    ]
                ),
                dash.html.Div(
                    className = "tabs-border-container",
                    children = dash.dcc.Tabs(
                                   colors = {"border": "#000000", "primary": "#006ec7", "background": "#FFFFFF"},
                                   children = [
                                       dash.dcc.Tab(
                                           label = "Set Revenue Range",
                                           selected_style = {"color": "#006ec7"},
                                           children = dash.html.Div(
                                               className = "tab-content-container",
                                               children = [
                                                   dash.html.Div(
                                                       className = "single-input-column1",
                                                       children = [
                                                           dash.html.Div("Minimum Revenue (millions):"),
                                                           dash.dcc.Input(id = "min-revenue-input", type = "number", value = None, placeholder = "No Min")
                                                       ]
                                                   ),
                                                   dash.html.Div(
                                                       className = "single-input-column2",
                                                       children = [
                                                           dash.html.Div("Maximum Revenue (millions):"),
                                                           dash.dcc.Input(id = "max-revenue-input", type = "number", value = None, placeholder = "No Max")
                                                       ]
                                                   )
                                               ]
                                                      )
                                       ),
                                       dash.dcc.Tab(
                                           label = "Set Valuation Range",
                                           selected_style = {"color": "#006ec7"},
                                           children = dash.html.Div(
                                               className = "tab-content-container",
                                               children = [
                                                   dash.html.Div(
                                                       className = "single-input-column1",
                                                       children = [
                                                           dash.html.Div("Minimum Valuation (millions):"),
                                                           dash.dcc.Input(id = "min-valuation-input", type = "number", value = None, placeholder = "No Min")
                                                       ]
                                                   ),
                                                   dash.html.Div(
                                                       className = "single-input-column2",
                                                       children = [
                                                           dash.html.Div("Maximum Valuation (millions):"),
                                                           dash.dcc.Input(id = "max-valuation-input", type = "number", value = None, placeholder = "No Max")
                                                       ]
                                                   )
                                               ]
                                                      )
                                       ),                         
                                       dash.dcc.Tab(
                                           label = "Set Profit Range",
                                           selected_style = {"color": "#006ec7"},
                                           children = dash.html.Div(
                                               className = "tab-content-container",
                                               children = [
                                                   dash.html.Div(
                                                       className = "single-input-column1",
                                                       children = [
                                                           dash.html.Div("Minimum Profit (millions):"),
                                                           dash.dcc.Input(id = "min-profit-input", type = "number", value = None, placeholder = "No Min")
                                                       ]
                                                   ),
                                                   dash.html.Div(
                                                       className = "single-input-column2",
                                                       children = [
                                                           dash.html.Div("Maximum Profit (millions):"),
                                                           dash.dcc.Input(id = "max-profit-input", type = "number", value = None, placeholder = "No Max")
                                                       ]
                                                   )
                                               ]
                                                      )
                                       ),
                                   ]
                               )
                ),
                dash.html.Div(
                    className = "multi-input-container",
                    children = [
                        dash.html.Div(
                            className = "single-input-column1",
                            children = [
                                dash.html.Div("Minimum Number of Employees:"),
                                dash.dcc.Input(id = "min-employees-input", type = "number", value = None, placeholder = "No Min"),
                                dash.html.Div("Minimum Company Rank:", style = {"marginTop": 20}),
                                dash.dcc.Input(id = "min-rank-input", type = "number", value = None, placeholder = "No Min")
                            ]
                        ),
                        dash.html.Div(
                            className = "single-input-column2",
                            children = [
                                dash.html.Div("Maximum Number of Employees:"),
                                dash.dcc.Input(id = "max-employees-input", type = "number", value = None, placeholder = "No Max"),
                                dash.html.Div("Maximum Company Rank:", style = {"marginTop": 20}),
                                dash.dcc.Input(id = "max-rank-input", type = "number", value = None, placeholder = "No Max")
                            ]
                        )
                    ]
                ),
                dash.html.Div(
                    className = "accordian-container",
                    children = [
                        dbc.Accordion(
                            start_collapsed = True,
                            flush = True,
                            children = [
                                dbc.AccordionItem(
                                    title = "Additional Parameters",
                                    style = {"width": "100%"},
                                    children = [
                                        dash.html.Div(className = "select-industries-container",
                                                      children = [
                                                          dash.html.Div("States to Include in Search"), 
                                                          dash.dcc.Dropdown(id = "indluded-states-multiselect", options = unique_states, value = [], multi = True, placeholder = "Leave Blank to Select All", style = {"width": "100%", "backgroundColor": "#f0f0f0"}),
                                                          dash.html.Div("Max Number of Companies Returned (1-500)", style = {"marginTop": 20}), 
                                                          dash.dcc.Input(id = "max-companies-input", type = "number", value = 500)
                                                      ]
                                        )
                                    ]
                                )
                            ]
                        )
                    ]
                ),
                dash.html.Div(
                    className = "settings-submit-button",
                    children = dash.html.Button("Run Search", id = "settings-submit-button", n_clicks = 0, className = "settings-submit-button")
                )
            ]
        ),
        dash.html.Div(
            className = "search-result-container",
            children = [
                dash.html.Div(className = "results-header", id = "results-header"),
                dash.html.Div(className = "results-df-container", 
                              children = dash.dash_table.DataTable(
                                             data = company_df.to_dict('records'),
                                             id = "result-table", 
                                             fill_width = False,
                                             page_size = 15,
                                             style_table = {'overflowX': 'scroll'},
                                             style_cell = {'textAlign': 'left'}
                                         )
                )
            ]
        )
    ]
)

@callback (
    Output(component_id = "result-table", component_property = "data"),
    Output(component_id = "df-store", component_property = "data"),
    Output(component_id = "results-header", component_property = "children"),
    Input(component_id = "settings-submit-button", component_property = "n_clicks"),
    State(component_id = "indluded-industries-multiselect", component_property = "value"),
    State(component_id = "min-revenue-input", component_property = "value"),
    State(component_id = "max-revenue-input", component_property = "value"),
    State(component_id = "min-valuation-input", component_property = "value"),
    State(component_id = "max-valuation-input", component_property = "value"),
    State(component_id = "min-profit-input", component_property = "value"),
    State(component_id = "max-profit-input", component_property = "value"),
    State(component_id = "min-employees-input", component_property = "value"),
    State(component_id = "max-employees-input", component_property = "value"),
    State(component_id = "min-rank-input", component_property = "value"),
    State(component_id = "max-rank-input", component_property = "value"),
    State(component_id = "max-companies-input", component_property = "value"),
    State(component_id = "indluded-states-multiselect", component_property = "value"))
def update_table(number_of_clicks, indluded_industries_value, min_revenue_value, max_revenue_value, min_valuation_value, max_valuation_value, min_profit_value, max_profit_value, min_employees_value, max_employees_value, min_rank_value, max_rank_value, max_companies_value, indluded_states_value, search_df = company_df):
    new_df = fileter_search(search_df, min_rank_value, max_rank_value, indluded_industries_value, indluded_states_value, min_employees_value, max_employees_value, max_companies_value, min_revenue_value, max_revenue_value, min_valuation_value, max_valuation_value, min_profit_value, max_profit_value)
    new_df_dict = new_df.to_dict('records')
    #new_df_json = new_df.reset_index().to_json(orient="split")
    result_string = f"Result: There are {len(new_df)} Companies that Match Your Criteria"
    return new_df_dict, new_df_dict, result_string

