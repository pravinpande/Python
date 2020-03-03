import cx_Oracle
import snowflake.connector
import sys
import csv
import os
from tabulate import tabulate
import pymsteams
import regex
import sqlalchemy.pool as pool
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

exp_dir = os.path.normpath('C:/Users/2019.8.3')
exp_file_name = 'ODS_Count_Diff.csv'
exp_path = os.path.join(exp_dir, exp_file_name)

o_host = 'ods'
o_port = 000
sid = 'ODSC'
user = 'pravin'
pwd = '****'
sid = cx_Oracle.makedsn(o_host, o_port, sid=sid)

def runSQL(table):
	statement = "select '{0}', count(0) from  {0}".format(table.replace(' ',''))
	return statement
	

if __name__ == '__main__':

	tables = [
'MAT_DEGREE                    ',
'MAT_INTEREST                  ']
	my_list = []
	x = []
	
	try:
		#conn_str = 
		cstr = 'oracle://{user}:{password}@{sid}'.format(
			user = user,
			password = pwd,
			sid = sid

			)

		engine = create_engine(
			cstr,
			convert_unicode = False,
			pool_recycle = 10,
			pool_size = 50,
			echo = True
			)
		#metadata.bind = engine
		DBSession = sessionmaker(bind=engine)
		session = DBSession()
		cursor = engine.connect()

		ctx = snowflake.connector.connect(
			****)
		cursor2 = ctx.cursor()



		for table in tables:
			sql = runSQL(table)
			cursor.execute(sql)
			o_count =  cursor.fetchone()[1]

			if re.match(re.compile('^M'),table):
				cursor2.execute("USE SCHEMA BRAMGR;")
				cursor2.execute(sql)
				s_count = cursor2.fetchone()[1]
			elif re.match(re.compile('^G'),table):
				cursor2.execute("USE SCHEMA BRARAL;")
				cursor2.execute(sql)
				s_count = cursor2.fetchone()[1]
			elif re.match(re.compile('^S'),table):
				cursor2.execute("USE SCHEMA BRAURN;")
				cursor2.execute(sql)
				s_count = cursor2.fetchone()[1]
			elif re.match(re.compile('^T'),table):
				cursor2.execute("USE SCHEMA BRASMGR;")
				cursor2.execute(sql)
				s_count = cursor2.fetchone()[1]

			my_list.append([table,o_count,s_count, o_count - s_count])

		outputFile = open(exp_path,'w', newline='') 
		writer = csv.DictWriter(outputFile,fieldnames=["Table Name","Source","Target","Difference"])
		writer.writeheader()
		output = csv.writer(outputFile)
		for data in my_list:
			output.writerow(data)
			if data[3] > 100:
				x.append(data)
		
		html = """{table}"""
		text = html.format(table=tabulate(x,headers=["Table Name", "Source Count", "Target Count", "Difference"], tablefmt="html"))
		myteams = pymsteams.connectorcard("https://outlook.office.com/webhook/d132ea53-c316-4fc2-ac8e-7dc745f45b9b@9d9a57a9-f226-4188-bad7-fc1cb39566b6/IncomingWebhook/a4da1a")
		myteams.text(text)
		myteams.title("ODS Tables")
		myteams.send()
	
	except cx_Oracle.Error as exc:
		error, = exc.args
		print("Oracle Error", error.code)
		print("Message", error.message)

	#finally:
		#outputFile.close()
		#cursor.close()
		#cursor2.close()
		#t.cancel()
		#pool.release(curcon)
		#curcon.close()
