from ..models import Team
from common.exceptions.team.info import TeamInfoExcept
from common.utils.helper.m_t_d import model_to_dict

class TeamLogic(object):

    NORMAL_FIELD = [
        'nickname', 'leader', 'leader__id', 'leader__nickname', 'leader__id',
        'slogan', 'maximum_number', 'full', 'public', 'create_time', 'update_time',
    ]

    def __init__(self, auth, tid=''):
        """
        INIT
        :param auth:
        :param tid:
        """
        self.auth = auth

        if isinstance(tid, Team):
            self.team = tid
        else:
            self.team = self.get_team_model(tid)

    def get_team_model(self, tid):
        """
        获取队伍
        :param tid:
        :return:
        """
        if tid == '' or tid is None:
            return None

        team = Team.objects.get_once(pk=tid)
        if team is None:
            raise TeamInfoExcept.team_is_not_exists()
        return team

    def get_team_info(self):
        """
        获取队伍信息
        :return:
        """
        if self.team is None:
            return dict()
        return model_to_dict(self.team, self.NORMAL_FIELD)