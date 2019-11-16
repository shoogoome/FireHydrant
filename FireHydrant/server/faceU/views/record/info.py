# -*- coding: utf-8 -*-
# coding: utf-8


from common.core.auth.check_login import check_login
from common.core.http.facec import FireHydrantFacecView
from common.grpc.facec_grpc_client import FireHydrantFacecRecognitionClient
from common.utils.helper.params import ParamsParser
from common.utils.helper.result import SuccessResult
from server.faceU.logic.distinguish import FaceUDistinguishLogic
from server.faceU.logic.groups import FaceUGroupsLogic
from common.core.dao.storage.local import FireHydrantLocalStorage
from common.utils.hash.signatures import gen_salt
from server.faceU.models import FaceUDistinguishRecord
from server.faceU.logic.record import FaceURecordLogic
from common.entity.faceu.record import FaceURecordEntity

class FaceURecordInfoView(FireHydrantFacecView):

    @check_login
    def get(self, request, rid):
        """
        获取记录信息
        :param request:
        :param rid:
        :return:
        """
        logic = FaceURecordLogic(self.auth, rid)

        return SuccessResult(logic.get_record_info())


