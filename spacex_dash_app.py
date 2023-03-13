# Import required libraries
import pandas as pd
import dash
import dash_html_components as html
import dash_core_components as dcc
from dash.dependencies import Input, Output
import plotly.express as px

# Read the airline data into pandas dataframe
spacex_df = pd.read_csv("spacex_launch_dash.csv")
max_payload = spacex_df['Payload Mass (kg)'].max()
min_payload = spacex_df['Payload Mass (kg)'].min()
sites = spacex_df['Launch Site'].unique()

# Create a dash application
app = dash.Dash(__name__)

# Create an app layout
app.layout = html.Div(children=[html.H1('SpaceX Launch Records Dashboard',
                                        style={'textAlign': 'center', 'color': '#503D36',
                                               'font-size': 40}),
                                # TASK 1: Add a dropdown list to enable Launch Site selection
                                dcc.Dropdown(id='site-dropdown', options=[{'label': 'All Sites', 'value': 'ALL'},
                                                                          {'label': sites[0], 'value': sites[0]},
                                                                          {'label': sites[1], 'value': sites[1]},
                                                                          {'label': sites[2], 'value': sites[2]},
                                                                          {'label': sites[3], 'value': sites[3]},
                                                                          ], 
                                                                          value='ALL', 
                                                                          placeholder='Select Launch Site', 
                                                                          searchable=True),         
                                html.Br(),
                                # TASK 2: Add a pie chart to show the total successful launches count for all sites
                                html.Div(dcc.Graph(id='success-pie-chart')),
                                html.Br(),

                                html.P("Payload range (Kg):"),
                                # TASK 3: Add a slider to select payload range
                                dcc.RangeSlider(id='payload-slider',
                                                min=0, max=10000, step=1000,
                                                marks={0: '0',
                                                    100: '100'},
                                                value=[min_payload, max_payload]),                    
                                # TASK 4: Add a scatter chart to show the correlation between payload and launch success
                                html.Div(dcc.Graph(id='success-payload-scatter-chart')),
                                ])

# TASK 2:
@app.callback(Output(component_id='success-pie-chart', component_property='figure'),
            Input(component_id='site-dropdown', component_property='value'))
def get_pie_chart(entered_site):
    filtered_df = spacex_df
    if entered_site == 'ALL':
        fig = px.pie(filtered_df, values='class', 
        names='Launch Site', 
        title='Total success launches for all sites')
        return fig
    else:
        filtered_df = spacex_df[spacex_df['Launch Site']==entered_site]
        df1 = filtered_df.groupby(['Launch Site','class']).size().reset_index(name='class count')
        fig = px.pie(df1, values='class count', names='class', title=f"Total Success Launches for site {entered_site}")
        return fig

# TASK 4:
@app.callback(
    Output(component_id='success-payload-scatter-chart', component_property='figure'),
    [Input(component_id='site-dropdown', component_property='value'),
    Input(component_id='payload-slider', component_property='value')]
)

def get_scatter_plot(entered_site, slide):
    low, high = slide
    cond = (spacex_df['Payload Mass (kg)'] > low) & (spacex_df['Payload Mass (kg)'] < high)
    filtered_df = spacex_df[cond]

    if entered_site == 'ALL':
        fig1 = px.scatter(filtered_df, x='Payload Mass (kg)', y='class', color='Booster Version Category')
    else:
        fig1 = px.scatter(
            filtered_df[filtered_df['Launch Site']==entered_site],
            x='Payload Mass (kg)',
            y='class',
            color='Booster Version Category')
    return fig1


    slide=(spacex_df['Payload Mass (kg)'] > low) & (spacex_df['Payload Mass (kg)'] < high)
    dropdown_scatter=spacex_df[slide]

    if site == 'ALL':
        fig = px.scatter(
            dropdown_scatter, x='Payload Mass (kg)', y='class',
            hover_data=['Booster Version'],
            color='Booster Version Category',
            title='Correlation between Payload and Success for all Sites')
        return fig
    else:
        dropdown_scatter = dropdown_scatter[spacex_df['Launch Site'] == site]
        title_scatter = f'Success by Payload Size for {site}'
        fig=px.scatter(
            dropdown_scatter,x='Payload Mass (kg)', y='class', 
            title = title_scatter, 
            color='Booster Version Category')
        return fig

# Run the app
if __name__ == '__main__':
    app.run_server()