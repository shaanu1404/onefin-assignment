class RequestCounterMiddleware(object):

    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        request.session['REQUEST_COUNT'] = request.session.get(
            'REQUEST_COUNT', 0) + 1
        return self.get_response(request)
