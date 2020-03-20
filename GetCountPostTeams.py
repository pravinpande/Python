import cx_Oracle
import snowflake.connector
import sys
import csv
import os
from tabulate import tabulate
import pymsteams

exp_dir = os.path.normpath('C:/Users/ppande/Documents/2019.8.3')
exp_file_name = 'PS_Count_Diff.csv'
exp_path = os.path.join(exp_dir, exp_file_name)


def runSQL(table):
	statement = "select '{0}', count(0) from  {0}".format(table.replace(' ',''))
	return statement
	

if __name__ == '__main__':

	tables = [
'PS_LEDGER         ',
'PS_LEDGER_CODE_DTL',
'PS_VOUCHER        ']
	my_list = []
	x = []
	
	try:
		conn_str = u'*****'
		curcon = cx_Oracle.connect(conn_str) 
		cursor = curcon.cursor()

		ctx = snowflake.connector.connect(
			user='*****', 
            password='****', 
            account='*****', 
            role='*****',
            WAREHOUSE='*****',
            database='*****',
            schema='*****')
		cursor2 = ctx.cursor()

		#sql_query = "SELECT * FROM INFORMATION_SCHEMA.TABLES WHERE TABLE_SCHEMA='*****' AND TABLE_NAME NOT LIKE '%LOG' AND TABLE_NAME NOT LIKE '%NRT';"
		#cursor2.execute(sql_query)
		#tables = list(cursor2.fetchall())

		for table in tables:
			sql = runSQL(table)
			cursor.execute(sql)
			o_count =  cursor.fetchone()[1]
			cursor2.execute(sql)
			s_count = cursor2.fetchone()[1]
			my_list.append([table,o_count,s_count, o_count - s_count])

		outputFile = open(exp_path,'w', newline='') 
		writer = csv.DictWriter(outputFile,fieldnames=["Table Name","Source","Target","Difference"])
		writer.writeheader()
		output = csv.writer(outputFile)
		for data in my_list:
			output.writerow(data)
			if data[3] >= 0:
				x.append(data)
		
		html = """{table}"""
		text = html.format(table=tabulate(x,headers=["Table Name", "Source Count", "Target Count", "Difference"], tablefmt="html"))
		myteams = pymsteams.connectorcard("https://outlook.office.com/webhook/93b7788a-27cc-435a-9506-ee6eb354a359@9d9a57a9-f226-4188-bad7-fc1cb39566b6/IncomingWebhook/")
		myteams.text(text)
		myteams.title("PeopleSoft Tables")
		myteams.send()
		

	finally:
		outputFile.close()
		cursor.close()
		cursor2.close()

