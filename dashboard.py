import pandas as pd
import plotly.express as px  # (version 4.7.0)
import json
import base64

import dash  # (version 1.12.0) pip install dash
import dash_core_components as dcc
import dash_bootstrap_components as dbc
import dash_html_components as html
from dash.dependencies import Input, Output


app = dash.Dash(__name__, external_stylesheets=[dbc.themes.BOOTSTRAP],
                meta_tags=[{'name': 'viewport',
                            'content': 'width=device-width, initial-scale=1.0, maximum-scale=1.2, minimum-scale=0.5,'}])
server = app.server
# ------------------------------------------------------------------------------
# Import and clean data (importing csv into pandas)

df = pd.read_csv('cleaneddata.csv')
df["value"] = 1

with open('geocities.json') as f:
    Germany = json.load(f)

cityloc = {"munich":{'lat': 48.160667, 'lon': 11.58577},
           "berlin":{'lat': 52.516939, 'lon': 13.409258},
           "hamburg":{'lat': 53.527565, 'lon': 9.994440},
           "cologne":{'lat': 50.938152, 'lon': 6.959075},
           "frankfurt":{'lat': 50.099036, 'lon': 8.650413}}

# ------------------------------------------------------------------------------
#App layout
app.layout = html.Div([
                    html.Br(),
                    html.Br(),
                    dbc.Row(
                        dbc.Col([
                            html.Span('Lieferando ', style={"text-transform": "uppercase", "font-size": 25, "color":"#FD7515", "font-weight": "bold"}),
                            html.Br(),
                            html.Span('spatial exploration', style={"text-transform": "uppercase", "font-size": 14}),
                            html.Br(),
                            html.Br(),
                            html.Span("Here you can explore restaurants listed on ", style={"font-style": "italic", "font-size": 14, "color": "grey"}),
                            html.Span(html.A('Liferando.de ', href='https://www.lieferando.de/'), style={"font-style": "italic", "font-size": 14, "color": "grey"}),
                            html.Span("by their area of delivery, cuisine and rating. ",style={"font-style": "italic", "font-size": 14, "color": "grey"}),
                            html.Span("The data used have been web-scrapped and visualised using ", style={"font-style": "italic", "font-size": 14, "color": "grey"}),
                            html.Span(html.A('Selenium ', href='https://selenium-python.readthedocs.io/'), style={"font-style": "italic", "font-size": 14, "color": "grey"}),
                            html.Span("& ", style={"font-style": "italic", "font-size": 14, "color": "grey"}),
                            html.Span(html.A('Dash ', href='https://dash.plotly.com/'), style={"font-style": "italic", "font-size": 14, "color": "grey"}),
                            html.Span("libraries by Tomas Kristof sometimes in October 2020.", style={"font-style": "italic", "font-size": 14, "color": "grey"}),
                            html.Br(),
                            html.Br(),
                            html.Span(html.A('GitHub', href='https://github.com/kristoftomas/ExploreLieferandoBeta'), style={"font-size": 14, "color": "gray"}),
                            html.Span(" | ", style={"font-size": 14, "color": "gray"}),
                            html.Span(html.A(' LinkedIn', href='https://www.linkedin.com/in/kristoftomas/'), style={"font-size": 14, "color": "grey"}),
                            html.Br(),
                            html.Br(),
                            html.Span("Select ", style={"text-transform": "uppercase", "font-weight": "bold", 'text-align': 'center'}),
                            html.Span("city & cusine to filter the data "),
                            html.Br(),

                            html.Span("Hover or Click ", style={"text-transform": "uppercase", "font-weight": "bold", 'text-align': 'center'}),
                            html.Span("postcode to learn more"),
                            html.Br(),

                                ], xs=10, sm=8, md=6, lg=3, xl=3, style={"justify-content": "center","text-align": "center" }),
                    justify="center"),
                    html.Br(),
                    dbc.Row([dbc.Col(dcc.Dropdown(id="slct_city", options=[
                                                        {'label': 'Berlin', 'value': 'berlin'},
                                                        {'label': 'Munich', 'value': 'munich'},
                                                        {'label': 'Hamburg', 'value': 'hamburg'},
                                                        {'label': 'Cologne', 'value': 'cologne'},
                                                        {'label': 'Frankfurt', 'value': 'frankfurt'}
                                                          ],value="berlin",
                                                    placeholder="Select a city",
                                                ),width=5, xs=10, sm=8, md=4, lg=2, xl=2),
                             html.Br(),
                             dbc.Col(dcc.Dropdown(id="slct_cusine",
                                                    options=[
                                                        {'label': 'All', 'value': 'all'},
                                                        {'label': 'Italian', 'value': 'italian'},
                                                        {'label': 'Sushi', 'value': 'sushi'},
                                                        {'label': 'Indian', 'value': 'indian'},
                                                        {'label': 'Vietnamise', 'value': 'vietnamise'},
                                                        {'label': 'Chinese', 'value': 'chinese'},
                                                        {'label': 'Thai', 'value': 'thai'},
                                                        {'label': 'American', 'value': 'american'},
                                                        {'label': 'Turkish', 'value': 'turkish'},
                                                        {'label': 'Greek', 'value': 'greek'},
                                                        {'label': 'Mexican', 'value': 'mexican'},
                                                        {'label': 'Vegetarian', 'value': 'vegetarian'},
                                                        {'label': 'Vegan', 'value': 'vegan'},
                                                    ],
                                                    value=['italian'],
                                                    multi=True,
                                                    style={'width': "100%"}), width=5, xs=10, sm=8, md=4, lg=2, xl=2)], justify="center"),
                    html.Br(),

                    html.Br(),
                    dbc.Row([dbc.Spinner(dbc.Col(dbc.Card(dcc.Graph(id='my_pizza_map'), color="light", outline=True), xs=10, sm=10, md=8, lg=8, xl=7)),], justify="center"),
                    html.Br(),
                    dbc.Row([dbc.Spinner(dbc.Col(dbc.Card(dcc.Graph(id='my-output'), color="light", outline=True), xs=10, sm=10, md=10, lg=8,
                                         xl=7))], justify="center")

], style={"background-color": "#F9FAFB", "min-height": "100vh"})


