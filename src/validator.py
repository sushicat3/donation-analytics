import re
import datetime


def validate(cmte, name, zipcode, date, amount, other):
	
	if other != '':
		return False

	if cmteValid(cmte) == False:
		return False

	if nameValid(name) == False:
		return False

	if zipValid(zipcode) == False:
		return False

	if dateValid(date) == False:
		return False

	if amountValid(amount) == False:
		return False

	return True


def cmteValid(cmte):
	return dataValid(cmte, '[a-zA-Z0-9]+')


def nameValid(name):
	return dataValid(name, '[a-zA-Z, -\.]+')


def zipValid(zipcode):
	return dataValid(zipcode, '[0-9]{5,9}')


def dateValid(date):
	if dataValid(date, '[0-9]{8}'):
		# validate using datetime for no invalid dates
		# no future dates
		month = int(date[:2])
		day = int(date[2:4])
		year = int(date[4:8])
		now = datetime.datetime.now()
		try:
			dateObject = datetime.datetime(year=year, month=month, day=day)
			if dateObject <= now:
				return True
		except ValueError as e:
			return False

	return False


def amountValid(amount):
	if len(amount) <= 14:
		return dataValid(amount, '[0-9]+(\.[0-9][0-9]?)?')

	return False


def dataValid(data, regex):
	"""
		Initial Regex validation. 
		Returns True if the regex matches the whole data string. 
		
	"""
	dataValidator = re.compile(regex)
	dataMatch = dataValidator.match(data)
	if dataMatch != None and len(data) == dataMatch.end():
		return True

	return False
