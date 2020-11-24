import dash
import dash_core_components as dcc 
import dash_html_components as html 
import yfinance as yf
from dash.dependencies import Input, Output
from dash.exceptions import PreventUpdate
import pandas as pd
import plotly.graph_objects as go

def get_stock_price_fig(df):
    fig = go.Figure()
    fig.add_trace(go.Scatter(mode= "lines", x = df["Date"], y = df["Close"]))
    return fig

def get_donut_graphs(df, label):
    non_main = 1 - df.values[0]
    labels =["main", label]
    values =[non_main, df]
    fig = go.Figure(data=[go.Pie(labels=labels, values=values, hole= 0.499)])
    return fig

app = dash.Dash()

app.layout = html.Div([
    html.Div([
        html.P("Choose the Company  to Start", className= "start"),
        dcc.Dropdown("dropdown_tickers", options= [
            {"label":"Apple", "value":"AAPL"},
            {"label":"Tesla", "value":"TSLA"},
            {"label":"Facebook", "value":"FB"},
            ]),
            html.Div([
                html.Button("Stock Price", className="stock-btn", id="stock"),
            ], className= "buttons")


    ], className= "navigation"),

    html.Div([
        html.Div([
            html.P(id="ticker"),
            html.Img(id="logo")], className="header"),

        html.Div(id= "description", className= "company_description"),
        html.Div([
            html.Div([],id="graph_contents")
        ], id= "main_content")
        ],className="content")
], className= "container")

@app.callback(
    [Output("description", "children"), Output("logo", "src"), Output("ticker", "children")],
    [Input("dropdown_tickers", "value")]
)
def update_content(v):
    if v == None:
        raise PreventUpdate
    ticker = yf.Ticker(v)
    inf = ticker.info
    df= pd.DataFrame().from_dict(inf, orient="index").T
    df = df[["logo_url", "shortName", "longBusinessSummary"]]
    return df["longBusinessSummary"].values[0], df["logo_url"].values[0], df["shortName"].values[0]

@app.callback(
    [Output("graph_contents", "children")],
    [Input("stock","n_clicks"), Input("dropdown_tickers","value")]
)

def stock_price(v, v2):
    if v==None:
        raise PreventUpdate
    df = yf.download(v2)
    df.reset_index(inplace= True)
    fig = get_stock_price_fig(df)
    return [dcc.Graph(figure=fig)]

app.run_server(debug=True)