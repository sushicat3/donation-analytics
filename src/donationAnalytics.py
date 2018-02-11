import re
import datetime
import math

"""
	CMTE_ID				01	alphanumeric
	NAME				08  alpha dashes spaces and commas
	ZIP_CODE			11	First 5
	TRANSACTION_DT		14	MMDDYYYY
	TRANSACTION_AMT 	15	up to 2 decimal places
	OTHER_ID			16	null
"""

P = None

def streamfile(infile, outfile, pfile):
	global P
	with open(pfile, 'r') as pf:
		percentile = pf.readline()
		P = int(percentile)
	
	with open(infile, 'r') as inf:
		with open(outfile, 'w') as outf:
			for line in inf:
				relativeFields = extractRelevantFields(line)
				if relativeFields != None:
					emit = proccessContribution(relativeFields[0], relativeFields[1], relativeFields[2], relativeFields[3], relativeFields[4])
					if emit != None:
						print(emit)
						outf.write(emit + '\n')


def extractRelevantFields(record):
	"""
		record: '|' delimited str with 21 values as described by FED data dictionary
	"""
	fields = []
	records = record.split('|')
	if len(records) == 21:
		cmte = records[0]
		name = records[7]
		zipcode = records[10]
		date = records[13]
		amount = records[14]
		other = records[15]

		fields.append(cmte)
		fields.append(name)
		fields.append(zipcode)
		fields.append(date)
		fields.append(amount)
		fields.append(other)
		
		if validate(fields):
			zipcode = zipcode[:5]
			fields[2] = zipcode
			year = date[4:8]
			fields[3] = year
			fields.pop()
			return cmte, name, zipcode, year, amount

	return None

	
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
	return dataValid(cmte, '[a-zA-Z0-9]+')


def nameValid(name):
	return dataValid(name, '[a-zA-Z, -]+')


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


# hash map for NAME|ZIP : YEAR (earlist year observed as repeat donor)
DONOR = {}
# hash map for CMTE_ID|ZIP_CODE|YEAR : [TRANSACTION_AMT, ...] (list of amounts observed from repeat donors)
RECIPIENT_AREA_YEAR = {}

def proccessContribution(recipient, donor, zipcode, year, amount):
	k = donor + '|' + zipcode
	v = year
	if k in DONOR:
		# if year is != to current(v), this is a repeat donor
		if DONOR[k] != v:
			# repeat donor!
			# make sure in order, if not update
			if DONOR[k] >= v:
				DONOR[k] = v
				# ignore this row if not in order
			else:
				# the year is in order and is after
				# this is a repeat donor
				# find out how much is being donated to this recipient from this area this year
				amounts = proccessRepeatDonor(recipient, zipcode, year, amount)
				if amounts != None:
					# we can calculate and emit data
					e = emit(recipient, zipcode, year, amounts)
					return(e)
	else:
		# this is a new donor
		# add to the hashmap
		DONOR[k] = v
		return None


def proccessRepeatDonor(recipient, zipcode, year, amount):
	k = recipient + '|' + zipcode + '|' + year
	v = float(amount)
	if k in RECIPIENT_AREA_YEAR:
		# there are already some repeat donors for this RECIPIENT, AREA and YEAR
		# append the value
		RECIPIENT_AREA_YEAR[k].append(v)
	else:
		# this is the first repeat donor for the given RECIPIENT, AREA and YEAR
		RECIPIENT_AREA_YEAR[k] = [v]

	# the list of amounts for the given RECIPIENT, AREA and YEAR
	return RECIPIENT_AREA_YEAR[k]


def emit(recipient, zipcode, year, amounts):
	perc = rounder(percentile(amounts))
	totalamount = rounder(sum(amounts))
	matches = len(amounts)
	emit = recipient + '|' + zipcode + '|' + year + '|' + str(perc) + '|' + str(totalamount) + '|' + str(matches)
	return(emit)

def percentile(amounts):
	ordinal = int(math.ceil((P / 100.0) * len(amounts)))
	return amounts[ordinal-1]

def rounder(number):
	upper = math.ceil(number)
	if upper - number <= 0.5:
		return int(upper)
	else:
		return int(upper - 1)

def main():
	infile = '../input/itcont.txt'
	outfile = '../output/repeat_donors.txt'
	pfile = '../input/percentile.txt'
	streamfile(infile, outfile, pfile)

if __name__ == '__main__':
	main()