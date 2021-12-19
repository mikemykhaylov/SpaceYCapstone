# Import required libraries
import dash
import dash.dcc as dcc
import dash.html as html
import pandas as pd
import plotly.express as px
from dash import Output, Input

spacex_df = pd.read_csv("spacex_launch_dash.csv")
max_payload = spacex_df['Payload Mass (kg)'].max()
min_payload = spacex_df['Payload Mass (kg)'].min()

# Create a dash application
app = dash.Dash(__name__)

# Create an app layout
app.layout = html.Div(children=[html.H1('SpaceX Launch Records Dashboard',
                                        style={'textAlign': 'center', 'color': '#503D36',
                                               'font-size': 40}),
                                # TASK 1: Add a dropdown list to enable Launch Site selection
                                # The default select value is for ALL sites
                                dcc.Dropdown(
                                    id='site-dropdown',
                                    options=[
                                        {'label': 'All Sites', 'value': 'ALL'},
                                        {'label': 'CCAFS LC-40', 'value': 'CCAFS LC-40'},
                                        {'label': 'VAFB SLC-4E', 'value': 'VAFB SLC-4E'},
                                        {'label': 'KSC LC-39A', 'value': 'KSC LC-39A'},
                                        {'label': 'CCAFS SLC-40', 'value': 'CCAFS SLC-40'}
                                    ],
                                    value='ALL',
                                    placeholder="Select site",
                                    searchable=True
                                ),
                                html.Br(),

                                # TASK 2: Add a pie chart to show the total successful launches count for all sites
                                # If a specific launch site was selected, show the Success vs. Failed counts for the site
                                html.Div(dcc.Graph(id='success-pie-chart')),
                                html.Br(),

                                html.P("Payload range (Kg):"),
                                # TASK 3: Add a slider to select payload range
                                dcc.RangeSlider(
                                    id='payload-slider',
                                    min=min_payload,
                                    max=max_payload,
                                    step=1000,
                                    value=[min_payload, max_payload]
                                ),

                                # TASK 4: Add a scatter chart to show the correlation between payload and launch success
                                html.Div(dcc.Graph(id='success-payload-scatter-chart')),
                                ])


# TASK 2:
# Add a callback function for `site-dropdown` as input, `success-pie-chart` as output

@app.callback(
    Output('success-pie-chart', 'figure'),
    Input('site-dropdown', 'value')
)
def get_pie_chart(entered_site):
    filtered_df = spacex_df[spacex_df['Mission Outcome'].map(lambda x: 'Success' in x)]
    if entered_site == 'ALL':
        filtered_df = filtered_df['Launch Site'].value_counts().rename('Site Count').reset_index()
        fig = px.pie(filtered_df, values='Site Count',
                     names='index',
                     title='Successful mission outcomes for all sites')
        return fig
    else:
        filtered_df = filtered_df[filtered_df['Launch Site'] == entered_site]
        fig = px.pie(filtered_df, values='class',
                     names='Mission Outcome',
                     title='Successful mission outcomes for site ' + entered_site)
        return fig


# TASK 4:
# Add a callback function for `site-dropdown` and `payload-slider` as inputs, `success-payload-scatter-chart` as output
@app.callback(
    Output('success-payload-scatter-chart', 'figure'),
    [Input('payload-slider', 'value'), Input('site-dropdown', 'value')],
)
def get_pie_chart(range, entered_site):
    filtered_df = spacex_df
    if entered_site != 'ALL':
        filtered_df = spacex_df[spacex_df['Launch Site'].map(lambda x: entered_site in x)]
    filtered_df = filtered_df[(filtered_df['Payload Mass (kg)'] > range[0]) &
                              (filtered_df['Payload Mass (kg)'] < range[1])]
    fig = px.scatter(filtered_df, x="Payload Mass (kg)", y="class", color="Booster Version Category")
    return fig


# Run the app
if __name__ == '__main__':
    app.run_server()
