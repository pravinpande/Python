from marketo_get_web_forms import MarketoGetWebForms
from utilities import write_response, move_to_hdfs, archive_files, format_etl_process_date
from sys import exit
import datetime
from hdfs import execute_hive_from_file
from iterable_load import run_iterable

# main program for retrieving Marketo web forms 

api_object_type = 'web_forms'

local_file_details = { 
  'results_prefix' : api_object_type, 
  'no_results_prefix' : 'no_results_'+api_object_type, 
  'path' : './staging/'
}



def get_next_iteration( get_object = None):
  '''logic setting up the next API call after a previous call. If no call was this will provide an object for the first call '''
  if get_object is not None:
    paging_offset = get_object.next_paging_offset
  else:
    paging_offset = 0

  print("Paging offset: " + str(paging_offset))
  next_get_object = MarketoGetWebForms(paging_offset)

  return next_get_object



total_result_count = run_iterable(local_file_details, get_next_iteration)

print("web form load to local file system complete")
print("total result count " + str(total_result_count))

if total_result_count > 0:
  print("Data Retrived Sucessfully")
else:
  exit("no results retrived")

'''
hdfs_path = '/data/staging/marketo/marketo_'+api_object_type+'/'

hdfs_move_success = move_to_hdfs(local_file_details["results_prefix"], local_file_details["path"], hdfs_path)

if hdfs_move_success:
  print("successfully moved files to hdfs")
else:
  exit("error moving files to hdfs")
  
  #load data from external table to managed table with results exploded
extract_end_date = datetime.datetime.today()
formatted_extract_end_date = format_etl_process_date(extract_end_date)
load_table_success = execute_hive_from_file('load_stg_get_'+api_object_type+'_exploded.hql', ['etl_process_dt=\'' + formatted_extract_end_date + '\''])
if load_table_success:
  print("successfully loaded exploded table")
else:
  exit("error loading exploded table")

#move data from external staging to persistent external staging
archive_hdfs_path = '/data/staging/marketo/marketo_'+api_object_type+'_persistent/'
archive_folder_files_success = archive_files(local_file_details["results_prefix"], hdfs_path, archive_hdfs_path)
if archive_folder_files_success:
  print("successfully archived files to perstistent storage")
else:
  exit("error archiving to persistent storage")
'''
