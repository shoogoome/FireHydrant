from server.account.models import AccountExhibition
from common.exceptions.account.exhibition import AccountExhibitionExcept
from common.utils.helper.m_t_d import model_to_dict
from server.resources.models import ResourcesMeta
from server.resources.logic.info import ResourceLogic

class ExhibitionLogic(object):

    NORMAL_FILED = [
        'account', 'account__id', 'title', 'content', 'show', 'create_time', 'update_time'
    ]

    def __init__(self, auth, eid):
        """
        INIT
        :param auth:
        :param eid:
        """
        self.auth = auth

        if isinstance(eid, AccountExhibition):
            self.exhibition = eid
        else:
            self.exhibition = self.get_exhibition_model(eid)

    def get_exhibition_model(self, eid):
        """
        获取展示model
        :param eid:
        :return:
        """
        if eid is None or eid == '':
            return None

        exhibition = AccountExhibition.objects.get_once(pk=eid)
        if exhibition is None:
            raise AccountExhibitionExcept.exhibition_is_not_exists()

        return exhibition

    def get_exhibition_info(self):
        """
        获取作品展示信息
        :return:
        """
        if self.exhibition is None:
            return dict()

        data = model_to_dict(self.exhibition, self.NORMAL_FILED)
        data['resource'] = [{
            'name': meta.name,
            'size': meta.size,
            'create_time': meta.create_time,
            'token': ResourceLogic.get_download_token(meta.hash)
        } for meta in self.exhibition.resource.all()]
        return data

