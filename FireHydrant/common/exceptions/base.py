from django.http import HttpResponse
import json

class FireHydrantExceptBase(BaseException):


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
                "error": self.key
            }),
            status=500,
            content_type='application/json'
        )
