from ..models import Account
from common.exceptions.account.info import AccountInfoExcept
from common.utils.helper.m_t_d import model_to_dict


class AccountLogic(object):

    NORMAL_FIELD = [
        'username', 'sex', 'nickname', 'role', 'phone', 'motto', 'create_time',
        'update_time', 'avator',
    ]

    def __init__(self, auth, aid=''):
        """
        INIT
        :param auth:
        :param aid:
        """
        self.auth = auth

        if isinstance(aid, Account):
            self.account = aid
        else:
            self.account = self.get_account_model(aid)

    def get_account_model(self, aid=""):
        """
        获取账户数据库对象
        :param aid:
        :return:
        """
        if aid == "" or aid is None:
            return None

        account = Account.objects.get_once(pk=aid)
        if account is None:
            raise AccountInfoExcept.account_is_not_exists()
        return account

    def get_account_info(self):
        """
        获取账户信息
        :return:
        """
        if self.account is None:
            return dict()
        return model_to_dict(self.account, self.NORMAL_FIELD)

