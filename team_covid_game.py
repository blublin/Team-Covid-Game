# Run this app with `python app.py` and
# visit http://127.0.0.1:8050/ in your web browser.
# Authors: Maria Gorbunova, Ben Lublin, Caetano Brito, Julian Pearson Rickenbach
# Date: 2/20/2021 11:51 PM

# pip install dash
# pip install dash_bootstrap_components
# pip install wget
# pip install plotly --upgrade

import dash
import dash_core_components as dcc
import dash_html_components as html
import dash_bootstrap_components as dbc
import plotly.express as px
import plotly.graph_objects as go

import pandas as pd
import tkinter.messagebox as tkmb

from pathlib import Path
import wget
#-----------------------------------------

external_stylesheets = ['https://codepen.io/chriddyp/pen/bWLwgP.css']
app = dash.Dash(__name__, external_stylesheets=external_stylesheets)

colors = {
    'background': 'rgba(0,0,0,0)',
    'text': '#7FDBFF',
    'dashbg' : 'rgb(39, 39, 74)',
    'dashcompbg' : 'rgb(158, 158, 163)'
}


#------------------------------------------------
# Check if file exists. Get from site if doesn't.
_file = 'daily.csv'
data_file = Path(_file)
if not data_file.exists():
    # Get CSV file
    url = f"https://api.covidtracking.com/v1/states/{_file}"
    wget.download(url)

# Convert CSV file to panda DataFrame
fh = pd.read_csv(_file, 
                 usecols=['date',
                          'deathConfirmed',
                          'hospitalizedCurrently',
                          'negative',# unused
                          'positive',
                          'recovered',# unused
                          'state',
                          'totalTestResults' # unused
                         ],
                 index_col='state'
                )

# Remove territories
fh = fh.drop( labels=['AS','GU','MP','PR','VI'] )

# Convert dates to string and separate into year-month-day
fh['date'] = fh['date'].astype(str)
fh['date'].replace(to_replace="(202[0-1])([0-1][0-9])([0-3][0-9])", value=r"\1-\2-\3", regex=True, inplace=True)

# Replace NULL with 0
fh['deathConfirmed'] = fh['deathConfirmed'].fillna(0)
fh['hospitalizedCurrently'] = fh['hospitalizedCurrently'].fillna(0)

# Sort by Descending dates
fh = fh.sort_values(by='date', ascending=True)
print(fh.head())
# Create Choropleth map
fig = px.choropleth(fh,
                    locations=fh.index,
                    scope="usa",
                    locationmode="USA-states",
                    color='positive',
                    hover_data=['positive','hospitalizedCurrently','deathConfirmed'],
                    animation_frame=fh['date'],
                    color_continuous_scale=px.colors.sequential.thermal)

# Set title
fig.update_layout(title_text='Spread of Coronavirus in Continental United States',
                  height=800,
                  plot_bgcolor=colors['background'],
                  paper_bgcolor=colors['background'],
                  geo={
                  'bgcolor':colors['background']
                  },
                  font_color=colors['text']
                  )

# Set resolution (world scale) to 1:110
fig.update_geos(resolution=110)

# Change frame time and transition time (in milliseconds)
fig.layout.updatemenus[0].buttons[0].args[1]['frame']['duration'] = 20
fig.layout.updatemenus[0].buttons[0].args[1]['transition']['duration'] = 5

# fig.show()
#-----------------------------------------------------------

