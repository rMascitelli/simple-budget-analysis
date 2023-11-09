import openpyxl
import argparse
from datetime import date

# Categories
TAKEOUT = 'TAKEOUT'
GROCERY = 'GROCERY'
SHOPPING = 'SHOPPING'
UTILS = 'UTILITIES'
UNKNOWN = 'UNKNOWN'

cat_list = [TAKEOUT, GROCERY, SHOPPING, UTILS, UNKNOWN]

tx_categories = {
	# Shopping
	'rottblots': SHOPPING,
	'amazon': SHOPPING,

	# GROCERY
	'costco': GROCERY,
	'loblaws': GROCERY,
	'busy bee': GROCERY,
	'ubereats': GROCERY,

	# TAKEOUT
	'shawarma': TAKEOUT,
	'starbucks': TAKEOUT,
	'tims': TAKEOUT,
	'mcd': TAKEOUT,

	# UTILITIES
	'gas': UTILS
}

def display_transactions(transaction_map):
	print("/////")
	print("//  TRANSACTIONS")
	print("/////")

	for category in transaction_map: 
		if len(transaction_map[category]) > 0:
			print(f"\n{category} :")
			total = 0
			for key, val in transaction_map[category].items():
				if isinstance(val, float):
					print(f"  [{key}]: {val}")
					total += val
				else:
					print(f"  [{key}]:")
					for subkey, subval in val.items():
						print(f"    [{subkey}]: {subval}")
						total += subval
			print(f"  [TOTAL]: {total}")


def main():
	transaction_map={}
	for cat in cat_list:
		transaction_map[cat] = {}

	parser = argparse.ArgumentParser()
	parser.add_argument('until', nargs='?', default=None)
	args = parser.parse_args()

	until = None
	if args.until:
		print("Parsing until day", args.until)
		until = int(args.until)
	else:
		day_of_month = str(date.today()).split('-')[2]
		print(f"Today is {day_of_month}, parsing until then")
		until = int(day_of_month)

	wb = openpyxl.load_workbook('budget.xlsx')
	ws = wb['November Budget']

	for i in range(0, until):
		cell = f'B{i+2}'
		spending = ws[cell].value
		print(f"Looking at day [{i+1}]: {spending}")
		indiv_trans = spending.split(',')
		for tx in indiv_trans:
			print(f"    Transaction: {tx}")
			spent_where = tx.split("_")[0]
			amount = tx.split("_")[1]
			description = None
			if "(" in spent_where:
				description = spent_where.split('(')[1][:-1]
				spent_where = spent_where.split('(')[0]
				print(f"        Spent at: {spent_where}")
				print(f"        Amount: ${amount}")
				print(f"        Description: {description}")
			else:
				print(f"        Spent at: {spent_where}")
				print(f"        Amount: ${amount}")

			category = tx_categories.get(spent_where)
			if not category:
				category = UNKNOWN

			if transaction_map[category].get(spent_where):
				if description:
					if transaction_map[category][spent_where].get(description):
						transaction_map[category][spent_where][description] += float(amount)
					else:	
						transaction_map[category][spent_where][description] = float(amount)
				else:
					transaction_map[category][spent_where] += float(amount)
			else:
				if description:
					transaction_map[category][spent_where] = {description: float(amount)}
				else:
					transaction_map[category][spent_where] = float(amount)

	print("\n\n---\n")

	#print(transaction_map)
	display_transactions(transaction_map)
	


main()
