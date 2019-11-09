import logging

from common.core.auth.firehydrant import FireHydrantAuthAuthorization
from .view import FireHydrantViewBase
from ..auth.clientModel import FireHydrantClientAuthorization

logger = logging.getLogger('django.request')


class FireHydrantView(FireHydrantViewBase):

    def __init__(self, request, **kwargs):
        super(FireHydrantView, self).__init__(request, **kwargs)

        # 客户端模式
        if self.request.META.get('HTTP_FIRE_AUTH_MODEL') == "client":
            # self.auth = FireHydrantClientAuthorization(request, self)
            ...
        # 浏览器登陆
        else:
            self.auth = FireHydrantAuthAuthorization(request, self)
