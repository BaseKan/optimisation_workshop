#!/usr/bin/env python
# -*- coding: utf-8 -*-


import dash
import dash_core_components as dcc
import dash_bootstrap_components as dbc
import dash_html_components as html
from dash.dependencies import Input, Output, State

import plotly.express as px

from app.ETL import load_data_from_file, load_timeseries_data, calculate_top_ten, calculate_timeseries
from app import page_jaarverbruik, page_tijdreeks
import time

external_stylesheets = ["https://bootswatch.com/4/flatly/bootstrap.css"]

app = dash.Dash(__name__, external_stylesheets=external_stylesheets)

overhead_bar = dbc.NavbarSimple(
    children = [dbc.NavItem(dbc.NavLink("Stedelijk Jaarverbruik", href='/jaarverbruik', active="exact")),
                dbc.NavItem(dbc.NavLink("Verbruik over de jaren", href='/tijdreeks', active="exact"))],
    brand='EnergieNL v0.1.0',
    color='primary',
    dark=True
)

content = html.Div(id='page-content', children=[])

app.layout = html.Div([
    dcc.Location(id='url'),
    overhead_bar,
    content
])

@app.callback(Output('page-content','children'),
              [Input('url','pathname')])

def render_page_content(pathname):
    if pathname == "/" or pathname == '/jaarverbruik':
        return page_jaarverbruik.content

    elif pathname == '/tijdreeks':
        return page_tijdreeks.content

    else:
        return dbc.Jumbotron(
        [
            html.H1("404: Not found", className="text-danger"),
            html.Hr(),
            html.P(f"The pathname {pathname} was not recognised..."),
        ]
    )

@app.callback(Output("dso-table", "data"),
              Output('calc-box1', 'children'),
              Input("submit-table-data", 'n_clicks'),
              State("year-box", "value"),
              State("dso-box", "value"))

def update_dso_table(n_clicks, year, dso):
    start = time.time()
    df = load_data_from_file(datapath='C:/Data/Code/EnergieKaart/data/Electricity',filename=dso+'_electricity_'+str(year)+'.csv')
    df = calculate_top_ten(df=df)
    end = time.time()
    rekentijd_str = str(round(end-start,3))+' seconden'
    return df.to_dict('records'), rekentijd_str

@app.callback(Output("timeseries-figure", "figure"),
              Output('calc-box2', 'children'),
              Input("submit-figure-data", 'n_clicks'),
              State("city-box", "value"))

def update_timeseries_figure(n_clicks, cities):
    start = time.time()
    df_elec = load_timeseries_data()
    df_gas = load_timeseries_data(type='Gas')
    df = calculate_timeseries(df_elec=df_elec,df_gas=df_gas, cities=cities)
    fig = px.line(df.sort_values('Jaar'), x='Jaar', y='Gemiddeld_verbruik', color='Stad')
    end = time.time()
    rekentijd_str = str(round(end-start,3))+' seconden'
    return fig, rekentijd_str


if __name__ == "__main__":
    app.run_server(debug=False)
