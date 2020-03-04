import snowflake.connector


def getColumuns(filename):
	"""
	This function takes flat file as input with 
	table name and respective primary keys
	"""
	tables = {}

	with open(filename) as f:
		for line in f:
			line = line.strip()
			if 'Primary Key' in line:
				continue

			cols = line.split(',')
			table = cols[0].strip()
			col = cols[1].strip()

			if table in tables:
				tables[table].append(col)
			else:
				tables[table] = [col]
	return tables

def runSQL(table, columns):
	"""
	This function runs the dynamic SQL for every table
	and primary key combination

	"""
	statement = "select '{1}', count(0) from (select {0} from {1} group by {0} having count(0) > 1)".format(', '.join(columns), table.replace(' ',''))
	return statement

if __name__ == '__main__':
	"""
	This function calls above functions and connects to Snowflake
	"""
	tables = getColumuns('Test.csv')
	try:
		ctx = snowflake.connector.connect(user='****', password='****', account='****', role='***')
		cursor = ctx.cursor()
		cursor.execute("USE WAREHOUSE ****")
		cursor.execute("USE DATABASE ****")
		cursor.execute("USE SCHEMA ****")
		for table in tables:
			sql = runSQL(table,tables[table])
			try:
				cursor.execute(sql)
			except:
				pass
			for result in cursor:
				print(result)

	finally:
		cursor.close()
	ctx.close()
