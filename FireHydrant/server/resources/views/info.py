# -*- coding: utf-8 -*-
# coding: utf-8

from common.core.http.view import FireHydrantView
from common.utils.helper.params import ParamsParser
from common.utils.helper.result import SuccessResult
from common.core.auth.check_login import check_login
from ..logic.info import ResourceLogic


class ResourcesInfoView(FireHydrantView):
    is_upload = False

    @check_login
    def get(self, request, mid):
        """
        获取令牌
        :param request:
        :param mid:
        :return:
        """
        logic = ResourceLogic(self.auth, mid)

        if self.is_upload:
            return SuccessResult(token=logic.client.get_upload_token(logic.meta.hash))
        return SuccessResult(token=logic.client.get_download_token(logic.meta.hash))
