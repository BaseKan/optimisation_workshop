import dash_core_components as dcc
import dash_bootstrap_components as dbc
import dash_html_components as html

from app.custom_components import dropdown_input, checklist_input


dropdown_card = dbc.Card(
    [
        dbc.CardHeader('Selecteer steden', className='card-title bold'),
        dbc.CardBody(
            [
                # dropdown_input(id='dso-box2',
                #                label="Selecter netbeheerder",
                #                options=[
                #                     {'label': 'Liander', 'value': 'liander'},
                #                     {'label': 'Enexis', 'value': 'enexis'},
                #                     {'label': 'Stedin', 'value': 'stedin'},
                #                     {'label': 'Coteq', 'value': 'coteq'},
                #                     {'label': 'Westland-Infra', 'value': 'westland-infra'},
                #                     {'label': 'Enduris', 'value': 'enduris'},
                #                     {'label': 'Rendo', 'value': 'rendo'},
                #                 ],
                #                 placeholder = 'liander'
                # ),
                checklist_input(id='city-box',
                                             label="",
                                             options=[
                                                {'label': 'Amsterdam', 'value': 'AMSTERDAM'},
                                                {'label': 'Rotterdam', 'value': 'ROTTERDAM'},
                                                {'label': 'Utrecht', 'value': 'UTRECHT'},
                                                {'label': 'Maastricht', 'value': 'MAASTRICHT'},
                                                {'label': 'Driebergen', 'value': 'DRIEBERGEN-RIJSENBURG'}
                                             ],
                                ),
                dbc.Button(
                    "Haal data op",
                    id='submit-figure-data',
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
            id='calc-box2',
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

plot_card = dbc.Card(
    [
        dcc.Graph(id='timeseries-figure')
    ],
    className="p-1 shadow-sm"
)

right_column = dbc.Col(
    [
        plot_card
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