
from ..models import FaceUAccount
from common.exceptions.faceU.account.info import FaceUAccountInfoExcept
from common.utils.helper.m_t_d import model_to_dict

class FaceUAccountLogic(object):

    NORMAL_FIELDS = [
        'username', 'sex', 'nickname', 'role', 'phone', 'phone_validated',
        'avator', 'motto',
    ]

    def __init__(self, auth, aid=''):
        """
        INIT
        :param auth:
        :param aid:
        """
        self.auth = auth

        if isinstance(aid, FaceUAccount):
            self.account = aid
        else:
            self.account = self.get_account_model(aid)

    def get_account_model(self, aid):
        """
        获取用户model
        :param aid:
        :return:
        """
        if not aid:
            return None

        account = FaceUAccount.objects.get_once(pk=aid)
        if not account:
            raise FaceUAccountInfoExcept.account_is_not_exists()
        return account

    def get_account_info(self):
        """
        获取用户信息
        :return:
        """
        if not self.account:
            return {}
        info = model_to_dict(self.account, self.NORMAL_FIELDS)
        return info





