from ..models import PracticeStudentUser
from .school import SchoolLogic
from common.exceptions.practice.school.studentuser import PracticeStudentUserInfoExcept
from common.utils.helper.m_t_d import model_to_dict
from django.db import transaction

from common.core.auth.check_login import check_login
from common.core.http.view import FireHydrantView
from common.utils.helper.params import ParamsParser
from common.utils.helper.result import SuccessResult
from common.exceptions.practice.school.studentuser import PracticeStudentUserInfoExcept
from django.db.models import Q
from server.account.models import Account
from common.enum.account.sex import AccountSexEnum
from common.enum.account.role import AccountRoleEnum
from common.utils.hash import signatures

class StudentUserLogic(SchoolLogic):

    NORMAL_FIELDS = [
        'account', 'account__id', 'school', 'school__id', 'code', 'realname',
        'create_time', 'update_time', 'id'
    ]

    def __init__(self, auth, sid, stid=''):
        """
        INIT
        :param auth:
        :param sid:
        :param stid:
        """
        super(StudentUserLogic, self).__init__(auth, sid)

        if isinstance(stid, PracticeStudentUser):
            self.studentuser = sid
        else:
            self.studentuser = self.get_studentuser_model(stid)

    def get_studentuser_model(self, stid):
        """
        获取学生model
        :param stid:
        :return:
        """
        if not stid:
            return None
        studentuser = PracticeStudentUser.objects.get_once(stid)
        if not studentuser:
            raise PracticeStudentUserInfoExcept.studentuser_is_not_exists()
        return studentuser

    def get_studentuser_info(self):
        """
        获取学生信息
        :return:
        """
        if not self.studentuser:
            return {}
        return model_to_dict(self.studentuser, self.NORMAL_FIELDS)

    def create_studentuser(self, params: ParamsParser):
        """
        创建学生账户
        :param params:
        :return:
        """
        code = params.str('code', desc='学号')
        phone = params.str('phone', desc='手机')

        # 学号存在或者，账号已绑定该学校则直接放回
        studentuser = PracticeStudentUser.objects.filter(school=self.school).filter(
                Q(code=code) |
                Q(account__phone=phone)
        )
        if studentuser.exists():
            return studentuser[0]

        account = Account.objects.filter(phone=phone)
        if account.exists():
            account = account[0]
        else:
            with transaction.atomic():
                try:
                    account = Account.objects.create(
                        username='{}@{}'.format(phone, self.school.name),
                        sex=int(AccountSexEnum.UNKNOW),
                        password=signatures.build_password_signature(phone, signatures.gen_salt()),
                        nickname=params.str('realname', desc='真实名称'),
                        role=int(AccountRoleEnum.USER),
                        phone=phone,
                    )
                except Exception as ex:
                    transaction.rollback()
                    raise PracticeStudentUserInfoExcept.create_studentuser_fail()

        with transaction.atomic():
            try:
                studentuser = PracticeStudentUser.objects.create(
                    account=account,
                    school=self.school,
                    code=code,
                    realname=params.str('realname', desc='真实名称'),
                )
            except Exception as ex:
                transaction.rollback()
                raise PracticeStudentUserInfoExcept.create_studentuser_fail()

        return studentuser