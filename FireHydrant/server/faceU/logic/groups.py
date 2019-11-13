import uuid

from common.exceptions.faceU.group.info import FaceUGroupInfoExcept
from common.utils.hash.signatures import session_signature
from common.utils.helper.durl import DataUrlParser
from common.utils.helper.m_t_d import model_to_dict
from ..models import FaceUGroups, FaceUFacialMakeupMapping
from common.grpc.facec_grpc_client import FireHydrantFacecRecognitionClient
from django.db import connection

class FaceUGroupsLogic(object):
    NORMAL_FIELDS = [
        'author', 'author__id', 'author__nickname', 'title',
        'description', 'create_time', 'update_time', 'id'
    ]

    MEMBER_FIELDS = [
        'name', 'code', 'create_time', 'update_time', 'id'
    ]

    def __init__(self, auth, gid=''):
        """
        INIT
        :param auth:
        :param gid:
        """
        self.auth = auth

        if isinstance(gid, FaceUGroups):
            self.group = gid
        else:
            self.group = self.get_group_model(gid)

    def get_group_model(self, gid):
        """
        获取分组model
        :param gid:
        :return:
        """
        if not gid:
            return None

        group = FaceUGroups.objects.get_once(pk=gid)
        if not group or group.author_id != self.auth.get_account().id:
            raise FaceUGroupInfoExcept.group_is_not_exists()

        return group

    def get_group_info(self):
        """
        获取分组信息
        :return:
        """
        if not self.group:
            return {}

        return model_to_dict(self.group, self.NORMAL_FIELDS)

    def get_group_members_info(self):
        """
        获取分组成员信息
        :return:
        """
        if not self.group:
            return []

        data = []
        mappings = FaceUFacialMakeupMapping.objects.filter(group=self.group)

        for mapping in mappings:
            try:
                data.append(model_to_dict(mapping, self.MEMBER_FIELDS))
            except:
                pass
        return data

    @staticmethod
    def save_face(face):
        """
        保存脸
        :param face:
        :return:
        """
        if isinstance(face, str):
            face_image = DataUrlParser(face).data
        else:
            face_image = face

        client = FireHydrantFacecRecognitionClient()
        # 存在则直接return
        face_uuid = client.is_exists(face_image)
        if face_uuid:
            return face_uuid

        face_uuid = session_signature(str(uuid.uuid1()))
        client.upload_face(face_image, face_uuid)

        return face_uuid