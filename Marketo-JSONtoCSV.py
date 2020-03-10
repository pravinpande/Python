import json
import csv
import os
import codecs
import sys
import datetime
import logging
import traceback
reload(sys)
sys.setdefaultencoding('utf8')

def my_get(mdict, key, sub_key):
    if isinstance(mdict, dict):
        mvalue = mdict.get(key)
        if isinstance(mvalue, dict):
            return mvalue.get(sub_key)
        else:
            return mvalue
    else:
        return None

def setup_log_file(filename):
    logging.basicConfig(filename = filename,
                        filemode='w',
                        level=logging.DEBUG,
                        format= '%(asctime)s,%(msecs)d %(levelname)-8s [%(filename)s:%(lineno)d] %(message)s',
                        datefmt='%d-%m-%Y:%H:%M:%S',
                        )

'''    
def log_inner_exception(ReqID,ResID):
    logger = logging.getLogger(__name__)
    logger.error("Request ID {ReqID} and Result ID {ResID}", exc_info=True)
'''

def log_exception(exp):
    logger = logging.getLogger(__name__)
    logger.error("Failed to read JSON file", exc_info=True)

   
file_dir = os.path.normpath('/home/marketo/staging/')
exp_dir = os.path.normpath('/home/marketo/CSV/')
log_dir = os.path.normpath('/home/marketo/Logs/')
exp_file_name = 'emails.csv'
log_file_name = 'log_Emails.log'
exp_path = os.path.join(exp_dir, exp_file_name)
log_path = os.path.join(log_dir, log_file_name)
setup_log_file(log_path)

my_dict_list =[]

try:    
    for f in os.listdir(file_dir):
        if f.endswith('.json') and f.startswith('emails_'):
            file_path = os.path.join(file_dir, f)
            data = open(file_path, 'r')
            for line in data:
                parsed_data = json.loads(line)
                for result in parsed_data["result"]:
                    my_dict = {}
                    my_dict["REQUEST_ID"] = parsed_data["requestId"]
                    my_dict["SUCCESS"] = parsed_data["success"]
                    my_dict["RESULT_ID"] = my_get(result,"id",'')
                    my_dict["NAME"] = my_get(result,"name",'')
                    my_dict["DESCRIPTION"] = my_get(result,"description",'')
                    my_dict["STATUS"] = my_get(result,"status",'')
                    my_dict["FOLDER_TYPE"] = my_get(result,"folder","type")
                    my_dict["FOLDER_ID"] = my_get(result,"folder","value")
                    my_dict["FOLDER_NAME"] = my_get(result,"folder","folderName")
                    my_dict["FROM_EMAIL_TYPE"] = my_get(result,"fromEmail","type")
                    my_dict["FROM_EMAIL_VALUE"] = my_get(result,"fromEmail","value")
                    my_dict["FROM_NAME_TYPE"] = my_get(result,"fromName","type")
                    my_dict["FROM_NAME_VALUE"] = my_get(result,"fromName","value")
                    my_dict["REPLY_EMAIL_TYPE"] = my_get(result,"replyEmail","type")
                    my_dict["REPLY_EMAIL_VALUE"] = my_get(result,"replyEmail","value")
                    my_dict["SUBJECT_TYPE"] = my_get(result,"subject","type")
                    my_dict["SUBJECT_VALUE"] = my_get(result,"subject","value")
                    my_dict["OPERATIONAL"] = my_get(result,"operational",'')
                    my_dict["PUBLISH_TO_MSI"] = my_get(result,"publishToMSI",'')
                    my_dict["TEMPLATE"] = my_get(result,"template",'')
                    my_dict["TEXT_ONLY"] = my_get(result,"textOnly",'')
                    my_dict["URL"] = my_get(result,"url",'')
                    my_dict["WEBVIEW"] = my_get(result,"webView",'')
                    my_dict["CREATED_AT"] = my_get(result,"createdAt",'')
                    my_dict["UPDATED_AT"] = my_get(result,"updatedAt",'')
                    my_dict["WORKSPACE"] = my_get(result,"workspace",'')
                    my_dict_list.append(my_dict)
                                            
    csv_columns = ["REQUEST_ID","SUCCESS","RESULT_ID","NAME","DESCRIPTION","STATUS","FOLDER_TYPE","FOLDER_ID","FOLDER_NAME","FROM_EMAIL_TYPE","FROM_EMAIL_VALUE","FROM_NAME_TYPE","FROM_NAME_VALUE","REPLY_EMAIL_TYPE","REPLY_EMAIL_VALUE","SUBJECT_TYPE","SUBJECT_VALUE","OPERATIONAL","PUBLISH_TO_MSI","TEMPLATE","TEXT_ONLY","URL","WEBVIEW","CREATED_AT","UPDATED_AT","WORKSPACE"]
    with open(exp_path,'wb') as csvfile:
                   xz = csv.DictWriter(csvfile,fieldnames=csv_columns)
                   headers = {}
                   for n in xz.fieldnames:
                       headers[n] = n
                   xz.writerow(headers)
                   for data in my_dict_list:
                       xz.writerow(data)
except Exception as exp:
    log_exception(exp)
    print("Please check the logs. JSON to CSV conversion failed for Emails: ", exp)
