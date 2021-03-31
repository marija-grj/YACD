import dash
import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Output, Input
import plotly.express as px
import plotly.graph_objects as go
import dash_bootstrap_components as dbc
import pandas as pd
import datetime

data = pd.read_csv("https://raw.githubusercontent.com/marija-grj/YACD/main/data/OxCGRT_latest.csv",dtype={'CountryCode':'string'})
data.loc[:,'Date'] = pd.to_datetime(data.Date, format='%Y-%m-%d')
minDate = data.Date.min()

numDate = [x for x in range(len(data.Date.unique()))] # Transform every unique date to a number

#  -------------------------------------------------------------------------------------

app = dash.Dash(__name__, external_stylesheets=[dbc.themes.LUMEN],
                suppress_callback_exceptions = True)

server = app.server

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
        html.H3("Yet"+"\n"+"Another Covid-19 Dashboard", className="display-8"),
        html.Hr(),
        html.P(
            "Select a country", className="lead"
        ),
        dcc.Dropdown(
            id='dropdown-country-1', multi=False, value='Latvia',
            options=[{'label':x, 'value':x} for x in sorted(data.CountryName.unique())]
        ),
        html.Hr(),
        dbc.Nav([
            dbc.NavLink("Main", href="/", active="exact"),
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

# -= Page 0 =-

page_main = html.Div([
    html.H1('The project',className="display-4",
            style={'textAlign':'center'}),
    html.Hr(),
    html.P('About the project, authors and sources')
])

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
    dcc.Graph(id='graph-dynamics', figure={}),
    dcc.RangeSlider(
        id='date-slider-1',
        min=numDate[0],
        max=numDate[-1],
        value=[numDate[0], numDate[-1]],
        step=1,
        allowCross=False,
        marks={
            0:"Jan 2020",
            60:"Mar 2020",
            121:"May 2020",
            182:"Jul 2020",
            244:"Sep 2020",
            305:"Nov 2020",
            366:"Jan 2021",
            425:"Mar 2021"
        }
    )   
])

@app.callback(
    Output('graph-dynamics', 'figure'),
    Input('dropdown-country-1', 'value'),
    Input('radio-data-row1', 'value'),
    Input('radio-data-row2', 'value'),
    Input('date-slider-1', 'value')
)
def update_graph(country, measure, type, dateNum):
    column = type+measure
    if (column=="CumulativeCases") | (column=="CumulativeDeaths"):
        column = "Confirmed"+measure
    dataS = data[data.CountryName == country]
    x = data[(data.CountryName==country) &
             (data.Date >= minDate+datetime.timedelta(days=dateNum[0])) &
             (data.Date <= minDate+datetime.timedelta(days=dateNum[1]))
             ]["Date"]
    y = data[(data.CountryName==country) &
             (data.Date >= minDate+datetime.timedelta(days=dateNum[0])) &
             (data.Date <= minDate+datetime.timedelta(days=dateNum[1]))
            ][column]
    fig = go.Figure()
    fig.add_trace(go.Scatter(x=x,y=y,marker_color='#158bba'))
    fig.update_layout(
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
            {'label': 'Workplace closing', 'value': 'C2_Workplace closing'},
            {'label': 'Internal movement', 'value': 'C7_Restrictions on internal movement'},
            {'label': 'International travel', 'value': 'C8_International travel controls'}
        ],
        value='C4_Restrictions on gatherings',
        labelClassName="mr-4",
        className="text-center lead",
        inline=True,
        inputClassName="mr-2"
    ),
    dcc.Graph(id='graph-npi', figure={}),
        dcc.RangeSlider(
        id='date-slider-2',
        min=numDate[0],
        max=numDate[-1],
        value=[numDate[0], numDate[-1]],
        step=1,
        allowCross=False,
        marks={
            0:"Jan 2020",
            60:"Mar 2020",
            121:"May 2020",
            182:"Jul 2020",
            244:"Sep 2020",
            305:"Nov 2020",
            366:"Jan 2021",
            425:"Mar 2021"
        }
    )      
])

dict_npi = {"C1_School closing":["No restrictions","Recommend closing","Require closing some levels","Require closing all levels"],
            "C2_Workplace closing":["No restrictions","Recommend closing","Require closing some sectors","Require closing all non-essential"],
            "C4_Restrictions on gatherings":["No restrictions","1001 or more people","101-1000 people","11-100 people","10 people or less"],
            "C7_Restrictions on internal movement":["No restrictions","Recommendations","Restrictions"],
            "C8_International travel controls":["No restrictions","Screening arrivals","Quarantine arrivals","Ban arrivals from some regions","Total border closure"]
            } 
colors_npi = ['#8b8b8b','#beddf4','#7cbce9','#3b9ade','#1f77b4']
colors_npi2 = ['#8b8b8b','#99caff','#4da3ff','#007bff','#0056b3']
colors_npi3 = ['#8b8b8b','#75cdf0','#30b4e8','#158bba','#0f678a']


@app.callback(
    Output('graph-npi', 'figure'),
    Input('dropdown-country-1', 'value'),
    Input('radio-data-1', 'value'),
    Input('radio-npi-1','value'),
    Input('date-slider-2', 'value')
)
def update_graph(country, column, npi, dateNum):
    dataS = data[(data.CountryName==country) &
             (data.Date >= minDate+datetime.timedelta(days=dateNum[0])) &
             (data.Date <= minDate+datetime.timedelta(days=dateNum[1]))
             ]
    x = dataS["Date"]
    y = dataS[column]
    c = dataS[npi]
    fig = go.Figure()
    for i in range(len(dict_npi[npi])):
        fig.add_trace(go.Bar(x=x[c==i], y=y[c==i], name=dict_npi[npi][i], marker_color=colors_npi3[i]))
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
    page_main,
    page_dynamics,
    page_interventions,
    page_context
])

@app.callback(
    Output("page-content", "children"),
    [Input("url", "pathname")]
)
def render_page_content(pathname):
    if pathname == "/": 
        return page_main
    elif pathname == "/dynamics":
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
    app.run_server(debug=True)