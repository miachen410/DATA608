'''
Module 4
In this module we’ll be looking at data from the New York City tree census:
https://data.cityofnewyork.us/Environment/2015-Street-Tree-Census-Tree-Data/uvpi-gqnh
This data is collected by volunteers across the city, and is meant to catalog information
about every single tree in the city.
'''

import pandas as pd
import numpy as np

'''
The dataset contains 684,000 rows and 45 columns. Instead of retrieving all the data, we can select only the data we need by querying through API call using Socrata query.
First we want to determine the range of the for loop:
Number of boroughs: 5
Species of trees: 132
States of health: 3
States of steward: 4
Thus, we need a maximum of 3*132*3*4 = 4752 rows
'''

for x in range(0, 4752, 1000):
    soql_url = ('https://data.cityofnewyork.us/resource/nwxe-4ae8.json?$limit=1000&$offset=' + str(x) +\
        '&$select=boroname,spc_common,health,steward,count(tree_id)' +\
        '&$group=boroname,spc_common,health,steward').replace(' ', '%20')
    soql_trees = pd.read_json(soql_url)
    if(x==0):
        df = pd.DataFrame(columns=list(soql_trees.columns.values))
    df = df.append(soql_trees)

# Remove rows that do not have complete data
df = df.dropna(axis=0, how='any')

species = df['spc_common'].unique()

'''
Build a dash app for a arborist studying the health of various tree species (as defined by the variable ‘spc_common’) across each borough (defined by the variable ‘borough’). This arborist would like to answer the following two questions for each species and in each borough:
1. What proportion of trees are in good, fair, or poor health according to the ‘health’ variable?
2. Are stewards (steward activity measured by the ‘steward’ variable) having an impact on the health of trees?
'''

# -*- coding: utf-8 -*-
import dash
import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output
import plotly.graph_objs as go

external_stylesheets = ['https://codepen.io/chriddyp/pen/bWLwgP.css']

app = dash.Dash(__name__, external_stylesheets=external_stylesheets)

app.layout = html.Div([
    html.Div(html.H1(children="NYC Trees")),

    html.Label("Select a specie"),

    html.Div(
        dcc.Dropdown(
            id='specie',
            options=[{'label':i, 'value':i} for i in species],
            value='sycamore maple'
        )
    ),

    html.Div(
        dcc.Graph(id="Tree Chart")
    ),

    html.Div(
        dcc.Graph(id="Steward Chart")
    )
])

# Tree Health Distribution Chart for question 1
@app.callback(
    Output('Tree Chart', 'figure'),
    [Input('specie', 'value')])
def update_fig(selected_specie):
    dff = df[df.spc_common == selected_specie]

    traces = []

    traces.append(go.Bar(
        x=list(dff.boroname),
        y=list(dff.count_tree_id[dff.health == "Good"]),
        name="Good"
    ))

    traces.append(go.Bar(
        x=list(dff.boroname),
        y=list(dff.count_tree_id[dff.health == "Fair"]),
        name="Fair"
    ))

    traces.append(go.Bar(
        x=list(dff.boroname),
        y=list(dff.count_tree_id[dff.health == "Poor"]),
        name="Poor"
    ))

    return {
        'data': traces,
        'layout': go.Layout(
            barmode='stack',
            title='Tree Health in Five Boroughs'
        )
    }


# Steward and Tree Health Chart for question 2
@app.callback(
    Output('Steward Chart', 'figure'),
    [Input('specie', 'value')])
def update_fig2(selected_specie):
    dff = df[df.spc_common == selected_specie]

    traces2 = []

    traces2.append(go.Bar(
        x=list(dff.steward),
        y=list(dff.count_tree_id[dff.health == "Good"]),
        name = "Good"
    ))
    
    traces2.append(go.Bar(
        x=list(dff.steward),
        y=list(dff.count_tree_id[dff.health == "Fair"]),
        name = "Fair"
    ))

    traces2.append(go.Bar(
        x=list(dff.steward),
        y=list(dff.count_tree_id[dff.health == "Poor"]),
        name = "Poor"
    ))

    return {
        'data': traces2,
        'layout': go.Layout(
            barmode='stack',
            title='Effect of Steward on Tree Health'
        )
    }


if __name__ == '__main__':
    app.run_server(debug=True)
