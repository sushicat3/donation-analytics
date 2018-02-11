import donationAnalytics


readmeEx = [
	'C00629618|N|TER|P|201701230300133512|15C|IND|PEREZ, JOHN A|LOS ANGELES|CA|90017|PRINCIPAL|DOUBLE NICKEL ADVISORS|01032017|40|H6CA34245|SA01251735122|1141239|||2012520171368850783',
	'C00177436|N|M2|P|201702039042410894|15|IND|DEEHAN, WILLIAM N|ALPHARETTA|GA|300047357|UNUM|SVP, SALES, CL|01312017|384||PR2283873845050|1147350||P/R DEDUCTION ($192.00 BI-WEEKLY)|4020820171370029337',
	'C00384818|N|M2|P|201702039042412112|15|IND|ABBOTT, JOSEPH|WOONSOCKET|RI|028956146|CVS HEALTH|VP, RETAIL PHARMACY OPS|01122017|250||2017020211435-887|1147467|||4020820171370030285',
	'C00384516|N|M2|P|201702039042410893|15|IND|SABOURIN, JAMES|LOOKOUT MOUNTAIN|GA|028956146|UNUM|SVP, CORPORATE COMMUNICATIONS|01312017|230||PR1890575345050|1147350||P/R DEDUCTION ($115.00 BI-WEEKLY)|4020820171370029335',
	'C00177436|N|M2|P|201702039042410895|15|IND|JEROME, CHRISTOPHER|LOOKOUT MOUNTAIN|GA|307502818|UNUM|EVP, GLOBAL SERVICES|10312017|384||PR2283905245050|1147350||P/R DEDUCTION ($192.00 BI-WEEKLY)|4020820171370029342',
	'C00384516|N|M2|P|201702039042412112|15|IND|ABBOTT, JOSEPH|WOONSOCKET|RI|028956146|CVS HEALTH|EVP, HEAD OF RETAIL OPERATIONS|01122018|333||2017020211435-910|1147467|||4020820171370030287',
	'C00384516|N|M2|P|201702039042410894|15|IND|SABOURIN, JAMES|LOOKOUT MOUNTAIN|GA|028956146|UNUM|SVP, CORPORATE COMMUNICATIONS|01312018|384||PR2283904845050|1147350||P/R DEDUCTION ($192.00 BI-WEEKLY)|4020820171370029339'
]

# print('------------------------------------')
# print('testing stream processor:')

# for line in readmeEx:
# 	relativeFields = donationAnalytics.extractRelevantFields(line)
# 	# print(relativeFields)
# 	if relativeFields != None:
# 		emit = donationAnalytics.proccessContribution(relativeFields[0], relativeFields[1], relativeFields[2], relativeFields[3], relativeFields[4])
# 		if emit != None:
# 			print(emit)

# print(donationAnalytics.DONOR)
# print(donationAnalytics.RECIPIENT_AREA_YEAR)

print('------------------------------------')
print('Validating two . precision:')
print(donationAnalytics.amountValid('2222.22'))
print(donationAnalytics.amountValid('22fdsafds22.22'))
print(donationAnalytics.amountValid('2324324324324324222.22'))
print(donationAnalytics.amountValid('224322.22343'))
print(donationAnalytics.amountValid('2222.2'))
print(donationAnalytics.amountValid('2222.'))
print(donationAnalytics.amountValid('484'))

print('------------------------------------')
print('test round:')

print(donationAnalytics.rounder(7.99))
print(donationAnalytics.rounder(7.09))
print(donationAnalytics.rounder(.50))

print('------------------------------------')
print('test nameValid:')
print(donationAnalytics.nameValid('B_2(*-Bhatt, Swetal'))
print(donationAnalytics.nameValid('B3920q-Bhatt, Swetal'))
print(donationAnalytics.nameValid('Bhatt-Bhatt, Swetal'))

print('------------------------------------')
print('test zipValid:')
print(donationAnalytics.zipValid('2'))
print(donationAnalytics.zipValid('2432'))
print(donationAnalytics.zipValid('fdsafdsa'))
print(donationAnalytics.zipValid('12334'))
print(donationAnalytics.zipValid('212332323'))

print('------------------------------------')
print('test cmteValid:')
print(donationAnalytics.cmteValid('kfjdsa8329f32qdsFDSF'))

print('------------------------------------')
print('test dateValid:')
print(donationAnalytics.dateValid('01014444'))
print(donationAnalytics.dateValid('65012018'))
print(donationAnalytics.dateValid('01782018'))
print(donationAnalytics.dateValid('02292018'))
print(donationAnalytics.dateValid('01012018'))


print('------------------------------------')
print('test io:')
infile = '../input/itcont.txt'
outfile = '../output/repeat_donors.txt'
pfile = '../input/percentile.txt'
donationAnalytics.streamfile(infile, outfile, pfile)

print(donationAnalytics.DONOR)
print(donationAnalytics.RECIPIENT_AREA_YEAR)
