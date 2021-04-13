import dash_core_components as dcc
import dash_bootstrap_components as dbc
import dash_html_components as html

from app.custom_components import dropdown_input
from dash_table import DataTable


dropdown_card = dbc.Card(
    [
        dbc.CardHeader('Kies jaar en netbeheerder', className='card-title bold'),
        dbc.CardBody(
            [
                dropdown_input(id='year-box',
                             label="Selecteer jaar",
                             options=[
                                 {'label': '2020', 'value': 2020},
                                 {'label': '2019', 'value': 2019},
                                 {'label': '2018', 'value': 2018},
                                 {'label': '2017', 'value': 2017},
                             ],
                             placeholder=2020
                ),
                dropdown_input(id='dso-box',
                               label="Selecteer netbeheerder",
                               options=[
                                    {'label': 'Liander', 'value': 'liander'},
                                    {'label': 'Enexis', 'value': 'enexis'},
                                    {'label': 'Stedin', 'value': 'stedin'},
                                    {'label': 'Coteq', 'value': 'coteq'},
                                    {'label': 'Westland-Infra', 'value': 'westland-infra'},
                                    {'label': 'Enduris', 'value': 'enduris'},
                                    {'label': 'Rendo', 'value': 'rendo'},
                                ],
                                placeholder = 'liander'
                ),
                dbc.Button(
                    "Haal data op",
                    id='submit-table-data',
                    color='primary',
                    className='mr-1 w-100'
                )
            ]
        )
    ],
    className='mb-3'
)

rekentijd_card = dbc.Card([
    dbc.CardHeader('Rekentijd', className='card-title bold'),
    dbc.CardBody([
        html.Div(
            id='calc-box1',
            className="content_box_content"
        )
    ])
])

sidebar = dbc.Col(
    [
        dropdown_card,
        rekentijd_card
    ],
    className='col-3'
)

table_card = dbc.Card(
    [
        DataTable(id="dso-table",
                  columns = [{'name': i, 'id':i } for i in ['Stad', 'Jaarverbruik (MWh)']],
                  data = [{}])
    ],
    className="p-1 shadow-sm"
)

right_column = dbc.Col(
    [
        table_card
    ],
    className='col-9'
)

content = dbc.Container([
        dbc.Row([
            sidebar,
            right_column],
            className="pl-3 pr-3 mt-3"
            )
        ],
        className="p-0",
        style={"max-width": "1920px"},
    )