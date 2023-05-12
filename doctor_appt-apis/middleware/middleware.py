from werkzeug.wrappers import Request, Response, ResponseStream

class middleware():
    '''
    Simple WSGI middleware
    '''
    # TODO finish this
    def __init__(self, app):
        self.app = app
        self.userName = None
        self.password = None

    def __call__(self, environ, start_response):
        request = Request(environ)
        userName = request.authorization['username']
        password = request.authorization['password']
        
        # verify the username and password from some database or env config variable
        # TODO: Fetch UserName and Password from dB
        # self.userName,self.password = fetch_user_data_from_db()
        if userName == self.userName and password == self.password:
            environ['user'] = { 'name': 'xyz' }
            return self.app(environ, start_response)

        res = Response(u'Authorization failed', mimetype= 'text/plain', status=401)
        return res(environ, start_response)