import dash
import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Output, Input
import plotly.express as px
import plotly.graph_objects as go
import dash_bootstrap_components as dbc
import pandas as pd

data = pd.read_csv("https://raw.githubusercontent.com/marija-grj/YACD/main/data/OxCGRT_latest.csv",dtype={'CountryCode':'string'})
data.loc[:,'Date'] = pd.to_datetime(data.Date, format='%Y-%m-%d')


app = dash.Dash(
    __name__, 
    external_stylesheets=[dbc.themes.LITERA], 
    meta_tags=[
        {'name':'viewport',
        'content':'width=device-width, initial-scale=1.0'}
    ]
)

app.layout = dbc.Container([
    dbc.Row([
        dbc.Col(html.H1("NPI", className="text-center text-primary, mb-4"), width=12)
    ]),
    dbc.Row([
        dbc.Col(
            dcc.Dropdown(id='dropdown-country-1', multi=False, value='Latvia',
                         options=[{'label':x, 'value':x}
                                  for x in sorted(data.CountryName.unique())
                                  ]
                         ),
            width=4
        )
    ], no_gutters=False, justify='center'),
     
     dbc.Row([
        dbc.Col(
            dcc.RadioItems(
                id="radio-data-1",
                options=[
                    {'label': 'Cumulative cases', 'value': 'ConfirmedCases'},
                    {'label': 'Daily cases', 'value': 'DailyCases'},
                    {'label': 'Cumulative 7-day-average', 'value': 'Average7'},
                    {'label': 'Cumulative 14-day-average', 'value': 'Average14'}
                ],
                value='Average7',
                labelStyle={'display': 'inline-block'},
                labelClassName="mr-4",
                className="text-center",
                inputClassName="mr-2"
            )
        )
    ]),
     dbc.Row([
         dbc.Col(
            dcc.RadioItems(
                id="radio-npi-1",
                options=[
                    {'label': 'Gatherings', 'value': 'C4_Restrictions on gatherings'},
                    {'label': 'School closing', 'value': 'C1_School closing'},
                    {'label': 'Workplace closing', 'value': 'C2_Workplace closing'}
                ],
                value='C4_Restrictions on gatherings',
                labelStyle={'display': 'inline-block'},
                labelClassName="mr-4",
                className="text-center",
                inputClassName="mr-2"
            )
         )
     ]),
     
     dbc.Row([
         dbc.Col(
             dcc.Graph(id='graph-1', figure={})
         )
     ])
])

dict_npi = {"C1_School closing":["No restrictions","Recommend closing","Require closing some levels","Require closing all levels"],
            "C2_Workplace closing":["No restrictions","Recommend closing","Require closing some sectors","Require closing all non-essential"],
            "C4_Restrictions on gatherings":["No restrictions","1001 or more people","101-1000 people","11-100 people","10 people or less"]
      }

@app.callback(
    Output('graph-1', 'figure'),
    Input('dropdown-country-1', 'value'),
    Input('radio-data-1', 'value'),
    Input('radio-npi-1','value')
)


def update_graph(country, column, npi):
    dataS = data[data.CountryName == country]
    x = data[(data.CountryName==country)]["Date"]
    y = data[(data.CountryName==country)][column]
    c = data[(data.CountryName==country)][npi]
    fig = go.Figure()
    for i in range(len(dict_npi[npi])):
        fig.add_trace(go.Bar(x=x[c==i], y=y[c==i], name=dict_npi[npi][i]))
    fig.update_layout(
        bargap=0,
        legend=dict(orientation="h",yanchor="bottom",y=1.02,xanchor="right", x=1),
        template="simple_white"
    )
    return fig

if __name__=='__main__':
    app.run_server(debug=True, port=3050)