import json
import logging
from functools import update_wrapper

from django.http import HttpResponse, HttpResponseNotAllowed
from django.utils.decorators import classonlymethod

from common.utils.helper.result import SuccessResult
from common.exceptions.base import FireHydrantExceptBase
from common.core.auth.authModel import FireHydrantAuthAuthorization
from django.views.generic import View
from ..auth.clientModel import FireHydrantClientAuthorization

logger = logging.getLogger('django.request')


class FireHydrantViewBase(View):
    """
    hoho扩展view
    """
    def __init__(self, request, **kwargs):
        super(FireHydrantViewBase, self).__init__(**kwargs)
        self.request = request
        self.__setcookies = []

    @classonlymethod
    def as_view(cls, **initkwargs):
        """
        主要响应点
        :param initkwargs:
        :return:
        """
        for key in initkwargs:
            if key in cls.http_method_names:
                raise TypeError("You tried to pass in the %s method name as association "
                                "keyword argument to %s(). Don't do that."
                                % (key, cls.__name__))
            if key == "method":
                continue
            # 检查路由参数正常与否
            if not hasattr(cls, key):
                raise TypeError("%s() received an invalid keyword %r. as_view "
                                "only accepts arguments that are already "
                                "attributes of the class." % (cls.__name__, key))

        def view(request, *args, **kwargs):
            self = cls(request, **initkwargs)
            if hasattr(self, 'get') and not hasattr(self, 'head'):
                self.head = self.get
            self.args = args
            self.kwargs = kwargs
            self.http_method_names = list(map(lambda x: x.lower(), initkwargs.get('method', self.http_method_names)))
            # 注册json信息
            request.JSON = self.__json_parser(request)
            return self.dispatch(request, *args, **kwargs)

        view.view_class = cls
        view.view_initkwargs = initkwargs

        # take name and docstring from class
        update_wrapper(view, cls, updated=())

        # and possible attributes set by decorators
        # like csrf_exempt from dispatch
        update_wrapper(view, cls.dispatch, assigned=())
        return view

    def dispatch(self, request, *args, **kwargs):
        """
        调度响应
        :param request:
        :param args:
        :param kwargs:
        :return:
        """
        if request.method.lower() in self.http_method_names:
            handler = getattr(self, request.method.lower(), self.http_method_not_allowed)
        else:
            handler = self.http_method_not_allowed

        try:
            a = self.http_method_names
            result = handler(request, *args, **kwargs)
        except FireHydrantExceptBase as ew:
            return ew.render(request)

        if isinstance(result, SuccessResult):
            response = HttpResponse(
                status=200,
                content=result.dumps(),
                content_type='application/json'
            )

        elif isinstance(result, dict) or \
                isinstance(result, list) or \
                isinstance(result, set) or \
                isinstance(result, tuple):
            response = HttpResponse(
                status=200,
                content=json.dumps(result),
                content_type='application/json'
            )
        elif isinstance(result, HttpResponse):
            response = result
        else:
            response = HttpResponse(
                status=200,
                content=result,
                content_type='text/plain' if isinstance(result, str) else 'application/octet-stream'
            )

        # 检查Authorization是否有需要写入Cookie的操作
        if len(self.__setcookies) > 0:
            for c in self.__setcookies:
                response.set_cookie(**c)
        # 允许跨域
        response["Access-Control-Allow-Origin"] = "http://localhost:8080, http://localhost:8000"
        response["Access-Control-Allow-Methods"] = "POST, GET, OPTIONS, PUT, DELETE"
        response["Access-Control-Max-Age"] = "1000"
        response["Access-Control-Allow-Headers"] = "*"

        return response

    def http_method_not_allowed(self, request, *args, **kwargs):
        logger.warning(
            'Method Not Allowed (%s): %s', request.method, request.path,
            extra={'status_code': 405, 'request': request}
        )
        return HttpResponseNotAllowed(self._allowed_methods())

    def options(self, request, *args, **kwargs):
        response = HttpResponse()
        response['Allow'] = ', '.join(self._allowed_methods())
        response['Content-Length'] = '0'
        return response

    def _allowed_methods(self):
        return [m.upper() for m in self.http_method_names if hasattr(self, m)]

    def __json_parser(self, request):
        if 'application/json' in request.META.get('CONTENT_TYPE', ''):
            try:
                info = json.loads(request.body.decode('utf-8'))
            except:
                info = {}
            return info
        else:
            return {}

    def set_cookie(self, key, value='', max_age=None, expires=None, path='/', domain=None, secure=False,
                   httponly=False):
        """
        替代的set_cookie方法，自动实现缓存

        :param key: Cookie Key
        :param value: Cookie Value
        :param max_age: 过期时间，单位秒
            should be association number of seconds, or None (default) if the cookie should last only
            as long as the client’s browser session. If expires is not specified, it will be calculated.
        :param expires: 过期日期
            should either be association string in the format "Wdy, DD-Mon-YY HH:MM:SS GMT" or association datetime.datetime object in UTC.
            If expires is association datetime object,the max_age will be calculated.
        :param path: 路径
        :param domain: 域名
            Use domain if you want to set association cross-domain cookie. For example, domain="example.com" will set association cookie
            that is readable by the domains www.example.com, blog.example.com, etc. Otherwise, association cookie will only be
            readable by the domain that set it.
        :param secure: True表示cookie只能通过SSL协议的https服务器来传递。
        :param httponly: True表示只在URL请求的时候才发送，Ajax等不发送此Cookie

        :return:
        """
        self.__setcookies.append({
            'key': key,
            'value': value,
            'max_age': max_age,
            'expires': expires,
            'path': path,
            'domain': domain,
            'secure': secure,
            'httponly': httponly,
        })



class FireHydrantView(FireHydrantViewBase):

    def __init__(self, request, **kwargs):
        super(FireHydrantView, self).__init__(request, **kwargs)

        if self.request.META.get('HTTP_FIRE_AUTH_MODEL') == "client":
            # 客户端登陆
            self.auth = FireHydrantClientAuthorization(request, self)
        # 浏览器登陆
        else:
            self.auth = FireHydrantAuthAuthorization(request, self)

