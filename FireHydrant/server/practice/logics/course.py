from ..models import PracticeCourse
from .school import SchoolLogic
from common.exceptions.practice.course.info import PracticeCourseInfoExcept
from common.utils.helper.m_t_d import model_to_dict

class CourseLogic(SchoolLogic):

    NORMAL_FIELDS = [
        'school', 'school__id', 'school__name',
        'author', 'author__id', 'author__name',
        'tag', 'name', 'description', 'start_time',
        'end_time', 'create_time', 'update_time'
    ]

    def __init__(self, auth, sid, cid=''):

        super(CourseLogic, self).__init__(auth, sid)

        if isinstance(cid, PracticeCourse):
            self.course = cid
        else:
            self.course = self.get_course_model(cid)

    def get_course_model(self, cid):
        """
        获取课程model
        :param cid:
        :return:
        """
        if not cid:
            return None

        course = PracticeCourse.objects.get_once(cid)
        if not course or course.school != self.school:
            raise PracticeCourseInfoExcept.course_is_not_exists()

        return course

    def get_course_info(self):
        """
        获取课程信息
        :return:
        """
        if not self.course:
            return {}
        return model_to_dict(self.course, self.NORMAL_FIELDS)
