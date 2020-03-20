from marketo_authentication import MarketoAuthentication

class MarketoAuthenticationSingleton:
   '''Singleton pattern for the marketo auth token so that only one is in use at a time
   and unneccessary authentication calls are not made.
   '''
   class __MarketoAuthenticationSingleton:
      def __init__(self):
         self.marketo_authentication = MarketoAuthentication()

   instance = None
   def __init__(self):
      if not MarketoAuthenticationSingleton.instance:
         MarketoAuthenticationSingleton.instance = MarketoAuthenticationSingleton.__MarketoAuthenticationSingleton()

   def __getattr__(self, access_token):
      auth = getattr(self.instance, 'marketo_authentication')
      if not hasattr(auth, 'access_token'):
         auth.call_api()
      if auth.is_access_token_expired():
         auth.call_api()

      return auth.access_token


