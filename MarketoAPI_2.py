import json
import csv
import os
import codecs
import sys
import math
reload(sys)
sys.setdefaultencoding('utf8')

file_dir = os.path.normpath('/home/ppande/jobs/marketo/staging/')
exp_dir = os.path.normpath('/home/ppande/jobs/marketo/CSV/')
exp_file_name = 'web_forms.csv'
exp_path = os.path.join(exp_dir, exp_file_name)

my_dict_list =[]
try:
    for f in os.listdir(file_dir):
        if f.endswith('.json') and f.startswith('web_forms_'):
            file_path = os.path.join(file_dir, f)
            data = open(file_path, 'r')
            for line in data:
                my_dict = {}
                parsed_data = json.loads(line)
                my_dict["REQUEST_ID"] = parsed_data["requestId"]
                my_dict["SUCCESS"] = parsed_data["success"]
                for result in parsed_data["result"]:
                    my_dict["RESULT_ID"] = result["id"]
                    my_dict["NAME"] = result["name"]
                    my_dict["DESCRIPTION"] = result["description"]
                    my_dict["FOLDER_ID"] = result["folder"]["value"]
                    my_dict["FOLDER_TYPE"] = result["folder"]["type"]
                    my_dict["FOLDER_NAME"] = result["folder"]["folderName"]
                    my_dict["BUTTON_LABEL"] = result["buttonLabel"]
                    my_dict["BUTTON_LOCATION"] = result["buttonLocation"]
                    my_dict["FONT_FAMILY"] = result["fontFamily"]
                    my_dict["FONT_SIZE"] = result["fontSize"]
                    my_dict["KNOWN_VISITOR_TEMPLATE"] = result["knownVisitor"]["template"]
                    my_dict["KNOWN_VISITOR_TYPE"] = result["knownVisitor"]["type"]
                    my_dict["LABEL_POSITION"] = result["labelPosition"]
                    my_dict["LANGUAGE"] = result["language"]
                    my_dict["PROGRESSIVE_PROFILING"] = result["progressiveProfiling"]
                    my_dict["STATUS"] = result["status"]
                    my_dict["THANK_YOU_LIST"] = result["thankYouList"]
                    my_dict["THEME"] = result["theme"]
                    my_dict["WAITING_LABEL"] = result["waitingLabel"]
                    my_dict["URL"] = result["url"]
                    my_dict["CREATED_AT"] = result["createdAt"]
                    my_dict["UPDATED_AT"] = result["updatedAt"]
                    my_dict_list.append(my_dict)

                
                
    csv_columns = ["REQUEST_ID","SUCCESS","RESULT_ID","NAME","DESCRIPTION","FOLDER_ID","FOLDER_TYPE","FOLDER_NAME","BUTTON_LABEL","BUTTON_LOCATION","FONT_FAMILY","FONT_SIZE","KNOWN_VISITOR_TEMPLATE","KNOWN_VISITOR_TYPE","LABEL_POSITION","LANGUAGE","PROGRESSIVE_PROFILING","STATUS","THANK_YOU_LIST","THEME","WAITING_LABEL","URL","CREATED_AT","UPDATED_AT"]
    with open(exp_path,'wb') as csvfile:
                   xz = csv.DictWriter(csvfile,fieldnames=csv_columns)
                   headers = {}
                   for n in xz.fieldnames:
                       headers[n] = n
                   xz.writerow(headers)
                   for data in my_dict_list:
                       xz.writerow(data)
except Exception as exception:
    print('Please check the logs. JSON to CSV conversion failed for Web Forms: ', exception)
