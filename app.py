"""
zomatoRestaurantsApp: Python-Flask webapp about World Cities Population and Location
"""

# render_template alows to separate presentation from controller
# it will render HTML pages
# notice Flask uses Jinja2 template engine for rendering templates

# url_for() to reference static resources. 
# For example, to refer to /static/js/main.js, 
# you can use url_for('static', filename='js/main.js')

# request is to hold requests from a client e.g request.headers.get('')

from flask import Flask, render_template, Blueprint, request, url_for

from model import ZomatoRestaurantsApark

import os
import logging


main = Blueprint('main', __name__)

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

listings = []
hosts_profiling = []

# in the dynamic routes we can use 4 Flask context global variables:
# current_app, g, request, session
# The request is used here. 
# Further details can be found in the Flask documentation 

# URLs to be handled by the main route handler
@main.route('/')  
def home():

	return render_template("home.html") 

@main.route('/about') 
def about():
	return render_template("about.html") 

@main.route('/filtering', methods=['GET','POST'])  
def filtering():
	logger.info(request.method)
	list_countries = 0
	list_city = 0
	if request.method == 'POST':
		list_countries = request.form.get("countries")
		list_city = str(request.form.get("city"))
		#min_population = int(request.form.get("minpopulation"))
		#max_population = int(request.form.get("maxpopulation"))
		#if request.form.get("minpopulation"):
		#	min_population = int(request.form.get("minpopulation"))
		#if request.form.get("maxpopulation"):
		#	max_population = int(request.form.get("maxpopulation"))

	zomato_restaurants.filtering(list_countries, list_city)
	listings = zomato_restaurants.getListings()
	
	# logger.info(listings) 
	# logger.info(hosts_profiling)
	return render_template("home.html", map_data=listings)

@main.route('/barchart') 
def barchart():
	return render_template("barchart.html")

@main.route('/barchart_filtering', methods=['GET','POST'])  
def barchart_filtering():
	option = ""
	list_countries = ""
	if request.method == 'POST':
		option = int(request.form.get("optionselect"))
		list_countries = request.form.getlist("countries")
			
	zomato_restaurants.barchart(option, list_countries)
	hosts_profiling = zomato_restaurants.getHostsProfiling()
	logger.info(hosts_profiling)
	return render_template("barchart.html", profiling_data=hosts_profiling)

@main.route('/bubblechart') 
def bubblechart():
	return render_template("bubblechart.html")

@main.route('/bubblechart_filtering', methods=['GET','POST'])  
def bubblechart_filtering():
	option = ""
	list_countries = ""
	if request.method == 'POST':
		option = int(request.form.get("optionselect"))
		list_countries = request.form.getlist("countries")
			
	zomato_restaurants.bubblechart(option, list_countries)
	hosts_profiling = zomato_restaurants.getHostsProfiling()
	logger.info(hosts_profiling)
	return render_template("bubblechart.html", profiling_data=hosts_profiling)

@main.route('/treemap') 
def treemap():
	zomato_restaurants.treemap()
	hosts_profiling = zomato_restaurants.getHostsProfiling()
	logger.info(hosts_profiling)
	return render_template("treemap.html", profiling_data=hosts_profiling)

def create_app(spark_session, dataset_path):

	# our main Spark class
	global zomato_restaurants     
	zomato_restaurants = ZomatoRestaurantsApark(spark_session, dataset_path) 
	
	# construct an instance of Flask class for our webapp
	app = Flask(__name__)    

	app.register_blueprint(main)   
	# note: if there are other blueprints I can include in the app

	# routes will be attached from now on

	return app
