from ..models import PracticeClassroom
from .school import SchoolLogic
from common.exceptions.practice.classroom.info import PracticeClassroomInfoExcept
from common.utils.helper.m_t_d import model_to_dict

class ClassroomLogic(SchoolLogic):

    NORMAL_FIELDS = [
        'school', 'school__id', 'school__name',
        'size', 'name', 'create_time', 'update_time'
    ]

    def __init__(self, auth, sid, cid=''):
        """
        INIT
        :param auth:
        :param sid:
        :param cid:
        """
        super(ClassroomLogic, self).__init__(auth, sid)

        if isinstance(cid, PracticeClassroom):
            self.classroom = cid
        else:
            self.classroom = self.get_classroom_model(cid)

    def get_classroom_model(self, cid):
        """
        获取教室model
        :param cid:
        :return:
        """
        if not cid:
            return None

        classroom = PracticeClassroom.objects.get_once(cid)
        if not classroom or classroom.school != self.school:
            raise PracticeClassroomInfoExcept.classroom_is_not_exists()
        return classroom

    def get_classroom_info(self):
        """
        获取教室信息
        :return:
        """
        if not self.classroom:
            return {}
        return model_to_dict(self.school, self.NORMAL_FIELDS)

