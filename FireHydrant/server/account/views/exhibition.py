#-*- coding: utf-8 -*-
# coding: utf-8

from common.core.auth.check_login import check_login
from common.core.http.view import FireHydrantView
from common.utils.helper.params import ParamsParser
from ..models import Account
from django.db import transaction
from common.exceptions.account.info import AccountInfoExcept
from common.utils.helper.result import SuccessResult
from common.utils.helper.m_t_d import model_to_dict
from ..logics.info import AccountLogic
from common.constants.length_limitation import *
from common.utils.hash import signatures
from server.account.models import AccountExhibition
from server.resources.logic.info import ResourceLogic
from server.resources.models import ResourcesMeta
from ..logics.exhibition import ExhibitionLogic

class AccountExhibitionView(FireHydrantView):

    @check_login
    def post(self, request):
        """
        创建个人作品展示
        :param request:
        :return:
        """
        params = ParamsParser(request.JSON)

        # 创建作品资源
        if params.has('resources'):
            meta_list, resource_token = self.upload_resource(params.list('resources', desc='资源信息'))

        with transaction.atomic():
            exhibition = AccountExhibition.objects.create(
                account=self.auth.get_account(),
                title=params.str('title', desc='标题'),
                content=params.str('content', desc='正文'),
                show=params.bool('show', desc='是否展示', default=True, require=False)
            )
        info = {
            'id': exhibition.id
        }
        # 关联资源元数据
        if params.has('resources'):
            exhibition.resource.set(meta_list)
            info['token'] = resource_token

        return SuccessResult(info)

    @check_login
    def get(self, request, eid):
        """
        查看用户作品展示详情
        :param request:
        :param eid:
        :return:
        """
        logic = ExhibitionLogic(self.auth, eid)

        return SuccessResult(logic.get_exhibition_info())

    @check_login
    def put(self, request, eid):
        """
        修改用户作品信息
        :param request:
        :param eid:
        :return:
        """
        params = ParamsParser(request.JSON)

        logic = ExhibitionLogic(self.auth, eid)
        exhibition = logic.exhibition

        with params.diff(exhibition):
            exhibition.title = params.str('title', desc='标题')
            exhibition.content = params.str('content', desc='正文')
            exhibition.show = params.bool('show', desc='是否展示')

        info = {
            'id': eid
        }
        if params.has('resource'):
            meta_list, resource_token = self.upload_resource(params.list('resource', desc='资源文件信息'))
            exhibition.resource.set(meta_list)
            info['token'] = resource_token

        return SuccessResult(info)

    @check_login
    def delete(self, request, eid):
        """
        删除作品
        :param request:
        :param eid:
        :return:
        """
        logic = ExhibitionLogic(self.auth, eid)

        logic.exhibition.delete()
        return SuccessResult(id=eid)

    @check_login
    def upload_resource(self, resources: list):
        """
        上传作品资源文件
        :return:
        """
        # 创建资源元数据记录
        re_logic = ResourceLogic(self.auth)
        resource_token = dict()
        meta_list = list()
        for resource in resources:
            # 存在即秒传
            re_params = ParamsParser(resource)
            if ResourcesMeta.objects.filter(hash=re_params.str('hash', desc='文件hash')).exists():
                continue
            try:

                with transaction.atomic():
                    meta = ResourcesMeta.objects.create(
                        name=re_params.str('name', desc='文件名称'),
                        size=re_params.float('size', desc='文件大小'),
                        hash=re_params.str('hash', desc='文件hash'),
                    )
                meta_list.append(meta)
                # 填入上传token信息
                re_logic.meta = meta
                resource_token[re_params.str('hash', desc='文件hash')] = re_logic.get_upload_token()
            except:
                pass

        return meta_list, resource_token

