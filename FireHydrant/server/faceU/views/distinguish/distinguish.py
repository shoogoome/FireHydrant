# -*- coding: utf-8 -*-
# coding: utf-8


from common.core.auth.check_login import check_login
from common.core.http.facec import FireHydrantFacecView
from common.grpc.facec_grpc_client import FireHydrantFacecRecognitionClient
from common.utils.helper.params import ParamsParser
from common.utils.helper.result import SuccessResult
from ...logic.distinguish import FaceUDistinguishLogic
from ...logic.groups import FaceUGroupsLogic


class FaceUDistinguishView(FireHydrantFacecView):

    @check_login
    def post(self, request):
        """
        上传图片识别存在
        :param request:
        :return:
        """
        params = ParamsParser(request.GET)
        gid = params.int('gid', desc='分组id')
        file = request.FILES.get('file')
        # 全局或者独立分组
        logic = FaceUGroupsLogic(self.auth, gid)
        d_logic = FaceUDistinguishLogic(self.auth, logic.group if gid else '')
        client = FireHydrantFacecRecognitionClient()

        uuids = client.recognition(file.read(), d_logic.to_face_uuid())
        return SuccessResult(result=d_logic.from_face_uuid(uuids))


