# app.py
import pandas as pd
from dash import Dash, dcc, html, Output, Input
import plotly.express as px

# Load processed data
df = pd.read_csv('data/processed_data.csv')
df['date'] = pd.to_datetime(df['date'])

# Initialize Dash app
app = Dash(__name__)
app.title = "Pink Morsel Sales Visualiser"

# Layout
app.layout = html.Div(
    style={'fontFamily': 'Arial, sans-serif', 'backgroundColor': '#f9f9f9', 'padding': '20px'},
    children=[
        html.H1(
            "Pink Morsel Sales Visualiser",
            style={'textAlign': 'center', 'color': '#2c3e50'}
        ),
        html.Div(
            style={'textAlign': 'center', 'marginBottom': '20px'},
            children=[
                html.Label("Select Region:", style={'fontWeight': 'bold', 'marginRight': '10px'}),
                dcc.RadioItems(
                    id='region-selector',
                    options=[
                        {'label': 'All', 'value': 'all'},
                        {'label': 'North', 'value': 'north'},
                        {'label': 'East', 'value': 'east'},
                        {'label': 'South', 'value': 'south'},
                        {'label': 'West', 'value': 'west'},
                    ],
                    value='all',
                    inline=True,
                    labelStyle={'marginRight': '15px'}
                )
            ]
        ),
        dcc.Graph(id='sales-line-chart')
    ]
)

# Callback to update graph based on region selection
@app.callback(
    Output('sales-line-chart', 'figure'),
    Input('region-selector', 'value')
)
def update_line_chart(selected_region):
    if selected_region == 'all':
        filtered_df = df
    else:
        filtered_df = df[df['region'].str.lower() == selected_region.lower()]
    
    # Aggregate sales by date
    df_total = filtered_df.groupby('date', as_index=False)['sales'].sum()
    
    fig = px.line(
        df_total,
        x='date',
        y='sales',
        title=f"Daily Sales of Pink Morsels ({selected_region.title()})",
        labels={'date': 'Date', 'sales': 'Total Sales'}
    )
    fig.update_layout(
        plot_bgcolor='#ecf0f1',
        paper_bgcolor='#f9f9f9',
        font=dict(color='#2c3e50')
    )
    return fig

# Run server
if __name__ == '__main__':
    app.run_server(debug=True)
