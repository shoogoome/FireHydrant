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


class FaceUAccountLogin(FireHydrantFacecView):

    def post(self, request):
        """
        登陆
        :param request:
        :return:
        """
        params = ParamsParser(request.JSON)
        code = params.str('token', desc='验证ID')
        openid, session = self.get_openid(code)
        client_auth_mode = self.request.META.get('HTTP_FIRE_AUTH_MODEL') == "client"

        accounts = FaceUAccount.objects.filter_cache(temp_access_token=openid)
        if len(accounts) == 0:
            nickname = params.str('nickname', desc='昵称')
            sex = params.int('sex', desc='性别')

            account = FaceUAccount.objects.create(
                nickname=nickname,
                sex=sex,
                temp_access_token=openid,
                role=int(AccountRoleEnum.USER),
                motto="这个人很懒，什么都没有"
            )
            _id = account.id
        else:
            account = accounts[0]
            _id = account.id
        # 更新数据
        self.auth.set_account(account)
        # 载入登陆信息  客户端模式
        if client_auth_mode:
            return SuccessResult({
                "id": _id,
                "token": self.auth.create_token()
            })
        # pc端模式
        self.auth.set_session()
        return SuccessResult(id=_id)

    def get_openid(self, code):
        """
        获取openid
        :return:
        """
        url = "https://api.weixin.qq.com/sns/jscode2session?appid={0}&secret={1}&js_code={2}&grant_type=authorization_code".format(
            "wxefe392b88181200a",
            "3296b8d643b9a6e8603f18dec0df265c",
            code
        )

        response = requests.get(url)
        token = json.loads(response.text)

        if token.get('errcode', 0):
            raise AccountInfoExcept.token_error(token.get('errmsg', '未知错误'))

        return token.get('openid', ''), token.get('session_key', '')


class FireHydrantDevelopLogin(FireHydrantFacecView):

    def post(self, request):
        """
        开发登陆接口
        :param request:
        :return:
        """
        params = ParamsParser(request.JSON)
        token = params.str('token', desc='token')

        accounts = FaceUAccount.objects.filter_cache(temp_access_token=token)

        self.auth.set_account(accounts[0])
        self.auth.set_session()
        return SuccessResult(id=accounts[0].id)
