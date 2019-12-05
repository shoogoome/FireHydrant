from ..models import Account
from common.exceptions.account.info import AccountInfoExcept
from common.utils.helper.m_t_d import model_to_dict
from server.team.models import AccountTeam
from server.resources.logic.info import ResourceLogic
from common.utils.helper.durl import DataUrlParser
from common.core.dao.storage.local import FireHydrantLocalStorage

class AccountLogic(object):

    NORMAL_FIELD = [
        'username', 'sex', 'nickname', 'role', 'phone', 'motto', 'create_time',
        'update_time', 'avator', 'id',
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
        info = model_to_dict(self.account, self.NORMAL_FIELD)
        account_team = AccountTeam.objects.filter(account=self.account)
        if account_team.exists():
            team = account_team[0].team
            info['team'] = {
                'nickname': team.nickname,
                'id': team.id,
                'role': account_team[0].role,
                'create_time': account_team[0].create_time
            }
        else:
            info['team'] = None
        # 获取头像资源下载token
        from common.core.dao.storage.local import FireHydrantLocalStorage
        info['avator'] = FireHydrantLocalStorage.generate_token(info['avator'], self.account.id)
        return info

    @staticmethod
    def save_account_avator(acount_id, durl):
        """
        保存用户头像
        :param acount_id:
        :param durl:
        :return:
        """
        parser = DataUrlParser(durl)
        storage = FireHydrantLocalStorage('account_avator')
        path = storage.save_file('{}/avator.{}'.format(
            acount_id,
            parser.mime
        ), parser.data, 'wb')

        return path