import plotly.express as px
import pandas as pd
from geopy.geocoders import Nominatim


geolocator = Nominatim(user_agent='AfriXplore')
def geolocate(country):
    # Geolocate the center of the country
    loc = geolocator.geocode(country)
    # And return latitude and longitude
    return (loc.latitude, loc.longitude)

TOKEN = 'pk.eyJ1IjoiaGJ5cjk5IiwiYSI6ImNrcnh2NW1rYTAyaXkzMW9ldHVjN2V5dzQifQ.Oy7iBuxYB2OtpXu2J-VysQ'


def createMap(country):
    points = geolocate(country)
    print(points)
    df = pd.DataFrame(columns=['x', 'y'])
    df.loc[len(df.index)] = [points[0],
                             points[1]]

    px.set_mapbox_access_token(TOKEN)
    fig = px.scatter_mapbox(df,
                            lat='x',
                            lon='y',
                            zoom=5,
                            height=800,
                            width=800)
    fig.write_html('static/example.html')