import dash_bootstrap_components as dbc
import dash_core_components as dcc


def number_input(id: str, label: str, placeholder: float = None):
    return dbc.FormGroup(
        [
            dbc.Label(label),
            dbc.Input(
                id=id,
                type="number",
                placeholder=placeholder,
                value=placeholder,
            ),
        ]
    )

def dropdown_input(id: str, label: str, options: list, placeholder = None):
    return dbc.FormGroup(
        [
            dbc.Label(label),
            dcc.Dropdown(
                id=id,
                options=options,
                value=placeholder,
            ),
        ]
    )


def checklist_input(id: str, label: str, options: list, placeholder = []):
    return dbc.FormGroup(
        [
            dbc.Label(label),
            dcc.Checklist(
                id=id,
                options=options,
                value=placeholder,
                labelStyle = {'display': 'block'}
            ),
        ]
    )