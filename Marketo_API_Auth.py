from rest_api_base import RestApiBase
import datetime

class MarketoAuthentication(RestApiBase):
  '''API call to get authentication token.
  Tracks the time that Marketo says the token will expire, so it can be renewed.
  '''

  def __init__(self):
    super(MarketoAuthentication, self).__init__()
    self.set_api_configuration('marketo_configurations/api.cfg')
    self.set_end_point_configuration('marketo_configurations/authentication_end_point.cfg')

  def call_api(self):
    self.execution_start = datetime.datetime.now()
    super(MarketoAuthentication, self).call_api()
#    print(self.get_response_dict())
    self.access_token = self.get_response_dict()['access_token']
#    print("access token " + self.access_token)
    self.expires_in = self.get_response_dict()['expires_in']
    self.expires_at = self.execution_start + datetime.timedelta(seconds=(self.expires_in - 60))
  
  def is_access_token_expired(self):
    return datetime.datetime.now() >= self.expires_at
