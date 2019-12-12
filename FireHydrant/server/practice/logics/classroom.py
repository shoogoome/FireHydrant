from ..models import PracticeClassroom
from .school import SchoolLogic
from common.exceptions.practice.classroom.info import PracticeClassroomInfoExcept
from common.utils.helper.m_t_d import model_to_dict
from ..models import PracticeClassroomUser

class ClassroomLogic(SchoolLogic):

    NORMAL_FIELDS = [
        'school', 'school__id', 'school__name',
        'size', 'name', 'create_time', 'update_time', 'id'
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
        return model_to_dict(self.classroom, self.NORMAL_FIELDS)

    def get_classroom_user(self):
        """
        获取教室使用情况
        :return:
        """
        if not self.classroom:
            return []

        user = PracticeClassroomUser.objects.select_related(
            'account__account', 'practice__practicearrangement', 'practice__practiceclassroom', 'practice__practicecourse'
        ).filter(
            classroom=self.classroom
        ).values(
            'author', 'author__nickname', 'arrangement', 'arrangement__name',
            'classroom', 'classroom__name', 'create_time', 'update_time', 'id'
            'arrangement__course__id', 'arrangement__course__name'
        )

        data = []
        for i in user:
            i['author'] = {
                'id': i['author'],
                'nickname': i['author__nickname']
            }
            i['arrangement'] = {
                'id': i['arrangement'],
                'name': i['arrangement__name'],
                'course': {
                    'id': i['arrangement__course__id'],
                    'name': i['arrangement__course__name']
                }
            }
            i['classroom'] = {
                'id': i['classroom'],
                'name': i['classroom__name']
            }
            del i['arrangement__name']
            del i['author__nickname']
            del i['classroom__name']
            try:
                data.append(i)
            except:
                pass
        return data