state_dd = dcc.Dropdown(
    id='demo-dropdown',
    options=[
        {'label':'Alabama', 'value':  'AL'},
        {'label':'Alaska', 'value':  'AK'},
        {'label':'Arizona', 'value':  'AZ'},
        {'label':'Arkansas', 'value':  'AR'},
        {'label':'California', 'value':  'CA'},
        {'label':'Colorado', 'value':  'CO'},
        {'label':'Connecticut', 'value':  'CT'},
        {'label':'Delaware', 'value':  'DE'},
        {'label':'Florida', 'value':  'FL'},
        {'label':'Georgia', 'value':  'GA'},
        {'label':'Hawaii', 'value':  'HI'},
        {'label':'Idaho', 'value':  'ID'},
        {'label':'Illinois', 'value':  'IL'},
        {'label':'Indiana', 'value':  'IN'},
        {'label':'Iowa', 'value':  'IA'},
        {'label':'Kansas', 'value':  'KS'},
        {'label':'Kentucky', 'value':  'KY'},
        {'label':'Louisiana', 'value':  'LA'},
        {'label':'Maine', 'value':  'ME'},
        {'label':'Maryland', 'value':  'MD'},
        {'label':'Massachusetts', 'value':  'MA'},
        {'label':'Michigan', 'value':  'MI'},
        {'label':'Minnesota', 'value':  'MN'},
        {'label':'Mississippi', 'value':  'MS'},
        {'label':'Missouri', 'value':  'MO'},
        {'label':'Montana', 'value':  'MT'},
        {'label':'Nebraska', 'value':  'NE'},
        {'label':'Nevada', 'value':  'NV'},
        {'label':'New Hampshire', 'value':  'NH'},
        {'label':'New Jersey', 'value':  'NJ'},
        {'label':'New Mexico', 'value':  'NM'},
        {'label':'New York', 'value':  'NY'},
        {'label':'North Carolina', 'value':  'NC'},
        {'label':'North Dakota', 'value':  'ND'},
        {'label':'Ohio', 'value':  'OH'},
        {'label':'Oklahoma', 'value':  'OK'},
        {'label':'Oregon', 'value':  'OR'},
        {'label':'Pennsylvania', 'value':  'PA'},
        {'label':'Rhode Island', 'value':  'RI'},
        {'label':'South Carolina', 'value':  'SC'},
        {'label':'South Dakota', 'value':  'SD'},
        {'label':'Tennessee', 'value':  'TN'},
        {'label':'Texas', 'value':  'TX'},
        {'label':'Utah', 'value':  'UT'},
        {'label':'Vermont', 'value':  'VT'},
        {'label':'Virginia', 'value':  'VA'},
        {'label':'Washington', 'value':  'WA'},
        {'label':'West Virginia', 'value':  'WV'},
        {'label':'Wisconsin', 'value':  'WI'},
        {'label':'Wyoming', 'value':  'WY'} 
    ],
    style={
    'backgroundColor' : colors['dashbg'],
    'color': colors['text']
    },
    value="Select a state to modify variables"
)

switches = dbc.FormGroup(
    [
        dbc.Checklist(
            options=[
                {"label": "Goverment enforces masks in stores", "value": "gems"},
                {"label": "Goverment enforces masks in stores", "value": "gemo"},
                {"label": "Government enforces Stay-At-Home order", "value": "gesah"},
                {"label": "Government does PSA about CDC's recommendations", "value": "gcdc"},
                {"label": "Citizens wear disposable masks", "value": "cdm"},
                {"label": "Citizens wear reusable masks", "value": "crm"},
                {"label": "Citizens wear gloves", "value": "cg"},
                {"label": "Citizens use hand sanitizer", "value": "chs"},
                {"label": "Citizens care about social distancing", "value": "csd"},
            ],
            id="df-checklist",
            value=[],
            style={
                'textAlign': 'center',
                'color': colors['text']
            },
            labelStyle={"display": "inline-block"},
            switch=True,
            inline=True,
        ),
    ]
)

app.layout = html.Div(
    style={
        'backgroundColor': colors['dashbg']
        },
    children=[
        html.H1(
            children='The Covid Game',
            style={
                'textAlign': 'center',
                'color': colors['text']
            }
        ),

        dcc.Graph(
            id='COVID timeline map',
            figure=fig
        ),
    
        state_dd,
        switches
    ]
)

if __name__ == '__main__':
    
    app.run_server(debug=False)