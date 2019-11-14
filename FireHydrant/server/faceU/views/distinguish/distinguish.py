# -*- coding: utf-8 -*-
# coding: utf-8


from common.core.auth.check_login import check_login
from common.core.http.facec import FireHydrantFacecView
from common.grpc.facec_grpc_client import FireHydrantFacecRecognitionClient
from common.utils.helper.params import ParamsParser
from common.utils.helper.result import SuccessResult
from ...logic.distinguish import FaceUDistinguishLogic
from ...logic.groups import FaceUGroupsLogic
from common.core.dao.storage.local import FireHydrantLocalStorage
from common.utils.hash.signatures import gen_salt
from ...models import FaceUDistinguishRecord
from common.entity.faceu.record import FaceURecordEntity

class FaceUDistinguishView(FireHydrantFacecView):

    @check_login
    def post(self, request):
        """
        上传图片识别存在
        :param request:
        :return:
        """
        params = ParamsParser(request.GET)
        gid = params.int('gid', desc='分组id', require=False, default=0)
        file = request.FILES.get('file')

        # 全局或者独立分组
        logic = FaceUGroupsLogic(self.auth, gid if gid else '')
        d_logic = FaceUDistinguishLogic(self.auth, gid)

        # 人脸识别
        client = FireHydrantFacecRecognitionClient()
        uuids, image = client.recognition(file.read(), d_logic.to_face_uuid())

        # 结果图存储
        _uid = gen_salt()
        if gid:
            storage = FireHydrantLocalStorage('facec_distinguish')
            vpath = storage.save_file(f"{gid}/{_uid}.jpeg", image, open_type='wb')
        else:
            storage = FireHydrantLocalStorage('facec_distinguish_static')
            vpath = storage.save_file(f"{_uid}.jpeg", image, open_type='wb')

        entity = FaceURecordEntity()
        entity.update({
            'storage': [vpath],
            'record': d_logic.from_face_uuid(uuids)
        })

        record = FaceUDistinguishRecord.objects.create(
            author=self.auth.get_account(),
            result=entity.dumps(),
        )
        if gid:
            record.group_id = gid
        record.save()

        return SuccessResult(id=record.id)


