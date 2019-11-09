# -*- coding: utf-8 -*-
# coding: utf-8


from django.db import transaction

from common.core.auth.check_login import check_login
from common.core.http.facec import FireHydrantFacecView
from common.utils.helper.params import ParamsParser
from common.utils.helper.result import SuccessResult
from server.faceU.models import FaceUAccount
from common.enum.account.role import AccountRoleEnum
import requests
import json
from common.exceptions.account.info import AccountInfoExcept


class FaceUDistinguishView(FireHydrantFacecView):

    @check_login
    def post(self, request, aid, gid):
        """
        上传图片识别存在
        :param request:
        :param aid:
        :param gid:
        :return:
        """
        ...

