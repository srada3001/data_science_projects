# Import required libraries
import pandas as pd
import dash
from dash import html
from dash import dcc
from dash.dependencies import Input, Output
import plotly.express as px

# Read the SpaceX launch data into pandas dataframe
spacex_df = pd.read_csv("spacex_launch_dash.csv")
max_payload = spacex_df['Payload Mass (kg)'].max()
min_payload = spacex_df['Payload Mass (kg)'].min()

# Create a dash application
app = dash.Dash(__name__)

# Create an app layout
app.layout = html.Div(children=[
    html.H1(
        'SpaceX Launch Records Dashboard',
        style={'textAlign': 'center', 'color': '#503D36', 'font-size': 40}
    ),

    # TASK 1: Dropdown for launch site selection
    dcc.Dropdown(
        id='site-dropdown',
        options=[
            {'label': 'All Sites', 'value': 'ALL'},
            *[
                {'label': site, 'value': site}
                for site in spacex_df['Launch Site'].unique()
            ]
        ],
        value='ALL',
        placeholder='Select a Launch Site here',
        searchable=True
    ),
    html.Br(),

    # TASK 2: Pie chart for ALL sites
    html.Div(dcc.Graph(id='all-sites-pie-chart')),
    html.Br(),

    # TASK 2: Pie chart for selected site
    html.Div(dcc.Graph(id='success-pie-chart')),
    html.Br(),

    html.P("Payload range (Kg):"),

    # TASK 3: Add Range Slider
    dcc.RangeSlider(
        id='payload-slider',
        min=0, max=10000, step=1000,
        marks={
            0: '0',
            2500: '2500',
            5000: '5000',
            7500: '7500',
            10000: '10000'
        },
        value=[min_payload, max_payload]
    ),
    html.Br(),

    # TASK 4: Scatter plot
    html.Div(dcc.Graph(id='success-payload-scatter-chart')),
])

# ---------------------------------------------------------------------
# TASK 2 – Callback A: Pie chart for ALL SITES
# ---------------------------------------------------------------------
@app.callback(
    Output('all-sites-pie-chart', 'figure'),
    Input('site-dropdown', 'value')
)
def render_all_sites_pie(_):
    fig = px.pie(
        spacex_df,
        values='class',
        names='Launch Site',
        title='Total Success Launches By Site'
    )
    return fig

# ---------------------------------------------------------------------
# TASK 2 – Callback B: Pie chart for SELECTED SITE (success vs failure)
# ---------------------------------------------------------------------
@app.callback(
    Output('success-pie-chart', 'figure'),
    Input('site-dropdown', 'value')
)
def render_selected_site_pie(selected_site):
    if selected_site == 'ALL':
        fig = px.pie(
            values=[1],
            names=['Select a Launch Site to view Success vs Failure'],
            title='Success vs Failure'
        )
        return fig

    filtered = spacex_df[spacex_df['Launch Site'] == selected_site]

    fig = px.pie(
        filtered,
        names='class',
        title=f'Success vs Failure for site {selected_site}'
    )
    return fig

# ---------------------------------------------------------------------
# TASK 4: Callback for scatter chart
# ---------------------------------------------------------------------
@app.callback(
    Output('success-payload-scatter-chart', 'figure'),
    [
        Input('site-dropdown', 'value'),
        Input('payload-slider', 'value')
    ]
)
def update_scatter(selected_site, payload_range):

    low, high = payload_range

    # Filter by payload range first
    df_filtered = spacex_df[
        (spacex_df['Payload Mass (kg)'] >= low) &
        (spacex_df['Payload Mass (kg)'] <= high)
    ]

    # ALL sites case
    if selected_site == 'ALL':
        fig = px.scatter(
            df_filtered,
            x='Payload Mass (kg)',
            y='class',
            color='Booster Version Category',
            title='Correlation Between Payload and Success for All Sites'
        )
        return fig

    # Specific site selected
    df_filtered = df_filtered[df_filtered['Launch Site'] == selected_site]

    fig = px.scatter(
        df_filtered,
        x='Payload Mass (kg)',
        y='class',
        color='Booster Version Category',
        title=f'Correlation Between Payload and Success for {selected_site}'
    )
    return fig


# Run the app
if __name__ == '__main__':
    app.run()
