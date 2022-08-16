######### Import your libraries #######
import dash
from dash import html
from dash import dcc
from dash.dependencies import Input, Output, State
import pandas as pd
import plotly as py
import plotly.graph_objs as go
from random import randrange

###### Define your variables #####
tabtitle = 'Titanic!'
color_list = ['paleturquoise', 'lavenderblush', 'aliceblue', 'burlywood', 'deeppink', 'lightyellow', 'beige', 'greenyellow', 'darkorange']
color1 = '#32a852'
color2 = '#4c32a8'
color3 = '#b8001f'
sourceurl = 'https://www.kaggle.com/c/titanic'
githublink = 'https://github.com/xshakib/304-titanic-dropdown'

###### Import a dataframe #######
df = pd.read_csv("https://raw.githubusercontent.com/austinlasseter/plotly_dash_tutorial/master/00%20resources/titanic.csv")
df['Female']=df['Sex'].map({'male':0, 'female':1})
df['Cabin Class'] = df['Pclass'].map({1:'first', 2: 'second', 3:'third'})
variables_list=['Survived', 'Female', 'Fare', 'Age']

########### Initiate the app
external_stylesheets = ['https://codepen.io/chriddyp/pen/bWLwgP.css']
app = dash.Dash(__name__, external_stylesheets=external_stylesheets)
server = app.server
app.title=tabtitle

####### Layout of the app ########
app.layout = html.Div([
    html.H3('Choose a continuous variable for summary statistics:'),
    dcc.Dropdown(
        id='dropdown',
        options=[{'label': i, 'value': i} for i in variables_list],
        value=variables_list[0]
    ),
    html.Br(),
    dcc.Graph(id='display-value'),
    html.A('Code on Github', href=githublink),
    html.Br(),
    html.A("Data Source", href=sourceurl),
])


######### Interactive callbacks go here #########
@app.callback(Output('display-value', 'figure'),
              [Input('dropdown', 'value')])
def display_value(continuous_var):
    grouped_mean=df.groupby(['Embarked', 'Cabin Class'])[continuous_var].mean()
    results=pd.DataFrame(grouped_mean)
    # Create a grouped bar chart
    mydata1 = go.Bar(
        x=results.loc['Cherbourg'].index,
        y=results.loc['Cherbourg'][continuous_var],
        name='Port Cherbourg',
        marker=dict(color=color1)
    )
    mydata2 = go.Bar(
        x=results.loc['Queenstown'].index,
        y=results.loc['Queenstown'][continuous_var],
        name='Port Queenstown',
        marker=dict(color=color2)
    )
    mydata3 = go.Bar(
        x=results.loc['Southampton'].index,
        y=results.loc['Southampton'][continuous_var],
        name='Port Southampton',
        marker=dict(color=color3)
    )

    mylayout = go.Layout(
        title='Grouped bar chart',
        xaxis = dict(title = 'Cabin Class'), # x-axis label
        yaxis = dict(title = str(continuous_var)), # y-axis label

    )
    fig = go.Figure(data=[mydata1, mydata2, mydata3], layout=mylayout)
    return fig


######### Run the app #########
if __name__ == '__main__':
    app.run_server(debug=True)