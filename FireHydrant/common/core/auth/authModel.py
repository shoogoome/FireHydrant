from server.account.models import Account


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
