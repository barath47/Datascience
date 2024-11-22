import dash
import dash_core_components as dcc
import dash_html_components as html
import plotly.express as px
from dash.dependencies import Input, Output
import pandas as pd

# Sample DataFrame (replace with your actual spacex_df)
data = {
    'launch_site': ['CCAFS LC-40', 'VAFB SLC-4E', 'CCAFS LC-40', 'KSC LC-39A', 'VAFB SLC-4E'],
    'payload_mass': [1000, 2000, 1500, 2500, 3000],
    'class': [1, 0, 1, 1, 0],  # 1 for success, 0 for failure
    'Booster Version Category': ['v1.0', 'v1.1', 'v1.2', 'v1.1', 'v1.0']
}
spacex_df = pd.DataFrame(data)

# Create Dash app
app = dash.Dash(__name__)

# Layout with RangeSlider, Dropdown, Pie Chart, and Scatter Plot
app.layout = html.Div([
    # Label for the RangeSlider
    html.P("Payload range (Kg):"),
    
    # RangeSlider for selecting Payload
    dcc.RangeSlider(
        id='payload-slider',  # Unique identifier for the component
        min=0,                # Minimum value of the slider (0 kg)
        max=10000,            # Maximum value of the slider (10000 kg)
        step=1000,            # Step value, determines the interval between selectable values (1000 kg)
        marks={               # Marks to show on the slider at specific intervals
            0: '0 kg',
            1000: '1000 kg',
            2000: '2000 kg',
            3000: '3000 kg',
            4000: '4000 kg',
            5000: '5000 kg',
            6000: '6000 kg',
            7000: '7000 kg',
            8000: '8000 kg',
            9000: '9000 kg',
            10000: '10000 kg'
        },
        value=[0, 10000],  # Default value: the entire range from 0 kg to 10000 kg
    ),
    
    # Dropdown for selecting Launch Site
    dcc.Dropdown(
        id='site-dropdown',
        options=[
            {'label': 'All Sites', 'value': 'ALL'},
            {'label': 'CCAFS LC-40', 'value': 'CCAFS LC-40'},
            {'label': 'VAFB SLC-4E', 'value': 'VAFB SLC-4E'},
            {'label': 'KSC LC-39A', 'value': 'KSC LC-39A'}
        ],
        value='ALL',  # Default value for the dropdown
        placeholder="Select a Launch Site here",
        searchable=True
    ),
    
    # Pie chart to visualize success/failure
    dcc.Graph(id='success-pie-chart'),

    # Scatter plot to visualize payload mass vs class
    dcc.Graph(id='success-payload-scatter-chart')
])

# Callback to update the pie chart based on payload range and selected launch site
@app.callback(
    Output('success-pie-chart', 'figure'),
    [Input('payload-slider', 'value'),
     Input('site-dropdown', 'value')]
)
def update_pie_chart(payload_range, entered_site):
    # Get the min and max payload values from the slider
    min_payload, max_payload = payload_range
    
    # Filter the dataframe based on the payload range
    filtered_df = spacex_df[(spacex_df['payload_mass'] >= min_payload) & 
                            (spacex_df['payload_mass'] <= max_payload)]
    
    # If a specific site is selected, filter further based on the selected site
    if entered_site != 'ALL':
        filtered_df = filtered_df[filtered_df['launch_site'] == entered_site]
    
    # Create a pie chart for the filtered data
    success_counts = filtered_df['class'].value_counts().reset_index()
    success_counts.columns = ['Success', 'Count']
    
    fig = px.pie(success_counts, names='Success', values='Count', 
                 title=f'Launch Success Distribution (Payload: {min_payload}-{max_payload} kg)')
    
    return fig

# Callback to update the scatter plot based on payload range and selected launch site
@app.callback(
    Output('success-payload-scatter-chart', 'figure'),
    [Input('site-dropdown', 'value'),
     Input('payload-slider', 'value')]
)
def update_scatter_plot(entered_site, payload_range):
    # Get the min and max payload values from the slider
    min_payload, max_payload = payload_range
    
    # Filter the dataframe based on the payload range
    filtered_df = spacex_df[(spacex_df['payload_mass'] >= min_payload) & 
                            (spacex_df['payload_mass'] <= max_payload)]
    
    # If a specific site is selected, filter further based on the selected site
    if entered_site != 'ALL':
        filtered_df = filtered_df[filtered_df['launch_site'] == entered_site]
    
    # Create a scatter plot with payload on the x-axis and class (launch outcome) on the y-axis
    fig = px.scatter(filtered_df, x='payload_mass', y='class',
                     color='Booster Version Category',  # Color by Booster Version
                     title=f'Payload vs Success for {entered_site}' if entered_site != 'ALL' 
                     else f'Payload vs Success (All Sites)',
                     labels={'payload_mass': 'Payload Mass (kg)', 'class': 'Launch Outcome'},
                     color_continuous_scale='Viridis')  # Color scale for the booster version category
    
    return fig

# Run the app
if __name__ == '__main__':
    app.run_server(debug=True)