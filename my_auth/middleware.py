from django.conf import settings


class UnauthorizedRequestsMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        try:
            f = open(settings.UNAUTHORIZED_REQUEST_COUNT_FILE, 'r')
            unauthorized_requests = int(f.readline())
            f.close()
        except IOError:
            unauthorized_requests = 0

        if not request.user.is_authenticated:
            unauthorized_requests += 1
            with open(settings.UNAUTHORIZED_REQUEST_COUNT_FILE, 'w') as f:
                f.write(str(unauthorized_requests))

        response = self.get_response(request)
        return response
