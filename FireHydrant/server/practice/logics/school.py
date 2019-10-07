from ..models import PracticeSchool
from common.exceptions.practice.school.info import PracticeSchoolInfoExcept
from common.utils.helper.m_t_d import model_to_dict

class SchoolLogic(object):

    NORMAL_FIELDS = [
        'name', 'description', 'create_time', 'update_time'
    ]

    def __init__(self, auth, sid):
        """
        INIT
        :param auth:
        :param sid:
        """
        self.auth = auth

        if isinstance(sid, PracticeSchool):
            self.school = sid
        else:
            self.school = self.get_school_model(sid)

    def get_school_model(self, sid):
        """
        获取学校model
        :param sid:
        :return:
        """
        if not sid:
            return None

        school = PracticeSchool.objects.get_once(pk=sid)
        if not school:
            raise PracticeSchoolInfoExcept.school_is_not_exists()
        return school

    def get_school_info(self):
        """
        获取学校信息
        :return:
        """
        if not self.school:
            return {}

        return model_to_dict(self.school, self.NORMAL_FIELDS)