# ------------------------------------------------------------------------------
# Connect the Plotly graphs with Dash Components

@app.callback(
     Output('my_pizza_map', 'figure'),
     [Input('slct_city', 'value'),
      Input('slct_cusine', 'value')])

def update_graph(slct_city, slct_cusine):
    dff = df.query(slct_city)
    dff = dff[dff[slct_cusine].any(1)]
    dff = dff.groupby("postcode").agg({"rating": "mean", "ratingtotal": "mean", "value":"sum"})
    dff = dff.reset_index()
    dff = dff.round(1)


    fig = px.choropleth_mapbox(dff, geojson=Germany,
                               locations='postcode',
                               color="rating",
                               color_continuous_scale="rainbow",
                               featureidkey="properties.plz",
                               zoom=9.8,
                               height=500,
                               center=cityloc[slct_city],
                               opacity=0.4,
                               hover_name ="postcode",
                               hover_data={'postcode': False,
                                           "value": True},
                               mapbox_style='carto-positron',
                               labels={'rating':'Rating','avgdeliverytime':'Delivery Time', "ratingtotal": "Total Ratings" , "count": "Restaurants"})


    fig.update_layout(margin={"r": 0, "t": 0, "l": 0, "b": 0})


    return fig

@app.callback(
    Output('my-output', 'figure'),
    [Input('my_pizza_map', 'clickData'),
     Input('slct_cusine', 'value')])


def display_click_data(clickData, slct_cusine):
    if clickData is None:
        return "nothing yet"
    else:
        temp = clickData["points"][0]["location"]
        df2 = df.query('postcode == @temp')
        df2 = df2[df2[slct_cusine].any(1)]
        fig2 = px.scatter(df2, x="rating", y="ratingtotal",
                          hover_data=['name', "url"],
                          height=300,
                          labels={'rating':'Average Rating', 'ratingtotal':'Total Rating Count (log)'},
                          log_y = True,
                          template="simple_white",
                          range_x= [0, 105])

        fig2.update_layout(margin={"r": 50, "t": 50, "l": 100, "b": 0})
        fig2.update(layout_coloraxis_showscale=False)
        # fig2.update_xaxes(fixedrange=True)
        # fig2.update_yaxes(fixedrange=True)

        return fig2

# ------------------------------------------------------------------------------
if __name__ == "__main__":
    app.run_server(debug=True)

