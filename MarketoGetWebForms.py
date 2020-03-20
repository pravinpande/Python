from marketo_rest_api import MarketoRestApi

class MarketoGetWebForms(MarketoRestApi):
  '''call the marketo REST API for get web forms

  paging is with page offest numbers. 

  warnings and result counts are important, because there is no ending
  page number. When a warning is received the error message will indicate
  that no assets are found. Also the results array will have zero elements.
  
  http://developers.marketo.com/documentation/marketo-rest-apis-web-page-objects/get-forms/
  '''

  def __init__(self, paging_offset):
    super(MarketoGetWebForms, self).__init__()

    self.set_api_configuration('marketo_configurations/rest_api.cfg')
    self.set_end_point_configuration('marketo_configurations/get_web_forms.cfg')

    self.current_paging_offset = paging_offset
    self.next_paging_offset = None

    self.request_id = None
    self.success = None
    self.warnings = None
    self.errors = None
    self.result = None
    self.result_count = None


  def call_api(self):
    ''' paging offset provided in the call changes as we iterate
    '''
    self.add_param('offset', self.current_paging_offset)

    super(MarketoGetWebForms, self).call_api() 
    self.request_id = self.get_response_value('requestId')

    self.success = self.get_response_value('success')

    self.warnings = self.get_response_value('warnings')
    self.log_warnings()

    self.errors = self.get_response_value('errors')
    self.log_errors()

    self.result = self.get_response_value('result')
    if self.result is not None:
      self.result_count = len(self.result)
    else:
      self.result_count = 0

    self.next_paging_offset = self.current_paging_offset + self.result_count


  def log_warnings(self):
    if self.warnings is not None:
      for warning in self.warnings:
        print('Warning: ' + warning)


  def log_errors(self):
    '''we know little about error messages returned.
    for now, we just print them.
    '''
    if self.errors is not None:
      for error in self.errors:
        print('Error: ' + str(error))


  def more_results(self):
    '''Determine if there are more results to page through
    '''
    more_results = True

    if self.warnings is not None:
      for warning in self.warnings:
        if warning == 'No assets found for the given search criteria.':
          more_results = False

    if self.result_count == 0:
      more_results = False

    return more_results

