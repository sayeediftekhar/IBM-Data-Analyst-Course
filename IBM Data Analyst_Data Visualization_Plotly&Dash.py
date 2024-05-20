import dash
from dash import dcc, html
from dash.dependencies import Input, Output
import pandas as pd
import plotly.express as px

# Load the data using pandas
data = pd.read_csv('https://cf-courses-data.s3.us.cloud-object-storage.appdomain.cloud/IBMDeveloperSkillsNetwork-DV0101EN-SkillsNetwork/Data%20Files/historical_automobile_sales.csv')

# Extract year and month from the Date column
data['Year'] = pd.to_datetime(data['Date']).dt.year
data['Month'] = pd.to_datetime(data['Date']).dt.month

# Initialize the Dash app
app = dash.Dash(__name__)

# Set the title of the dashboard
app.title = "Automobile Sales Statistics Dashboard"

# Create the dropdown menu options
dropdown_options = [
    {'label': 'Yearly Statistics', 'value': 'Yearly'},
    {'label': 'Recession Period Statistics', 'value': 'Recession'}
]

# Create the layout of the app
app.layout = html.Div([
    html.H1("Automobile Sales Statistics Dashboard", style={'textAlign': 'center', 'color': '#503D36', 'font-size': '24px'}),
    html.Div([
        html.Label("Select Statistics:"),
        dcc.Dropdown(
            id='dropdown-statistics',
            options=dropdown_options,
            placeholder='Select a report type',
            value='Yearly',
            style={'width': '50%', 'margin': 'auto'}
        )
    ], style={'text-align': 'center', 'margin-bottom': '20px'}),
    
    html.Div(id='output-container')
])


# Define the callback function to update the output container based on the selected statistics
@app.callback(
    Output(component_id='output-container', component_property='children'),
    [Input(component_id='dropdown-statistics', component_property='value')])
def update_output_container(selected_statistics):
    print("Selected statistics:", selected_statistics)  # Add a print statement to check the selected statistics
    if selected_statistics == 'Recession':
        # Filter the data for recession periods
        recession_data = data[data['Recession'] == 1]
        print("Recession data:", recession_data.head())  # Add a print statement to check the filtered data
        
        # Plot 1: Automobile sales fluctuate over Recession Period (year wise)
        yearly_rec = recession_data.groupby('Year')['Automobile_Sales'].mean().reset_index()
        R_chart1 = dcc.Graph(
            figure=px.line(yearly_rec, 
                x='Year',
                y='Automobile_Sales',
                title="Average Automobile Sales fluctuation over Recession Period")
        )
        print("Recession chart 1:", R_chart1)  # Add a print statement to check the chart object
        
        # Plot 2: Calculate the average number of vehicles sold by vehicle type
        average_sales = recession_data.groupby('Vehicle_Type')['Automobile_Sales'].mean().reset_index()
        R_chart2 = dcc.Graph(
            figure=px.bar(average_sales, 
                x='Vehicle_Type',
                y='Automobile_Sales',
                title="Average Number of Vehicles Sold by Vehicle Type during Recession")
        )
        print("Recession chart 2:", R_chart2)  # Add a print statement to check the chart object

        return html.Div([
            R_chart1,
            R_chart2
        ])

    elif selected_statistics == 'Yearly':
        # Plot 1: Yearly Automobile sales using line chart for the whole period
        yas = data.groupby('Year')['Automobile_Sales'].mean().reset_index()
        Y_chart1 = dcc.Graph(
            figure=px.line(yas, 
                x='Year',
                y='Automobile_Sales',
                title="Yearly Automobile Sales")
        )

        return html.Div(Y_chart1)


# Run the Dash app without debug mode on localhost:8050
if __name__ == '__main__':
    app.run_server(host='localhost', port=8050, debug=False)
