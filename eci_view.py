from dash import Dash, html, dcc
import dash_bootstrap_components as dbc
from eci_model import df_qual, df_quant

# Specify HTML <head> elements
app = Dash(__name__,
           title="Confidence Intervals",
           update_title=None,
           external_stylesheets=[dbc.themes.BOOTSTRAP],
           meta_tags=[{"name": "viewport",
                       "content": "width=device-width, initial-scale=1.0, maximum-scale=1.0"}])

# Specify app layout (HTML <body> elements) using dash.html, dash.dcc and dash_bootstrap_components
# All component IDs should relate to the Input or Output of callback functions in eci_controller.py
app.layout = dbc.Container([
    # Quantitative instructions
    dbc.Row([
        html.H2("Confidence Intervals for quantitative variables"),
        html.P("Because of the large sample size, the confidence interval for the population mean of the variable of interest is quite narrow, even at the 99% confidence level. Select a variable from the dropdown list below to view upper and lower bounds for the actual value of its population mean.")
    ]),
    # Quantitative user input
    dbc.Row([
        dbc.Col([
            html.Div([
                dbc.Label("Variable",
                          className="label",
                          html_for="quant-dropdown"),
                dbc.Select(id="quant-dropdown",
                           options=[{"label": x, "value": x}
                                    for x in df_quant.columns[0:5]],
                           value="Total_happiness")
            ], **{"aria-live": "polite"}),
        ], xs=12, md=4, lg=3),
        dbc.Col([
            dbc.Label("Confidence level",
                      className="label",
                      html_for="quant-conf-value"),
            dcc.Slider(id="quant-conf-value",
                       value=0.95,
                       min=0.8,
                       max=0.99,
                       marks={0.8: {"label": "80%"},
                              0.85: {"label": "85%"}, 
                              0.9: {"label": "90%"}, 
                              0.95: {"label": "95%"},
                              0.99: {"label": "99%"}}),
        ], xs=12, md=8, lg=9)
    ]),
    # Quantitative Graph and Results
    dbc.Row([
        dbc.Col([
            # Graph components are placed inside a Div with role="img" to manage UX for screen reader users
            html.Div([
                dcc.Graph(id="quant-hist",
                          config={"displayModeBar": False,
                                  "doubleClick": False,
                                  "editable": False,
                                  "scrollZoom": False,
                                  "showAxisDragHandles": False})
            ], role="img", **{"aria-hidden": "true"}),
            html.Br(),
            # A second Div is used to associate alt text with the relevant Graph component to manage the experience for screen reader users, styled using CSS class sr-only
            html.Div(id="sr-hist",
                     children=[],
                     className="sr-only",
                     **{"aria-live": "polite"}),
        ], xs=12, lg=6),
        dbc.Col([
                dbc.Card([
                    dbc.CardBody([
                        html.Div([
                            html.H4("Results"),
                            html.P([
                                html.Span("Variable: ",
                                        className="bold-p"),
                                html.Span(id="quant-variable")
                            ]),
                            html.P([
                                html.Span("Sample mean: ",
                                        className="bold-p"),
                                html.Span(id="quant-mean")
                            ]),
                            html.P([
                                html.Span("Confidence interval for population mean: ",
                                        className="bold-p"),
                                html.Span(id="quant-conf-int")
                            ]),
                            html.P([
                                html.Span("Confidence level: ",
                                        className="bold-p"),
                                html.Span(id="quant-conf-level")
                            ])
                        ], **{"aria-live": "polite", "aria-atomic": "true"})
                    ])
                ])
        ], xs=12, lg=6)
    ]),
    # Qualitative instructions
    dbc.Row([
        html.H2("Confidence Intervals for qualitative variables"),
        html.P("When calculating confidence intervals for qualitative data, we are investigating if the probability of observing a specific characteristic is evenly distributed between categories, or if there are significant differences in the proportions in each category. For example, is a student completing the Happy questionnaire equally likely to be male or female? Select a variable from the dropdown list to view the observed proportions in each category, and compare this to categories with equal proportions.")
    ]),
    # Qualitative user input
    dbc.Row([
        dbc.Col([
            html.Div([
                dbc.Label("Variable",
                          className="label",
                          html_for="qual-dropdown"),
                dbc.Select(id="qual-dropdown",
                           options=[{"label": x, "value": x}
                                        for x in df_qual.columns[1:6]],
                           value="Sex")
            ], **{"aria-live": "polite"}),
            html.Div([
                dbc.Label("Category",
                          className="label",
                          html_for="cat-radio"),
                dcc.RadioItems(id="cat-radio",
                               options=[],
                               labelStyle={"margin-left": 10},
                               inputStyle={"margin-right": 10})
            ], **{"aria-live": "polite"})
        ], xs=12, sm=12, md=4, lg=3, xl=3),
        dbc.Col([
            dbc.Label("Confidence level",
                      className="label",
                      html_for="qual-conf-value"),
            dcc.Slider(id="qual-conf-value",
                       value=0.95,
                       min=0.8,
                       max=0.99,
                       marks={0.8: {"label": "80%"},
                              0.85: {"label": "85%"},
                              0.9: {"label": "90%"},
                              0.95: {"label": "95%"},
                              0.99: {"label": "99%"}}),
        ], xs=12, sm=12, md=8, lg=9, xl=9)
    ]), 
    # Qualitative Graph and Results
    dbc.Row([
        dbc.Col([
            html.Div([
                dcc.Graph(id="qual-bar",
                          config={"displayModeBar": False,
                                  "doubleClick": False,
                                  "editable": False,
                                  "scrollZoom": False,
                                  "showAxisDragHandles": False})
            ], role="img", **{"aria-hidden": "true"}),
            html.Br(),
            html.Div(id="sr-bar",
                     children=[],
                     className="sr-only",
                     **{"aria-live": "polite"})
        ], xs=12, lg=6),
        dbc.Col([
                dbc.Card([
                    dbc.CardBody([
                        html.Div([
                            html.H4("Results"),
                            html.P([
                                html.Span("Variable: ",
                                        className="bold-p"),
                                html.Span(id="qual-variable")
                            ]),
                            html.P([
                                html.Span(id="qual-cat1", className="bold-p"),
                                html.Span(id="count-cat1")
                            ]),
                            html.P([
                                html.Span(id="qual-cat2", className="bold-p"),
                                html.Span(id="count-cat2")
                            ]),
                            html.P([
                                html.Span("Total count: ", className="bold-p"),
                                html.Span(id="qual-n-cat1")
                            ]),
                            html.P([
                                html.Span(id="ci-cat1", className="bold-p"),
                                html.Span(id="qual-ci-result")
                            ]),
                            html.P([
                                html.Span("Confidence level: ", className="bold-p"),
                                html.Span(id="qual-conf-level")
                            ])
                        ], **{"aria-live": "polite", "aria-atomic": "true"})
                    ])
                ])
        ], xs=12, lg=6)
    ])
], fluid=True)
