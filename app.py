#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Aug  8 19:23:40 2022

@author: yogisharosarumaha
"""


import dash
from dash import Dash, html, dcc
import pandas as pd
import numpy as np
import plotly.express as px

#Import dataset
df = pd.read_csv('/Users/yogisharosarumaha/Documents/GitHub/dash-luxloan-portfolio/data/LuxuryLoanPortfolio.csv')

#add remaining principal column
df['pct_remaining_principal'] = round(df['loan balance'] / df['funded_amount'] * 100)


#Create list of conditions
conditions = [
    (df['pct_remaining_principal'] <= 10),
    (df['pct_remaining_principal'] <= 20),
    (df['pct_remaining_principal'] <= 30),
    (df['pct_remaining_principal'] <= 40),
    (df['pct_remaining_principal'] <= 50),
    (df['pct_remaining_principal'] <= 60),
    (df['pct_remaining_principal'] <= 70),
    (df['pct_remaining_principal'] <= 80),
    (df['pct_remaining_principal'] <= 90),
    (df['pct_remaining_principal'] > 90)
]

#list of values to assign conditions
values = ['10%','20%','30%', '40%', '50%', '60%', '70%', '80%', '90%', '100%']

#replace existing column
df['pct_remaining_principal'] = np.select(conditions, values)


#Figure for 1st metric
fig1 = px.histogram(df, 
                        x = "pct_remaining_principal",
                        title = "Pct remaining principal")
                    
fig1.update_xaxes(
    categoryorder='array', 
    categoryarray= ['10%','20%','30%', '40%', '50%', '60%', '70%', '80%', '90%', '100%']
)



#Figure for 2nd metric
fig2 = px.pie(df,
                         values= "funded_amount", 
                         names= "purpose", 
                         title ="Funded Amount by purpose")

#Figure for 3rd metric
tbl = round(
    pd.crosstab(index = df['employment length'], 
            columns = df['duration months'],
            margins = True,
            margins_name = "proportion of loan months",
            normalize = 'index'
           ) * 100 
    , 1)

import plotly.graph_objects as go

# Data initiation for figure
data = []
# For loop for x axis to create barchart data
for x in tbl.columns:
   data.append(go.Bar(name=str(x), x=tbl.index, y=tbl[x]))

fig3 = go.Figure(data)




external_stylesheets = ['https://codepen.io/chriddyp/pen/bWLwgP.css']



# Create the Dash app
app = Dash(__name__, external_stylesheets=external_stylesheets)

app.layout = html.Div(children=[
    # Chart element for top page
    html.Div([
        html.Div([
            html.H1(children='Percentage Remaining Principal'),

            html.Div(children='''
                Metrics to check the health of portfolio, does the customer's payback ? 
            '''),

            dcc.Graph(
                id='graph1',
                figure=fig1
            ),  
        ], className='six columns'),
        html.Div([
            html.H1(children='Funded Amount by Purpose'),

            html.Div(children='''
                Metrics to check if we have too many loans concentrated in one sector? 
If we’re putting the most egg in one basket, what happens if that sector suddenly decline? 
Can our company withstand the defaults? 

            '''),

            dcc.Graph(
                id='graph2',
                figure=fig2
            ),  
        ], className='six columns'),
    ], className='row'),
    # Chart element for bottom page
    html.Div([
        html.H1(children='Employment Tenure and Loan Duration'),

        html.Div(children='''
            Metrics to check the distribution of customers employment length and loan duration. |
            X-Axis : Employment (Year) |
            Y-Axis : Count |
            Color : Loan Duration (months) |
        '''),

        dcc.Graph(
            id='graph3',
            figure=fig3
        ),  
    ], className='row'),
])
                 
server = app.server
                 
#Run local server
if __name__ == '__main__':
    app.run_server(debug=False)