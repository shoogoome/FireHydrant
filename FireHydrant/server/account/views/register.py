
# from common.core.auth.check_login import check_login
from common.core.http.view import FireHydrantView
from common.utils.helper.params import ParamsParser
from ..models import Account
from django.db import transaction
from common.exceptions.account.info import AccountInfoExcept
from common.utils.helper.result import SuccessResult
from common.utils.hash import signatures
from common.constants.length_limitation import *

class AccountRegisterView(FireHydrantView):

    def post(self, request):
        """
        注册账户
        :param request:
        :return:
        """
        params = ParamsParser(request.JSON)

        # TODO: 后续添加邮箱验证
        username = params.str('username', desc='用户名', max_length=MAX_USERNAME_LENGTH)
        if Account.objects.filter(username=username).exists():
            raise AccountInfoExcept.username_is_exists()

        with transaction.atomic():
            account = Account.objects.create(
                username=username,
                sex=params.int('sex', desc='性别', default=0, require=False),
                nickname=username,
                password=signatures.build_password_signature(params.str(
                    'password', desc='密码', min_length=MIN_PASSWORD_LENGTH, max_length=MAX_PASSWORD_LENGTH), signatures.gen_salt()),
            )
        return SuccessResult(id=account.id)



