from ..models import FaceUDistinguishRecord
from common.exceptions.faceU.record.info import FaceURecordInfoExcept
from common.utils.helper.m_t_d import model_to_dict
from common.core.dao.storage.local import FireHydrantLocalStorage
from common.entity.faceu.record import FaceURecordEntity

class FaceURecordLogic(object):

    NORMAL_FIELDS = [
        'author', 'author__id', 'author__nickname',
        'group', 'group__id', 'group__title',
        'result', 'create_time', 'update_time'
    ]

    def __init__(self, auth, rid=''):
        """
        INIT
        :param auth:
        :param rid:
        """
        self.auth = auth

        if isinstance(rid, FaceUDistinguishRecord):
            self.record = rid
        else:
            self.record = self.get_record_model(rid)

    def get_record_model(self, rid):
        """
        获取记录model
        :param rid:
        :return:
        """
        if not rid:
            return None

        record = FaceUDistinguishRecord.objects.get_once(pk=rid)
        if not record:
            raise FaceURecordInfoExcept.record_is_not_exists()

        return record

    def get_record_info(self):
        """
        获取记录信息
        :return:
        """
        if not self.record:
            return {}

        token = []
        info = model_to_dict(self.record, self.NORMAL_FIELDS)
        entity = FaceURecordEntity()
        entity.update(info['result'])

        for i in entity.storage:
            token.append(FireHydrantLocalStorage.generate_token(i))
        entity.storage = token
        info['result'] = entity.dump()
        return info


