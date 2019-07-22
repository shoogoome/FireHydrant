from server.account.models import Account
from common.constants.params import *
from common.utils.hash.signatures import session_signature


class Authorization(object):

    def __init__(self, **kwargs):
        """
        INIT
        :param kwargs:
        """

    def is_login(self):
        """
        判断登陆与否
        :return:
        """
        ...

    def get_account(self):
        """
        获取账户model
        :return:
        """
        ...

    def set_account(self, account):
        """
        设置账户
        :return:
        """
        ...


class FireHydrantAuthorization(Authorization):

    def __init__(self, **kwargs):
        """
        FireHydrant授权
        :param kwargs:
        """
        super(FireHydrantAuthorization, self).__init__(**kwargs)
        self._is_login = False
        self._account = None
        self._association_id = ""
        self._school_id = ""

    def is_login(self):
        """
        返回登陆情况
        :return:
        """
        return self._is_login

    def get_account(self):
        """
        返回账户model
        :return:
        """
        return self._account

    def set_account(self, account):
        """
        设置账户model
        :param account:
        :return:
        """
        self._account = account

    def get_school_id(self):
        """
        返回当前学校id
        :return:
        """
        return self._school_id

    def get_association_id(self):
        """
        返回当前协会id
        :return:
        """
        return self._association_id

    @staticmethod
    def fetch_account_by_id(aid):
        """
        id查询账户model
        :param aid:
        :return:
        """
        return Account.objects.get_once(pk=aid)

    def set_login_status(self, account_id):
        """
        挂起用户信息
        :param account_id:
        :return:
        """
        if account_id is not None:
            account = FireHydrantAuthorization.fetch_account_by_id(account_id)
            if account is not None:
                self._is_login = True
                self._account = account
                return True

        return False


class FireHydrantAuthAuthorization(FireHydrantAuthorization):

    def __init__(self, request, view):
        """
        auth验证
        :param request:
        :param view:
        """
        super(FireHydrantAuthAuthorization, self).__init__(request=request, view=view)
        self.request = request
        self.view = view
        self.load_from_session()

    def load_from_session(self):
        """
        载入登陆信息
        :return:
        """
        # 读取用户id
        account_id = self.request.session.get(FIREAUTHSESSION, '')
        # 挂起登陆信息
        if not self.set_login_status(account_id):
            self.load_from_cookie()

    def load_from_cookie(self):
        """
        从Cookie里读取登录信息
        :return:
        """
        user_token = self.request.COOKIES.get(FIREAUTHSIGN, '')
        # 如果未能从cookie中获取信息，直接返回
        if user_token.strip() == '':
            return False

        self.set_login_status(user_token)


    def set_session(self):
        """
        设置登陆信息
        :return:
        """
        if self._account is None:
            return False

        self.request.session[FIREAUTHSESSION] = self._account.id
        # 产生登陆签名
        sign = session_signature(self._account.id)

        self.view.set_cookie(
            key=FIREAUTHSIGN,
            value=sign,
        )

        return True









