# -*- coding: utf-8 -*-
# coding: utf-8

from common.core.http.view import FireHydrantView
from common.utils.helper.params import ParamsParser
from common.utils.helper.result import SuccessResult
from ..logic.client import LiumaClient


class ResourcesInfoView(FireHydrantView):
    is_upload = False

    def get(self, request):
        """
        获取令牌
        :param request:
        :return:
        """
        params = ParamsParser(request.GET)

        client = LiumaClient()
        if self.is_upload:
            return SuccessResult(token=client.get_upload_token(params.str('hash', desc='文件hash')))
        return SuccessResult(token=client.get_download_token(params.str('hash', desc='文件hash')))
