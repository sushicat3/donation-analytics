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
	fields = []
	records = record.split('|')
	if len(records) == 21:
		fields.append(records[0])
		fields.append(records[7])
		fields.append(records[10])
		fields.append(records[13])
		fields.append(records[14])
		fields.append(records[15])
		
	if validate(fields):
		fields[2] = fields[2][:5]
		fields.pop()
	else:
		return None
	
	return fields


	
def validate(fields):

	if len(fields) != 6:
		return False
	
	if fields[5] != '':
		return False

	if cmteValid(fields[0]) == False:
		return False

	if nameValid(fields[1]) == False:
		return False

	if zipValid(fields[2]) == False:
		return False

	if dateValid(fields[3]) == False:
		return False

	if amountValid(fields[4]) == False:
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


def amountValid(amount):
	if len(amount) <= 14:
		amountValidator = re.compile('[0-9]+(\.[0-9][0-9]?)?')
		amountMatch = amountValidator.match(amount)
		if amountMatch != None and len(amount) == amountMatch.end():
			return True

	return False

def proccessContribution(fields):
	"""
		fields: list
			[recipient, donor, zip, date, amount]
		returns 
	"""
	pass
