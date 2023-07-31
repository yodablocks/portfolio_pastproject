import pandas as pd  
import folium
import dash
import dash_html_components as html
import dash_core_components as dcc 
import plotly.express as px  
from dash.dependencies import Input, Output  

# Read the cleaned CSV file  
data = pd.read_csv('gpi_cleaned.csv') # it's the cleaned version from the xlsx file 

# Create the Dash app  
app = dash.Dash(__name__)  

# App layout  
app.layout = html.Div([  
html.H1('Travel Safety Analysis'),  
dcc.Dropdown(  
id='year-dropdown',  
options=[{'label': str(year), 'value': str(year)} for year in range(2011, 2021)],  
value='2011',  
),  
html.Div(id='map-container'),  
html.Div(id='charts-container'),  
])  

# Callback function  
@app.callback(  
[Output('map-container', 'children'),  
Output('charts-container', 'children')],  
[Input('year-dropdown', 'value')]  
)  
def update_map_and_charts(year):  
# Update the map  
m = folium.Map(zoom_start=2)  
folium.Choropleth(  
geo_data='https://raw.githubusercontent.com/python-visualization/folium/master/examples/data/world-countries.json',  
name='choropleth',  
data=data,  
columns=['iso3c', year],  
key_on='feature.id',  
fill_color='YlOrRd',  
fill_opacity=0.7,  
line_opacity=0.2,  
legend_name='Safety Score'  
).add_to(m)  
map_container = html.Iframe(srcDoc=m._repr_html_(), width='100%', height='600')  
# Update the charts  
avg_safety_score = data[year].mean()  
top_10_safest = data.nsmallest(10, year)  
bar_chart = px.bar(top_10_safest, x=year, y='Country', orientation='h', title=f'Top 10 Safest Countries in {year}')  
scatter_chart = px.scatter(data, x='Country', y=year, title=f'Safety Scores for All Countries in {year}')  
scatter_chart.add_shape(type='line', x0=0, x1=len(data), y0=avg_safety_score, y1=avg_safety_score,  
yref='y', xref='x', line=dict(color='red'))  
charts_container = html.Div([  
html.Div([dcc.Graph(figure=bar_chart)], style={'width': '50%', 'display': 'inline-block'}),  
html.Div([dcc.Graph(figure=scatter_chart)], style={'width': '50%', 'display': 'inline-block'}),  
])  
return map_container, charts_container  
# Run the app  
if __name__ == '__main__':  
app.run_server(debug=True)
