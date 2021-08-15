import pandas as pd
import plotly.express as px  # (version 4.7.0)
import plotly.graph_objects as go
import dash
import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output

# ---------- Additional function which changes the name of variables in column
def if_smoker(data):
  if data=='yes':return 'Smoking'
  else: return 'Non-smoking'

external_stylesheets = ['https://codepen.io/chriddyp/pen/bWLwgP.css']

app = dash.Dash(__name__, external_stylesheets=external_stylesheets)

# ---------- Import and clean data (importing csv into pandas)
df = pd.read_csv("insurance.csv")

# ---------- Using addition function on dataframe
df.smoker = df.smoker.apply(if_smoker)
df.columns =[e.capitalize() for e in df.columns]
df = df.groupby(['Smoker','Age','Sex','Region'])[['Charges']].mean()
df.reset_index(inplace=True)
print(df[:5])

# ------------------------------------------------------------------------------
# App layout
app.layout = html.Div(children=[
    html.H1("Web Application about impact on Insurence charge", style={'text-align': 'center'}),
    html.Br(),
    html.Div(children=[
        html.Div(children=[
            html.H2("Value of insurance charge based on age.", style={'text-align': 'center'}),
                dcc.Dropdown(id="slectd_characteristics",
                    options=[
                        {"label": "Sex: Female", "value": 'female'},
                        {"label": "Sex: Male", "value": 'male'},
                        {"label": "Smoker: Yes", "value": 'Smoking'},
                        {"label": "Smoker: No", "value": 'Non-smoking'}],
                    multi=False,
                    value=None,
                    placeholder="Choose the characteristics of the selected group",
                    style={'width': "50%"}
                    ),
            dcc.Graph(id='insurance_graph', figure={}),

            html.Div(id='output_container', children=[]),
        ], className='six columns'),
        html.Div(children=[
            html.H2(children="Sum of charges based on group's region", style={'text-align': 'center'}),
            html.Br(),
            dcc.Graph(
                id='insurance_graph2',
                figure={}
            ),
        ], className='six columns'),

    ], className='row'),
    html.Br(),
    html.H5('''The charts on the webside show that the value of insurance charge depends on age, as evidenced by the increasing minimum value with age. 
    Smoking has the greatest impact into the charge based on dataset, if person smokes, their insurance charges almost double. 
    It is possible to hover the mouse over for more information.
    '''),
    html.Br(),
    html.Br()

])


# ------------------------------------------------------------------------------
# Connect the Plotly graphs with Dash Components
@app.callback(
    [Output(component_id='output_container', component_property='children'),
     Output(component_id='insurance_graph', component_property='figure'),
     Output(component_id='insurance_graph2', component_property='figure')],
    [Input(component_id="slectd_characteristics", component_property='value')]
)
def update_graph(option_slctd):
    print(option_slctd)
    print(type(option_slctd))

    container = "Selected group of people is: {}".format(option_slctd)

    dff = df.copy()
    dff = dff[(dff["Sex"] == option_slctd) | (dff["Smoker"] == option_slctd)]


    # Plotly Express
    fig = px.scatter(
        data_frame=dff,
        x='Age',
        y='Charges',
        template='plotly_dark'
    )
    fig2 = px.bar(
        data_frame=dff,
        x='Region',
        y='Charges',
        template='plotly_dark'
    )

    return container, fig, fig2


# -------------------------------------------

if __name__ == '__main__':
    app.run_server(debug=True)