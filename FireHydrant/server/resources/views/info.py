# -*- coding: utf-8 -*-
# coding: utf-8

from common.core.http.view import FireHydrantView
from common.utils.helper.params import ParamsParser
from common.utils.helper.result import SuccessResult
from common.core.auth.check_login import check_login
from ..logic.info import ResourceLogic
from django.db import transaction
from ..models import ResourcesMeta
from common.constants.mime import MIME_TYPE
from common.exceptions.resources.info import ResourceInfoExcept

class ResourcesInfoView(FireHydrantView):

    @check_login
    def get(self, request):
        """
        获取上传令牌 1-资源已存在 秒传，0-获取上传token
        :param request:
        :return:
        """
        params = ParamsParser(request.GET)

        fhash = params.str('hash', desc='文件hash值')
        meta = ResourcesMeta.objects.filter(hash=fhash)
        # 资源存在，尝试构建资源凭证
        # 成功返回凭证，失败返回上传凭证
        if meta.exists():
            logic = ResourceLogic(self.auth, meta[0])
            ok, v_token = logic.upload_finish(ResourceLogic.get_upload_token(fhash), '')
            if ok:
                return SuccessResult(token=v_token, state=1)

        return SuccessResult(token=ResourceLogic.get_upload_token(fhash), state=0)

    @check_login
    def post(self, request):
        """
        完成上传
        :param request:
        :return:
        """
        params = ParamsParser(request.JSON)

        token = params.str('token', desc='token')
        name = params.str('name', desc='文件名称')
        fhash = params.str('hash', desc='文件hash')
        meta = ResourcesMeta.objects.filter(hash=fhash)
        if meta.exists():
            meta = meta[0]
        else:
            with transaction.atomic():
                meta = ResourcesMeta.objects.create(
                    name=name,
                    mime=MIME_TYPE.get(name.strip('.')[-1], 'text/plain'),
                    size=params.int('size', desc='文件大小'),
                    hash=fhash
                )
        logic = ResourceLogic(self.auth, meta)
        ok, v_token = logic.upload_finish(token, name)
        if not ok:
            raise ResourceInfoExcept.upload_fail()

        return SuccessResult(token=v_token)


