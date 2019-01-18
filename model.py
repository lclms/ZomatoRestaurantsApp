import logging

import pandas
import json

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# The main class to deal with Spark data computation 

class ZomatoRestaurantsApark:

	def __init__(self, spark_session, filename):
		logger.info("Starting up ZomatoRestaurantsApark...")
		self.sc = spark_session
		self.airbnb_df = self.sc.read.format("csv")\
			.option("header","true")\
			.option("inferSchema", "true")\
			.load(filename);
		self.airbnb_df.createOrReplaceTempView("zomato")
		self.airbnb_df.cache()
		self.airbnb_df.printSchema()
		logger.info("Data model built")

	def filtering(self, list_countries, list_city):
		logger.info("Filtering data. It may take a while...")
		self.listcountries = list_countries
		self.listcity = list_city

		# must get rid of limit later on. Just using it while developing code 
		if self.listcity:
			str_listings = "SELECT `Restaurant Name` AS restaurantName, Cuisines, `Rating color`as ratingColor, `Price range` as priceRange, `Aggregate rating` as aggregateating, City as city, Latitude, Longitude FROM zomato WHERE `Country Code` = '%s' AND zomato.City = '%s'" % (self.listcountries, self.listcity)
		else:
			str_listings = "SELECT `Restaurant Name` AS restaurantName, Cuisines, `Rating color`as ratingColor, `Price range` as priceRange, `Aggregate rating` as aggregateating, City as city, Latitude, Longitude FROM zomato WHERE `Country Code` = '%s'" % self.listcountries

		
		self.df_listings = self.sc.sql(str_listings)
		logger.info("Data filtered")

	def barchart(self, option, list_countries):
		logger.info("Filtering data. It may take a while...")
		self.option = option
		self.list_countries = list_countries
		str_listings = ""
		var_list_countries = ""
		for x in self.list_countries:
			var_list_countries = var_list_countries + "'" + x + "'" + ","
			if x == self.list_countries[-1]:
				var_list_countries = var_list_countries + "'" + x + "'"

		if self.option == 1:
			str_listings = "SELECT `Country Code` as country, COUNT('`Restaurant ID`') as num_restaurants_by_country FROM zomato WHERE `Country Code` IN ("+var_list_countries+") GROUP BY `Country Code`"
		elif self.option == 3:
			str_listings = "SELECT `Country Code` as country, COUNT('`Restaurant ID`') as num_restaurants_by_country FROM zomato WHERE `Country Code` IN ("+var_list_countries+") AND `Rating text` = 'Excellent' GROUP BY `Country Code`"
		elif self.option == 4:
			str_listings = "SELECT `Country Code` as country, COUNT('`Restaurant ID`') as num_restaurants_by_country FROM zomato WHERE `Country Code` IN ("+var_list_countries+") AND `Rating text` = 'Very Good' GROUP BY `Country Code`"
		elif self.option == 5:
			str_listings = "SELECT `Country Code` as country, COUNT('`Restaurant ID`') as num_restaurants_by_country FROM zomato WHERE `Country Code` IN ("+var_list_countries+") AND `Rating text` = 'Good' GROUP BY `Country Code`"
		elif self.option == 6:
			str_listings = "SELECT `Country Code` as country, COUNT('`Restaurant ID`') as num_restaurants_by_country FROM zomato WHERE `Country Code` IN ("+var_list_countries+") AND `Rating text` = 'Average' GROUP BY `Country Code`"
		else:
			str_listings = "SELECT `Country Code` as country, COUNT('`Restaurant ID`') as num_restaurants_by_country FROM zomato WHERE `Country Code` IN ("+var_list_countries+") AND `Rating text` = 'Poor' GROUP BY `Country Code`"


		# must get rid of limit later on. Just using it while developing code 
	
		
		self.df_hosts_profiling = self.sc.sql(str_listings)
		logger.info("Data filtered")

	def bubblechart(self, option, list_countries):
		logger.info("Filtering data. It may take a while...")
		self.option = option
		self.list_countries = list_countries
		str_listings = ""
		var_list_countries = ""
		for x in self.list_countries:
			var_list_countries = var_list_countries + "'" + x + "'" + ","
			if x == self.list_countries[-1]:
				var_list_countries = var_list_countries + "'" + x + "'"

		if self.option == 1:
			str_listings = "SELECT `Country Code` as Name, COUNT('`Restaurant ID`') as Count FROM zomato WHERE `Country Code` IN ("+var_list_countries+") GROUP BY `Country Code`"
		elif self.option == 3:
			str_listings = "SELECT `Country Code` as Name, COUNT('`Restaurant ID`') as Count FROM zomato WHERE `Country Code` IN ("+var_list_countries+") AND `Rating text` = 'Excellent' GROUP BY `Country Code`"
		elif self.option == 4:
			str_listings = "SELECT `Country Code` as Name, COUNT('`Restaurant ID`') as Count FROM zomato WHERE `Country Code` IN ("+var_list_countries+") AND `Rating text` = 'Very Good' GROUP BY `Country Code`"
		elif self.option == 5:
			str_listings = "SELECT `Country Code` as Name, COUNT('`Restaurant ID`') as Count FROM zomato WHERE `Country Code` IN ("+var_list_countries+") AND `Rating text` = 'Good' GROUP BY `Country Code`"
		elif self.option == 6:
			str_listings = "SELECT `Country Code` as Name, COUNT('`Restaurant ID`') as Count FROM zomato WHERE `Country Code` IN ("+var_list_countries+") AND `Rating text` = 'Average' GROUP BY `Country Code`"
		else:
			str_listings = "SELECT `Country Code` as Name, COUNT('`Restaurant ID`') as Count FROM zomato WHERE `Country Code` IN ("+var_list_countries+") AND `Rating text` = 'Poor' GROUP BY `Country Code`"

		
		self.df_hosts_profiling = self.sc.sql(str_listings)
	
	def treemap(self):
		logger.info("Filtering data. It may take a while...")
		str_listings = "SELECT City as key, `Country Code` as region, Locality as subregion, COUNT('`Restaurant ID`') as value FROM zomato GROUP BY City, `Country Code`, Locality"
		self.df_hosts_profiling = self.sc.sql(str_listings)

	# return the listings dataframe but in json format
	def getListings(self):
		listings = self.df_listings.toPandas().to_dict(orient='records')
		listings = json.dumps(listings, indent=2)
		return listings

	# return the hosts profiling dataframe but in json format
	def getHostsProfiling(self):
		hosts_profiling = self.df_hosts_profiling.toPandas().to_dict(orient='records')
		hosts_profiling = json.dumps(hosts_profiling, indent=2)
		return hosts_profiling
	
	

