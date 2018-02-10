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
	pass

def proccessContribution(fields):
	"""
		fields: list
			[recipient, donor, zip, date, amount]
		returns 
	"""
	pass
