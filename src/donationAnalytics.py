import re
import datetime

"""
	CMTE_ID				01	alphanumeric
	NAME				08  alpha dashes spaces and commas
	ZIP_CODE			11	First 5
	TRANSACTION_DT		14	MMDDYYYY
	TRANSACTION_AMT 	15	up to 2 decimal places
	OTHER_ID			16	null
"""

def extractRelevantFields(record):
	"""
		record: '|' delimited str with 21 values as described by FED data dictionary
	"""
	relevantFields = []
	records = record.split('|')
	if len(records) == 21:
		relevantFields.append(records[0])
		relevantFields.append(records[7])
		relevantFields.append(records[10])
		relevantFields.append(records[13])
		relevantFields.append(records[14])
		relevantFields.append(records[15])
		
	return relevantFields


	
def validate(relevantFields):
	
	if relevantFields[5] != '':
		return False

	if cmteValid(relevantFields[0]) == False:
		return False

	if nameValid(relevantFields[1]) == False:
		return False

	if zipValid(relevantFields[2]) == False:
		return False

	if dateValid(relevantFields[3]) == False:
		return False

	return True

def cmteValid(cmte):
	cmteValidator = re.compile('[a-zA-Z0-9]+')
	cmteMatch = cmteValidator.match(cmte)
	if cmteMatch != None and len(cmte) == cmteMatch.end():
		return True

	return False


def nameValid(name):
	nameValidator = re.compile('[a-zA-Z, -]+')
	nameMatch = nameValidator.match(name)
	if nameMatch != None and len(name) == nameMatch.end():
		return True

	return False

def zipValid(zipcode):
	zipValidator = re.compile('[0-9]{5,9}')
	zipMatch = zipValidator.match(zipcode)
	if zipMatch != None and len(zipcode) == zipMatch.end():
		return True

	return False


def dateValid(date):
	dateValidator = re.compile('[0-9]{8}')
	dateMatch = dateValidator.match(date)
	if dateMatch != None and len(date) == dateMatch.end():
		
		# validate using datetime
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


def proccessContribution(fields):
	"""
		fields: list
			[recipient, donor, zip, date, amount]
		returns 
	"""
	pass
