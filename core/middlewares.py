import logging

logger = logging.getLogger(__name__)


class ExceptionLoggingMiddleware:

    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        return self.get_response(request)

    @staticmethod
    def process_exception(request, exception):
        logger.exception(exception)
