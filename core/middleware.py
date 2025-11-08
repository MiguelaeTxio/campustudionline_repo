class HtmxMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        request.htmx = request.headers.get('Hx-Request') == 'true'
        response = self.get_response(request)
        return response
