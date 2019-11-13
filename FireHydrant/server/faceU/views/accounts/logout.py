# -*- coding: utf-8 -*-
# coding: utf-8


import json

import requests

from common.core.http.facec import FireHydrantFacecView
from common.enum.account.role import AccountRoleEnum
from common.exceptions.account.info import AccountInfoExcept
from common.utils.helper.params import ParamsParser
from common.utils.helper.result import SuccessResult
from server.faceU.models import FaceUAccount


class FaceUAccountLogout(FireHydrantFacecView):

    def get(self, request):
        """
        登出
        :param request:
        :return:
        """
        self.auth.set_account(None)
        self.auth.set_session()

        return SuccessResult(status="ok")