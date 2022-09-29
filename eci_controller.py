from dash import Input, Output
import numpy as np
import plotly.graph_objects as go
from eci_model import get_df_qual, get_df_quant, df_qual, quant_y_range
from eci_view import app

# app.callback Outputs and Inputs are all associated with unique elements in *_view.py though the first argument (component_id) and control/are controlled by the second argument (component_property)


# Callback function to update histogram, results and screen reader text based on user entry values (quantitative variable dropdown and confidence level)
@app.callback(
    # Graph Outputs
    Output("quant-hist", "figure"),
    Output("sr-hist", "children"),
    # Results Outputs
    Output("quant-variable", "children"),
    Output("quant-mean", "children"),
    Output("quant-conf-int", "children"),
    Output("quant-conf-level", "children"),
    # Inputs
    Input("quant-dropdown", "value"),
    Input("quant-conf-value", "value")
)
def update_histogram(value, conf_level):
    df, mean, conf_int = get_df_quant(value, conf_level)
    fig = go.Figure(
        go.Histogram(x=df,
                     name=value,
                     hoverinfo="name+y",
                     showlegend=False))
    fig.update_traces(marker_line_color="rgba(158,171,5,1)",
                      marker_color="rgba(158,171,5,0.5)",
                      marker_line_width=1)
    fig.update_yaxes(title_text=None,
                     range=[0, quant_y_range[value]])
    fig.update_layout(margin=dict(t=20, b=10, l=20, r=20),
                      font_size=14,
                      dragmode=False)
    add_ci_lines(fig, value, conf_int[0], conf_int[1])
    # Screen reader text
    sr_hist = f"Histogram of {value} with confidence interval ({conf_int[0]:.3f}, {conf_int[1]:.3f})"
    return fig, sr_hist, f"{value}", f"{mean:.3f}", f"({conf_int[0]:.3f}, {conf_int[1]:.3f})", f"{conf_level:.0%}"


# Add graph lines to histogram for confidence interval lower/upper bounds
def add_ci_lines(fig, value, ci_lower, ci_upper):
    y = np.linspace(0, quant_y_range[value], 10)
    fig.add_trace(
        go.Scatter(x=[ci_lower] * 10,
                   y=y,
                   marker_opacity=0,
                   marker_color="#0085a1",
                   name="Confidence<br>interval<br>(upper/lower<br>bounds)",
                   hovertemplate="CI lower bound: %{x:.3f}<extra></extra>"))
    fig.add_trace(
        go.Scatter(x=[ci_upper] * 10,
                   y=y,
                   marker_opacity=0,
                   marker_color="#0085a1",
                   hovertemplate="CI upper bound: %{x:.3f}<extra></extra>",
                   showlegend=False))
    return fig


# Callback function to update category radio buttons based on qualitative dropdown user selection
@app.callback(
    Output("cat-radio", "options"),
    Output("cat-radio", "value"),
    Input("qual-dropdown", "value")
)
def set_categories(value):
    df = df_qual[value]
    categories = df.unique()
    cat1 = categories[0]
    cat2 = categories[1]
    return [{"label": cat1, "value": cat1}, {"label": cat2, "value": cat2}], cat1


# Callback function to update bar chart, results and associated screen reader text based on qualitative variable dropdown/category radio button and confidence level user selection
@app.callback(
    # Graph Outputs
    Output("qual-bar", "figure"),
    Output("sr-bar", "children"),
    # Results Outputs
    Output("qual-variable", "children"),
    Output("qual-cat1", "children"),
    Output("count-cat1", "children"),
    Output("qual-cat2", "children"),
    Output("count-cat2", "children"),
    Output("qual-n-cat1", "children"),
    Output("ci-cat1", "children"),
    Output("qual-ci-result", "children"),
    Output("qual-conf-level", "children"),
    # Inputs
    Input("qual-dropdown", "value"),
    Input("qual-conf-value", "value"),
    Input("cat-radio", "value")
)
def update_bar(value, conf_level, category):
    x, y1, y2, y1_range, y2_range, cat1, cat2, conf_int = get_df_qual(value, conf_level, category)
    # Stacked bar chart - users can compare the bar of observed results against a bar displaying equal proportions
    fig = go.Figure(data=[go.Bar(name=cat1,
                                 x=x,
                                 y=y1_range,
                                 marker_color="#d10373",
                                 marker_opacity=0.6),
                          go.Bar(name=cat2,
                                 x=x,
                                 y=y2_range,
                                 marker_color="#9eab05",
                                 marker_opacity=0.6)])
    fig.update_layout(barmode="stack",
                      margin=dict(t=20, b=10, l=20, r=20),
                      font_size=14,
                      dragmode=False)
    fig.update_yaxes(title_text=None,
                     range=[0, (y1+y2)+1])
    # fig.add_shape to add lower/upper bounds for confidence interval - hovertext not available
    fig.add_shape(type="line",
                  xref="paper",
                  yref="paper",
                  x0=0,
                  y0=conf_int[0],
                  x1=1,
                  y1=conf_int[0],
                  line=dict(color="#0085a1",
                            width=2))
    fig.add_shape(type="line",
                  xref="paper",
                  yref="paper",
                  x0=0,
                  y0=conf_int[1],
                  x1=1,
                  y1=conf_int[1],
                  line=dict(color="#0085a1",
                            width=2))
    # Screen reader text
    sr_bar = f"Barchart of {value} with confidence interval for {cat1} ({conf_int[0]*(y1+y2):.2f}, {conf_int[1]*(y1+y2):.2f}"
    return fig, sr_bar, value, f"Count of {cat1}: ", y1, f"Count of {cat2}: ", y2, y1+y2, f"Confidence interval for {cat1}: ", f"({conf_int[0]*(y1+y2):.2f}, {conf_int[1]*(y1+y2):.2f})", f"{conf_level:.0%}"


if __name__ == "__main__":
    app.run(debug=True)
    # To deploy on Docker, replace app.run(debug=True) with the following:
    # app.run(debug=False, host="0.0.0.0", port=8080, dev_tools_ui=False)
