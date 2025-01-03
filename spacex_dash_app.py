# Import required libraries
import pandas as pd
import dash
import dash_html_components as html
import dash_core_components as dcc
from dash.dependencies import Input, Output
import plotly.express as px
import plotly.graph_objects as go

# Read the airline data into pandas dataframe
spacex_df = pd.read_csv("spacex_launch_dash.csv")
max_payload = spacex_df['Payload Mass (kg)'].max()
min_payload = spacex_df['Payload Mass (kg)'].min()
print(spacex_df.columns)

# Create a dash application
app = dash.Dash(__name__)

# Create an app layout
app.layout = html.Div(children=[html.H1('SpaceX Launch Records Dashboard',
                                        style={'textAlign': 'center', 'color': '#503D36',
                                               'font-size': 40}),
                                # TASK 1: Add a dropdown list to enable Launch Site selection
                                # The default select value is for ALL sites
                                dcc.Dropdown(id='site-dropdown',
                                            options=[{'label': 'All Sites', 'value': 'ALL'},
                                            {'label': 'CCAFS LC-40', 'value': 'CCAFS LC-40'},
                                            {'label': 'VAFB SLC-4E', 'value': 'VAFB SLC-4E'},
                                            {'label': 'KSC LC-39A', 'value': 'KSC LC-39A'},
                                            {'label': 'CCAFS SLC-40', 'value': 'CCAFS SLC-40'}],
                                            value='ALL',
                                            placeholder='Select a Launch Site here',
                                            searchable=True,
                                            style={'font-size': '25px'}
                                            ),
                                html.Br(),

                                # TASK 2: Add a pie chart to show the total successful launches count for all sites
                                # If a specific launch site was selected, show the Success vs. Failed counts for the site
                                html.Div(dcc.Graph(id='success-pie-chart')),
                                html.Br(),

                                html.P("Payload range (Kg):",
                                style={'font-size': '28px'}),
                                # TASK 3: Add a slider to select payload range
                                dcc.RangeSlider(id='payload-slider',
                                                min=0, max=10000, step=1000,
                                                marks={0: '0',
                                                       2500: '2500',
                                                       5000: '5000',
                                                       7500: '7500',
                                                       10000: '10000'},
                                                value=[min_payload, max_payload],
                                                tooltip={
                                                        "placement": "bottom",
                                                        "always_visible": True,
                                                        "style": {"fontSize": "25px"},},
                                                ),
                                html.Br(),

                                # TASK 4: Add a scatter chart to show the correlation between payload and launch success
                                html.Div(dcc.Graph(id='success-payload-scatter-chart')),
                                ])

# TASK 2:
# Add a callback function for `site-dropdown` as input, `success-pie-chart` as output
# Function decorator to specify function input and output
@app.callback(Output(component_id='success-pie-chart', component_property='figure'),
              Input(component_id='site-dropdown', component_property='value'))
def get_pie_chart(entered_site):
    filtered_df = spacex_df
    if entered_site == 'ALL':
        data = filtered_df[filtered_df['class'] == 1]
        fig = px.pie(data, values='class', 
        names='Launch Site', 
        title='Total Success Launches By Sites')
        # Customize title, axis labels, and font sizes
        fig.update_layout(
            title={
                'text': 'Total Success Launches By Sites',
                'font': {'size': 24}  # Title font size
                },
            font={
                'size': 18  # General font size including labels and numbers
                }
        )       
    else:
        site_data = filtered_df[filtered_df['Launch Site'] == entered_site]
        counts = site_data['class'].value_counts().reset_index()
        counts.columns = ['Outcome', 'Count']
        counts['Outcome'] = counts['Outcome'].replace({1: 'Success', 0: 'Failure'})
        fig = px.pie(counts, values='Count', 
        names='Outcome', 
        title='Total Success for site {}'.format(entered_site))
        fig.update_layout(
            title={
                'text': 'Total Success for site {}'.format(entered_site),
                'font': {'size': 24}  # Title font size
                },
            font={
                'size': 18  # General font size including labels and numbers
                }
        ) 

    return fig
    # return the outcomes piechart for a selected site

# TASK 4:
# Add a callback function for `site-dropdown` and `payload-slider` as inputs, `success-payload-scatter-chart` as output
@app.callback(Output(component_id='success-payload-scatter-chart', component_property='figure'),
              [Input(component_id='site-dropdown', component_property='value'),
              Input(component_id='payload-slider', component_property='value')])
def get_scatter_chart(entered_site, payload_range):
    filtered_df = spacex_df
    # Map categorical data to numeric or color codes
    category_colors = {
        'v1.0': 'blue',
        'v1.1': 'red',
        'FT': 'green',
        'B4': 'purple',
        'B5': 'orange'
        }
    if entered_site == 'ALL':
        data = filtered_df
        
        # Further filter based on payload range
        min_payload, max_payload = payload_range
        data = data[(data['Payload Mass (kg)'] >= min_payload) & (data['Payload Mass (kg)'] <= max_payload)]

        data['Color'] = data['Booster Version Category'].map(category_colors)
        fig = px.scatter(data, 
                        x='Payload Mass (kg)', y='class', 
                        color='Booster Version Category') 
        fig.update_layout(title='Correlation between Payload and Succes for all Sites', 
                            xaxis_title='Payload Mass (Kg)', 
                            yaxis_title='class',
                            legend_title='Booster Version Category') 

        fig.update_layout(
            title={
                'text': 'Correlation between Payload and Succes for all Sites',
                'font': {'size': 24}  # Title font size
                },
            font={
                'size': 18  # General font size including labels and numbers
                }
        ) 
        fig.update_traces(marker=dict(size=10))

    else:
        site_data = filtered_df[filtered_df['Launch Site'] == entered_site]

        # Further filter based on payload range
        min_payload, max_payload = payload_range
        site_data = site_data[(site_data['Payload Mass (kg)'] >= min_payload) & (site_data['Payload Mass (kg)'] <= max_payload)]

        fig = px.scatter(site_data, 
                        x='Payload Mass (kg)', y='class', 
                        color='Booster Version Category') 
        fig.update_layout(title='Correlation between Payload and Succes for {}'.format(entered_site), 
                            xaxis_title='Payload Mass (Kg)', 
                            yaxis_title='class',
                            legend_title='Booster Version Category')
        fig.update_layout(
            title={
                'text': 'Correlation between Payload and Succes for all Sites',
                'font': {'size': 24}  # Title font size
                },
            font={
                'size': 18  # General font size including labels and numbers
                }
        ) 
        fig.update_traces(marker=dict(size=10)) 

    return fig
    # return the outcomes piechart for a selected site

# Run the app
if __name__ == '__main__':
    app.run_server()
