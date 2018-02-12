import math
import validator
import bstree


# Global variable for percentile
P = None


def streamfile(infile, outfile, pfile):
	"""
		Function for reading in input files, and processing itcont.txt like a stream.
		For each line:
			- first the "relevant fields" are extracted. These are the fields used to
			  determine the reapeat donors and their contributions.
			- then the "relevant fields" are "proccessed" to see if they contain
			  information about a repeat donor. If they do, a line containing
			  the output data is "emmited"
			- the "emitted" line is written to the output file.

	"""
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
		
		fields to check:
			CMTE_ID				01	alphanumeric
			NAME				08  alpha dashes spaces and commas
			ZIP_CODE			11	First 5
			TRANSACTION_DT		14	MMDDYYYY
			TRANSACTION_AMT 	15	up to 2 decimal places
			OTHER_ID			16	null

		if those fields are validated...

			returns (cmte, name, zipcode, year, amount)

		otherwise this line can be skipped...
			returns None

	"""
	records = record.split('|')
	if len(records) == 21:
		cmte = records[0]
		name = records[7]
		zipcode = records[10]
		date = records[13]
		amount = records[14]
		other = records[15]
		
		if validator.validate(cmte, name, zipcode, date, amount, other):
			zipcode = zipcode[:5]
			year = date[4:8]
			return cmte, name, zipcode, year, amount

	return None
	

"""
	hash map:
		NAME|ZIP_CODE : YEAR

	To quickly (O(1)) find if a donor is a repeat donor. If they are, they will
	be in the hash map with an earlier year.

"""
DONOR = {}


"""
	hash map:
		CMTE_ID|ZIP_CODE|YEAR : BSTree(TRANSACTION_AMT)

	To quickly (O(1)) find all amounts dontated by repeat donors in a particular 
	zip code, during a particular year, to a particlar committee.

"""
RECIPIENT_AREA_YEAR = {}


def proccessContribution(recipient, donor, zipcode, year, amount):
	"""
		Takes information from a new contribution, and determines if it
		is from a repeat donor using the DONOR hashmap. If so, the percentile
		is calculated.

		returns output line with percentile if this is a repeat donor.
		otherwise, returns None.

	"""
	k = donor + '|' + zipcode
	v = year
	if k in DONOR:
		if DONOR[k] != v:
			if int(DONOR[k]) >= int(v):
				# if not in order, update
				DONOR[k] = v
			else:
				amounts = proccessRepeatDonor(recipient, zipcode, year, amount)
				e = emit(recipient, zipcode, year, amounts)
				return(e)
	else:
		# new donor, add to the hashmap
		DONOR[k] = v
		return None


def proccessRepeatDonor(recipient, zipcode, year, amount):
	"""
		Takes the contribution data about the repeat donor and uses it to obtain
		all amounts dontated by repeat donors in a with that zip code, during that
		particular year, to that particlar committee, (so they may be used to 
		calculate the percentile)

		returns the BSTree of TRANSACTION_AMTs for the given RECIPIENT, AREA and YEAR

	"""
	k = recipient + '|' + zipcode + '|' + year
	v = float(amount)
	if k in RECIPIENT_AREA_YEAR:
		RECIPIENT_AREA_YEAR[k].insert(v)
	else:
		RECIPIENT_AREA_YEAR[k] = bstree.BSTree()
		RECIPIENT_AREA_YEAR[k].insert(v)
 
	return RECIPIENT_AREA_YEAR[k]


def emit(recipient, zipcode, year, amounts):
	"""
		Calculates all the values in the output string:
			recipient|zipcode|year|percentile|total amount|total contributions

		the total amount is stored in the bst as "total"
		the total contributions are stored in the bst as "size"
	"""
	perc = rounder(percentile(amounts))
	totalamount = rounder(amounts.total)
	matches = amounts.size
	emit = recipient + '|' + zipcode + '|' + year + '|' + str(perc) + '|' + str(totalamount) + '|' + str(matches)
	return(emit)


def percentile(amounts):
	"""
		amounts: BSTree with all the amounts needed for percentile calculation.

		Percentile calculation: ceil(P/100 * N) = n, where the nth element of an ordered 
		list of N elements, is the Pth percentile.

	"""
	ordinal = int(math.ceil((P / 100.0) * amounts.size))
	return amounts.findNth(ordinal)


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