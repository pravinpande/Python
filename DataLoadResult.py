import pandas as pd
import win32com.client as win32
import snowflake.connector

ctx = snowflake.connector.connect(
			user='', 
            password='', 
            account='', 
            role='',
            warehouse='',
            database='')

query = "WITH DATE AS (SELECT NAME,DATABASE_NAME,SCHEMA_NAME,SCHEDULED_TIME,COMPLETED_TIME,STATE,ERROR_CODE,ERROR_MESSAGE,ROW_NUMBER() OVER(PARTITION BY NAME,DATABASE_NAME,SCHEMA_NAME ORDER BY SCHEDULED_TIME DESC) RN FROM TABLE(INFORMATION_SCHEMA.TASK_HISTORY()) WHERE NAME IN ('','') AND STATE!='SCHEDULED' AND DATABASE_NAME='') SELECT NAME,DATABASE_NAME,STATE,ERROR_CODE,ERROR_MESSAGE,CONVERT_TIMEZONE('America/New_York',SCHEDULED_TIME) AS SCHEDULED_TIME_EST,CONVERT_TIMEZONE('America/New_York',COMPLETED_TIME) AS COMPLETED_TIME_EST FROM DATE WHERE RN=1;"

df = pd.read_sql(query,ctx)
email = "{df}"
email = email.format(df=df.to_html())

outlook = win32.Dispatch('outlook.application')
mail = outlook.CreateItem(0)
mail.To = ''
mail.Subject = 'SNF Dataload Results'
mail.Body = str(email)
mail.HTMLBody = str(email)

mail.Send()
