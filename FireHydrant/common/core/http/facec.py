import logging

from common.core.auth.facec import FireHydrantFacecAuthAuthorization
from .view import FireHydrantViewBase
from ..auth.clientModel import FireHydrantClientAuthorization

logger = logging.getLogger('django.request')


class FireHydrantFacecView(FireHydrantViewBase):

    def __init__(self, request, **kwargs):
        super(FireHydrantFacecView, self).__init__(request, **kwargs)

        # 客户端模式
        if self.request.META.get('HTTP_FIRE_AUTH_MODEL') == "client":
            self.auth = FireHydrantClientAuthorization(request, self)
        # 浏览器登陆
        else:
            self.auth = FireHydrantFacecAuthAuthorization(request, self)
