# ==============================================================
DATASET = "zomato.csv"
SPARK_CODE = "model.py"
APP_NAME = "Zomato and Spark SQL"
WEB_PORT = 5678
# DATASET = "https://www.kaggle.com/i2i2i2/cities-of-the-world"
# ==============================================================

import time, sys, cherrypy, os
from paste.translogger import TransLogger
from pyspark.sql import SparkSession

from app import create_app # where the Flask app is defined

basedir = os.path.abspath(os.path.dirname(__file__))

def init_spark_session():
	
	# start Spark session
	spark = SparkSession.builder.appName(APP_NAME).getOrCreate()
	
	# important: should pass all Python modules to each Spark worker
	# to be adjusted in case
	spark_code_path = os.path.join(basedir, SPARK_CODE)
	spark.sparkContext.addPyFile(spark_code_path)

	return spark


# launch the web server and run the Flask app
#
# 1. start the log and mention the port and the host address 
# 2. start the cherrypy server

def run_server(app):
 
	# enable WSGI access logging via Paste
	# WSGI stands for Web Server Gateway Interface
	app_logged = TransLogger(app)
 
	# mount the WSGI callable object (app) on the root directory
	cherrypy.tree.graft(app_logged, '/')
 
	# set the configuration of the web server
	cherrypy.config.update({
		'engine.autoreload.on': True,
		'log.screen': True,
		'log.error_file': "cherrypy.log",
		'server.socket_port': WEB_PORT,   # 80, 443 para https
		'server.socket_host': '0.0.0.0'  
	})
		 
	# start the CherryPy WSGI web server
	cherrypy.engine.start()
	cherrypy.engine.block()
 
 
if __name__ == "__main__":    # is script executed directly?
   
	# init spark session and load libraries
	spark_session = init_spark_session()
	
	# dataset path 
	dataset_path = os.path.join(basedir,'data', DATASET)
	# in the web server:
	# dataset_path = DATASET_SERVER

	# create the webapp
	app = create_app(spark_session, dataset_path)  

	# run the web server and the webapp
	run_server(app)
	
