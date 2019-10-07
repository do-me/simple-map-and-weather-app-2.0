# Simple map and weather app: WeatherMapp

from flask import Flask,render_template,request
from string import Template 
import pyowm # open weather API
owm = pyowm.OWM('yourkey')
from geopy.geocoders import Bing
geolocator= Bing("yourkey", format_string=None, scheme=None, user_agent=None)

app = Flask(__name__)

@app.route("/") # homepage with form
def places():
    return render_template('my-form.html')
	
@app.route('/', methods=['POST']) # gets form results and executes function
def my_form_post():
    text = request.form['text']
    return create_homepage(text) # refers to create_homepage() defined below
	
@app.route("/<city>") 
def create_homepage(city):
    loca = geolocator.geocode(city) # geocodeing: input to address 
    latlong=str(loca.latitude)+","+str(loca.longitude) # address to coordinates
    observation = owm.weather_around_coords(loca.latitude, loca.longitude) # get weather for coordinates
    w = observation[0].get_weather() # string format result 
    weather=str("<br>")+str(round(w.get_temperature('celsius')["temp"])) + " °C</br> " + str(w.get_detailed_status()).title()
    
    return Template(render_template('standard.html')).substitute(latlong=latlong, # latlong for leaflet map in template
	title=city.title(), weather=weather)

if __name__ == '__main__':
    app.run(use_reloader=True,debug=True)
