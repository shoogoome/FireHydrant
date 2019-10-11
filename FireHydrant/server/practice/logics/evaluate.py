from ..models import PracticeEvaluateStudentToTeacher,\
    PracticeEvaluateTeacherToStudent, PracticeEvaluateStudentToCourse, PracticeStudentUser
from .course import CourseLogic
from common.exceptions.practice.evaluate.info import PracticeEvaluateExcept
from common.utils.helper.m_t_d import model_to_dict
from django.db import connection

BASE_FIELDS = [
    'author', 'author__id', 'star', 'message',
    'create_time', 'update_time', 'id'
]

class EvaluateBaseLogic(CourseLogic):

    def __init__(self, auth, sid, cid):
        """
        INTI
        :param auth:
        :param sid:
        :param cid:
        """
        super(EvaluateBaseLogic, self).__init__(auth, sid, cid)
        self.evaluate = None

    def get_evaluate_info(self):
        """
        获取评价信息
        :return:
        """
        if not self.evaluate:
            return {}
        return model_to_dict(self.evaluate, self.NORMAL_FIELDS)

    def get_course_all_students(self, codes=None):
        """
        获取课程全部学生
        :param codes:
        :return:
        """
        if not self.course:
            return []

        # 获取课程所有学生id
        with connection.cursor() as cursor:
            cursor.execute("SELECT arrangement_students.practicestudentuser_id as id "
                           "FROM `practice_practicearrangement` as arrangement, "
                           "`practice_practicestudentuser` as student, "
                           "`practice_practicearrangement_students` as arrangement_students, "
                           "`practice_practicecourse` as course "
                           "WHERE arrangement_students.practicearrangement_id = arrangement.id "
                           "AND arrangement.course_id = course.id "
                           "AND student.id = arrangement_students.practicestudentuser_id "
                           "AND ( 1 = %s or student.code in %s )",
                           [0, codes] if codes else [1, [""]])
            row = cursor.fetchall()
        # id获取所有学生model（历经缓存）
        return PracticeStudentUser.objects.get_many([i[0] for i in row])


class EvaluateStudentToCourseLogic(EvaluateBaseLogic):

    NORMAL_FIELDS = [
        'course', 'course__id'
    ] + BASE_FIELDS

    def __init__(self, auth, sid, cid, eid=''):
        """
        INIT
        :param auth:
        :param sid:
        :param cid:
        :param eid:
        """
        super(EvaluateStudentToCourseLogic, self).__init__(auth, sid, cid)

        if isinstance(eid, PracticeEvaluateStudentToCourse):
            self.evaluate = eid
        else:
            self.evaluate = self.get_evaluate_model(eid)

    def get_evaluate_model(self, eid):
        """
        获取评价model
        :param eid:
        :return:
        """
        if not eid:
            return None

        evaluate = PracticeEvaluateStudentToCourse.objects.get_once(pk=eid)
        if not evaluate:
            raise PracticeEvaluateExcept.evaluate_is_not_exists()
        return evaluate

class EvaluateStudentToTeacherLogic(EvaluateBaseLogic):

    NORMAL_FIELDS = [
        'teacher', 'teacher__id'
    ] + BASE_FIELDS

    def __init__(self, auth, sid, cid, eid=''):
        """
        INIT
        :param auth:
        :param sid:
        :param cid:
        :param eid:
        """
        super(EvaluateStudentToTeacherLogic, self).__init__(auth, sid, cid)

        if isinstance(eid, PracticeEvaluateStudentToTeacher):
            self.evaluate = eid
        else:
            self.evaluate = self.get_evaluate_model(eid)

    def get_evaluate_model(self, eid):
        """
        获取评价model
        :param eid:
        :return:
        """
        if not eid:
            return None

        evaluate = PracticeEvaluateStudentToTeacher.objects.get_once(pk=eid)
        if not evaluate:
            raise PracticeEvaluateExcept.evaluate_is_not_exists()
        return evaluate

class EvaluateTeacherToStudentLogic(EvaluateBaseLogic):

    NORMAL_FIELDS = [
        'student', 'student__id'
    ] + BASE_FIELDS

    def __init__(self, auth, sid, cid, eid=''):
        """
        INIT
        :param auth:
        :param sid:
        :param cid:
        :param eid:
        """
        super(EvaluateTeacherToStudentLogic, self).__init__(auth, sid, cid)

        if isinstance(eid, PracticeEvaluateTeacherToStudent):
            self.evaluate = eid
        else:
            self.evaluate = self.get_evaluate_model(eid)

    def get_evaluate_model(self, eid):
        """
        获取评价model
        :param eid:
        :return:
        """
        if not eid:
            return None

        evaluate = PracticeEvaluateTeacherToStudent.objects.get_once(pk=eid)
        if not evaluate:
            raise PracticeEvaluateExcept.evaluate_is_not_exists()
        return evaluate



