import sys
from django.http import HttpResponse
from common.exceptions.base import FireHydrantExceptBase
from django.utils.deprecation import MiddlewareMixin
from django.views.debug import technical_500_response

class FireHydrantErrorHandleMiddleware(MiddlewareMixin):

    def process_request(self, request):
        """
        响应处理
        :param request:
        :return:
        """
        pass

    def process_response(self, request, response):
        """
        处理应答部分
        :param request:
        :param response:
        :return:
        """
        return response

    def process_exception(self, request, exception):
        """
        异常处理
        :param request:
        :type request: WSGIRequest|
        :param exception:
        :return:
        """
        path = request.path
        if path[0:1] == '/':
            path = path[1:]
        prefix = path.split('/')[0]
        if prefix in ['server_admin']:
            return technical_500_response(request, *sys.exc_info())

        if isinstance(exception, FireHydrantExceptBase):
            return exception.render(request)
        else:
            if request.GET.get('debug', False) == '1':
                django_debug_resp = technical_500_response(request, *sys.exc_info())
                return django_debug_resp
            else:
                return HttpResponse(
                    content="开启调试",
                    status=500,
                    content_type='application/json',
                )