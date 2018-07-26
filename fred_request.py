from config import fred_webservice, fred_api_key, DEFAULT_START_DATE, DEFAULT_END_DATE 
import requests
import json
import pandas as pd

class fred_data_query:
	"""
	FRED Data Query
	"""
	__folder = "series/search?"
	__webservice = ""
	__result = None
	def __init__(self, key_words):
		"""Function to initialize fred_data_query
		
		Initialize the URL needed for HttpGet based on the key_words
		"""
		self.__webservice = fred_webservice+\
							self.__folder+\
							"search_text={key_words}&"+\
							"api_key={api_key}&"+\
							"file_type=json&"+\
							"limit=10"
		self.__webservice = self.__webservice.format(key_words=key_words, 
											   api_key=fred_api_key)

	def search(self):
		"""
		Function to call the FRED webserice and retrieve the search result
		"""
		response = requests.get(self.__webservice)
		self.__result = pd.DataFrame(response.json()['seriess'])
		try:
			self.__result = self.__result.drop(['realtime_end', 'realtime_start'], 1)
		except:
			## sometimes, no result can be found based on your key_words
			print 'no data'

	def get_result(self):
		"""
		Function to return the search result as a panda dataframe
		"""
		return self.__result

class fred_data_downloader:
	"""
	FRED Data Downloader
	"""
	__folder = "series/observations?"
	__webservice = ""
	__result = None
	def __init__(self, selected_series_id, 
					   observation_start_date=DEFAULT_START_DATE, 
					   observation_end_date=DEFAULT_END_DATE, 
					   freq=""):
		""" 
		Function to initialize the webservice to retrieve data

		The default start date and end date are "1776-07-04" and "9999-12-31"
		"""
		self.__webservice = fred_webservice+\
							self.__folder+\
							"series_id={series_id}&"+\
							"observation_start={observation_start}&"+\
							"observation_end={observation_end}&"+\
							"frequency={freq}&"+\
							"api_key={api_key}&"+\
							"file_type=json"
		self.__webservice = self.__webservice.format(series_id=selected_series_id,
													observation_start=observation_start_date,
													observation_end=observation_end_date,
													freq=freq,
													api_key=fred_api_key)			
	def retrieve(self):
		"""
		Function to retrieve the data for a specified series ID
		"""
		response = requests.get(self.__webservice)
		try:
			self.__result = pd.DataFrame(response.json()['observations'])
			self.__result = self.__result.drop(['realtime_end', 'realtime_start'], 1)
		except:
			self.__result = None

	def get_data(self):
		"""
		Function to return the data
		"""
		return self.__result

