from ..models import PracticeTag
from common.exceptions.practice.tag.info import PracticeTagInfoExcept
from common.utils.helper.m_t_d import model_to_dict
class TagLogic(object):

    NORMAL_FIELD = [
        'name', 'parent', 'parent__id', 'parent__name', 'id'
    ]

    def __init__(self, auth, tid):
        """
        INIT
        :param auth:
        :param tid:
        """
        self.auth = auth

        if isinstance(tid, PracticeTag):
            self.tag = tid
        else:
            self.tag = self.get_tag_model(tid)

    def get_tag_model(self, tid):
        """
        获取标签model
        :param tid:
        :return:
        """
        if not tid:
            return None

        tag = PracticeTag.objects.get_once(tid)
        if not tag:
            raise not PracticeTagInfoExcept.tag_is_not_exists()
        return tag

    def get_tag_info(self):
        """
        获取标签信息
        :return:
        """
        if not self.tag:
            return {}
        return model_to_dict(self.tag, self.NORMAL_FIELD)

    @staticmethod
    def is_not_annular(parent: PracticeTag, target_id: int) -> bool:
        """
        判断是否环形
        :param parent:
        :param target_id:
        :return:
        """
        if not parent.parent:
            return True

        if parent.parent_id == target_id:
            return False
        else:
            return TagLogic.is_not_annular(parent.parent, target_id)