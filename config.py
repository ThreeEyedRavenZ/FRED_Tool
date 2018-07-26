""" settings for the applications
This file contains some constants used for FRED API requests and the interface.
"""
## registered FRED API Key
fred_api_key = "894d34e924b71cabb177c762fce5ced3"
## FRED webservice URL
fred_webservice = "https://api.stlouisfed.org/fred/"
## Frequency dictionary 
freq_list = {
	'': "", 
	'Daily Close': 'd', 
	'Annual, Fiscal Year': 'a',
	'Daily': 'd', 
	'Weekly': 'w',
	'Biweekly': 'bw',
	'Monthly': 'm',
	'Quarterly': 'q', 
	'Semiannual': 'sa', 
	'Annual': 'a',
	'Weekly, Ending Friday': 'wef', 
	'Weekly, Ending Thursday': 'weth',
	'Weekly, Ending Wednesday': 'wew',
	'Weekly, Ending Tuesday': 'wetu', 
	'Weekly, Ending Monday': 'wem', 
	'Weekly, Ending Sunday': 'wesu',
	'Weekly, Ending Saturday': 'wesa', 
	'Biweekly, Ending Wednesday': 'bwew',
	'Biweekly, Ending Monday' : 'bwem'
}

FRED_ID_NAME = 'id'
FRED_FREQUENCY_NAME = 'frequency'
APP_NAME = 'FRED Data Downloader'
DEFAULT_START_DATE = '1776-07-04'
DEFAULT_END_DATE = '9999-12-31'