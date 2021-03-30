import dash
import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Output, Input
import plotly.express as px
import plotly.graph_objects as go
import dash_bootstrap_components as dbc
import pandas as pd

df = pd.read_csv('https://raw.githubusercontent.com/Coding-with-Adam/Dash-by-Plotly/master/Bootstrap/Side-Bar/iranian_students.csv')

data = pd.read_csv("https://raw.githubusercontent.com/marija-grj/YACD/main/data/OxCGRT_latest.csv",dtype={'CountryCode':'string'})
data.loc[:,'Date'] = pd.to_datetime(data.Date, format='%Y-%m-%d')

#  -------------------------------------------------------------------------------------

app = dash.Dash(__name__, external_stylesheets=[dbc.themes.FLATLY],
                suppress_callback_exceptions = True)

#  -------------------------------------------------------------------------------------

# styling the sidebar
SIDEBAR_STYLE = {
    "position": "fixed",
    "top": 0,
    "left": 0,
    "bottom": 0,
    "width": "16rem",
    "padding": "2rem 1rem",
    "background-color": "#f8f9fa",
}

# padding for the page content
CONTENT_STYLE = {
    "margin-left": "18rem",
    "margin-right": "2rem",
    "padding": "2rem 1rem",
}

#  -------------------------------------------------------------------------------------

sidebar = html.Div(
    [
        html.H2("Group R", className="display-4"),
        html.Hr(),
        html.P(
            "Select a country", className="lead"
        ),
        dcc.Dropdown(
            id='dropdown-country-1', multi=False, value='Latvia',
            options=[{'label':x, 'value':x}
                     for x in sorted(data.CountryName.unique())
                     ]
        ),
        html.Hr(),
        dbc.Nav(
            [
                dbc.NavLink("Dynamics", href="/dynamics", active="exact"),
                dbc.NavLink("Interventions", href="/interventions", active="exact"),
                dbc.NavLink("Global Context", href="/global-context", active="exact"),
            ],
            vertical=True,
            pills=True,
        ),
    ],
    style=SIDEBAR_STYLE,
)

content = html.Div(id="page-content", children=[], style=CONTENT_STYLE)

#  -------------------------------------------------------------------------------------

# -= Page 1 =-

page_dynamics = html.Div([
    html.H1('Covid-19 Dynamics',className="display-4",
            style={'textAlign':'center'}),
    html.Hr(),
    dbc.RadioItems(
        id="radio-data-row1",
        options=[
            {'label': 'Cases', 'value': 'Cases'},
            {'label': 'Deaths', 'value': 'Deaths'},
            {'label': 'Tests', 'value': 'Tests'},
            {'label': 'Vaccinations', 'value': 'Vaccine'},
        ],
        value='Cases',
        labelClassName="mr-4",
        className="text-center lead",
        inline=True,
        inputClassName="mr-2"
    ),
        dbc.RadioItems(
        id="radio-data-row2",
        options=[
            {'label': 'Cumulative', 'value': 'Cumulative'},
            {'label': 'Daily', 'value': 'Daily'},
            {'label': '14-day cumulative per 100K', 'value': 'BiweeklyNorm'},
        ],
        value='Daily',
        labelClassName="mr-4",
        className="text-center lead",
        inline=True,
        inputClassName="mr-2"
    ),
    dcc.Graph(id='graph-dynamics', figure={})   
    # dcc.Graph(id='bargraph',
    #             figure=px.bar(df, barmode='group', x='Years',
    #             y=['Girls Kindergarten', 'Boys Kindergarten']))
])

@app.callback(
    Output('graph-dynamics', 'figure'),
    Input('dropdown-country-1', 'value'),
    Input('radio-data-row1', 'value'),
    Input('radio-data-row2', 'value')
)
def update_graph(country, measure, type):
    column = type+measure
    if column.isin(["CumulativeCases","CumulativeDeaths"]):
        column = "Confirmed"+measure
    dataS = data[data.CountryName == country]
    x = data[(data.CountryName==country)]["Date"]
    y = data[(data.CountryName==country)][column]
    fig = go.Figure()
    fig.add_trace(go.Scatter(x=x,y=y))
    fig.update_layout(
        # bargap=0,
        # legend=dict(orientation="h",yanchor="bottom",y=1.02,xanchor="right", x=1),
        template="simple_white"
    )
    return fig

#  -------------------------------------------------------------------------------------

# -= Page 2 =-

page_interventions = html.Div([
    html.H1('Government Interventions ',className="display-4",
            style={'textAlign':'center'}),
    html.Hr(),
    dbc.RadioItems(
        id="radio-data-1",
        options=[
            {'label': 'Cumulative cases', 'value': 'ConfirmedCases'},
            {'label': 'Daily cases', 'value': 'DailyCases'},
            {'label': '7-day average', 'value': 'Average7'},
            {'label': '14-day-average', 'value': 'Average14'}
        ],
        value='Average7',
        labelClassName="mr-4",
        className="text-center lead",
        inline=True,
        inputClassName="mr-2"
    ),
    dbc.RadioItems(
        id="radio-npi-1",
        options=[
            {'label': 'Gatherings', 'value': 'C4_Restrictions on gatherings'},
            {'label': 'School closing', 'value': 'C1_School closing'},
            {'label': 'Workplace closing', 'value': 'C2_Workplace closing'}
        ],
        value='C4_Restrictions on gatherings',
        labelClassName="mr-4",
        className="text-center lead",
        inline=True,
        inputClassName="mr-2"
    ),
    dcc.Graph(id='graph-npi', figure={})    
])

dict_npi = {"C1_School closing":["No restrictions","Recommend closing","Require closing some levels","Require closing all levels"],
            "C2_Workplace closing":["No restrictions","Recommend closing","Require closing some sectors","Require closing all non-essential"],
            "C4_Restrictions on gatherings":["No restrictions","1001 or more people","101-1000 people","11-100 people","10 people or less"]
      }

@app.callback(
    Output('graph-npi', 'figure'),
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

#  -------------------------------------------------------------------------------------

# -= Page 3 =-

page_context = html.Div([
    html.H1('Global Context',className="display-4",
            style={'textAlign':'center'}),
    html.Hr(),
    dcc.Graph(id='graph-world', figure={})
])

#  -------------------------------------------------------------------------------------

app.layout = html.Div([
    dcc.Location(id="url"),
    sidebar,
    content
])

app.validation_layout = html.Div([
    sidebar,
    content,
    page_dynamics,
    page_interventions,
    page_context
])

@app.callback(
    Output("page-content", "children"),
    [Input("url", "pathname")]
)
def render_page_content(pathname):
    if pathname == "/dynamics":
        return page_dynamics
    elif pathname == "/interventions":
        return page_interventions
    elif pathname == "/global-context":
        return page_context
    # If the user tries to reach a different page, return a 404 message
    return dbc.Jumbotron([
            html.H1("404: Not found", className="text-danger"),
            html.Hr(),
            html.P(f"The pathname {pathname} was not recognised..."),
    ])
#  -------------------------------------------------------------------------------------

if __name__=='__main__':
    app.run_server(debug=True, port=3000)
    # app.run_server(debug=False,dev_tools_ui=False,dev_tools_props_check=False,port=3000)