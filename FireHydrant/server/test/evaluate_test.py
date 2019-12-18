from django.test import TestCase
from server.practice.models import PracticeEvaluateStudentToCourse, PracticeStudentUser, PracticeCourse, PracticeSchool
from server.account.models import Account
from common.utils.hash.signatures import gen_salt, build_password_signature
from common.enum.account.role import AccountRoleEnum
from common.enum.account.sex import AccountSexEnum
from common.utils.helper.m_t_d import model_to_dict
import time
import json

class EvaluateTest(TestCase):

    FIELD = [
        'id', 'author', 'course', 'star', 'message', 'create_time',
        'update_time', 'author__id', 'course__id'
    ]

    def setUp(self):
        """
        init
        :return:
        """
        school = PracticeSchool.objects.create(
            name='北京师范大学珠海分校',
        )
        account = Account.objects.create(
            username='test',
            sex=int(AccountSexEnum.MALE),
            password=build_password_signature('password', gen_salt()),
            nickname='test',
            role=int(AccountRoleEnum.ADMIN),
            phone='13000000000',
        )
        self.student = PracticeStudentUser.objects.create(
            account=account,
            school=school,
            code='1700000000',
            realname='121',
        )
        self.course = PracticeCourse.objects.create(
            school=school,
            author=account,
            name='软件测试',
            description='教授软件开发测试流程及方法',
            start_time=time.time(),
            end_time=time.time() + 3600
        )

    def test_tent(self):
        """
        评价测试
        :return:
        """
        sc = PracticeEvaluateStudentToCourse.objects.create(
            author=self.student,
            star=4,
            message='课程很好我很喜欢',
            course=self.course
        )
        print(json.dumps(model_to_dict(sc, self.FIELD), indent=1))

        sc.delete()







