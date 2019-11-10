# -*- coding: utf-8 -*-
# coding: utf-8


from common.core.auth.check_login import check_login
from common.core.http.facec import FireHydrantFacecView
from common.enum.account.sex import AccountSexEnum
from common.exceptions.faceU.group.manage import FaceUGroupManageExcept
from common.utils.helper.params import ParamsParser
from common.utils.helper.result import SuccessResult
from server.faceU.models import FaceUFacialMakeupMapping, FaceUFacialMakeup
from ...logic.groups import FaceUGroupsLogic


def save_mapping(face_uuid, name, code, group):
    makeup, _ = FaceUFacialMakeup.objects.get_or_create(face_uuid=face_uuid, defaults={
        "name": name,
        "id_code": "",
        "sex": int(AccountSexEnum.UNKNOW)
    })
    mapping = FaceUFacialMakeupMapping.objects.create(
        face=makeup,
        group=group,
        name=name,
        code=code,
    )
    return mapping


class FaceUGroupManageView(FireHydrantFacecView):

    @check_login
    def get(self, request, gid):
        """
        获取分组成员
        :param request:
        :param gid:
        :return:
        """
        logic = FaceUGroupsLogic(self.auth, gid)
        return SuccessResult(logic.get_group_members_info())

    @check_login
    def post(self, request, gid):
        """
        单独新增成员信息
        :param request:
        :param gid:
        :return:
        """
        params = ParamsParser(request.JSON)
        logic = FaceUGroupsLogic(self.auth, gid)

        name = params.str('name', desc='名称')
        code = params.str('code', desc='自定义标识符', require=False, default='')
        face = params.str('face', desc='脸谱图')

        # 图片数据
        face_uuid = FaceUGroupsLogic.save_face(face)
        mapping = save_mapping(face_uuid, name, code, logic.group)
        return SuccessResult(id=mapping.id)

    @check_login
    def put(self, request, gid, mid):
        """
        修改成员信息
        :param request:
        :param gid:
        :param mid:
        :return:
        """
        params = ParamsParser(request.JSON)
        mapping = FaceUFacialMakeupMapping.objects.filter(group_id=gid, id=mid)
        if not mapping.exists():
            raise FaceUGroupManageExcept.member_is_not_exists()

        mapping = mapping[0]
        with params.diff(mapping):
            mapping.name = params.str('name', desc='姓名')
            mapping.code = params.str('code', desc='标识')
        if params.has('face'):
            face_uuid = FaceUGroupsLogic.save_face(params.str('face', desc='脸谱'))
            makeup, _ = FaceUFacialMakeup.objects.get_or_create(face_uuid=face_uuid, defaults={
                "name": mapping.name,
                "id_code": "",
                "sex": int(AccountSexEnum.UNKNOW)
            })
            mapping.face = makeup
        mapping.save()

        return SuccessResult(id=mid)

    @check_login
    def delete(self, request, gid):
        """
        移除成员
        :param request:
        :param gid:
        :return:
        """
        params = ParamsParser(request.JSON)
        logic = FaceUGroupsLogic(self.auth, gid)
        ids = params.list('ids', desc='成员id列表')

        status = {}
        mappings = FaceUFacialMakeupMapping.objects.get_many(ids)
        for mapping in mappings:
            _id = mapping.id
            try:
                if mapping.group_id == logic.group.id:
                    mapping.delete()
                    status[_id] = 1
                else:
                    status[_id] = 0
            except:
                status[_id] = 0

        return SuccessResult(status=status)


class FaceUGroupManageMany(FireHydrantFacecView):

    @check_login
    def post(self, request, gid):
        """
        批量上传脸谱
        :param request:
        :param gid:
        :return:
        """
        logic = FaceUGroupsLogic(self.auth, gid)

        status = {}
        files = request.FILES.getlist('faces')
        for file in files:
            file_name = file.name.split('@')
            name = ''.join(file_name[1:])
            code = file_name[0]
            try:
                # 上传脸谱
                face_uuid = FaceUGroupsLogic.save_face(file.read())
                _ = save_mapping(face_uuid, name, code, logic.group)
                status[code] = 1
            except:
                status[code] = 0

        return SuccessResult(status=status)
