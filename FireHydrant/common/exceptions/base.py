from django.http import HttpResponse
import json

class FireHydrantExceptBase(BaseException):

    MAJOR_HTTP_CODE = 550

    def __init__(self, key=''):
        """
        INIT
        :param key:
        """
        # self.request = request
        self.key = key

    def render(self, request):
        """
        渲染
        :param request:
        :return:
        """
        return HttpResponse(
            content=json.dumps({
                "error": self.key,
                "code": self.MAJOR_HTTP_CODE
            }),
            status=self.MAJOR_HTTP_CODE,
            content_type='application/json'
        )
