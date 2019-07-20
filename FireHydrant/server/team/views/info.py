#-*- coding: utf-8 -*-
# coding: utf-8

from common.core.auth.check_login import check_login
from common.core.http.view import FireHydrantView
from common.utils.helper.params import ParamsParser
from ..models import Team, AccountTeam
from django.db import transaction
from common.exceptions.account.info import AccountInfoExcept
from common.utils.helper.result import SuccessResult
from common.utils.helper.m_t_d import model_to_dict
from common.utils.hash import signatures
from common.decorate.administrators import administrators
from common.exceptions.team.info import TeamInfoExcept
from common.enum.team.role import TeamRoleEnum
from ..logics.team import TeamLogic

class TeamInfoView(FireHydrantView):

    @check_login
    def post(self, request):
        """
        创建队伍
        :param request:
        :return:
        """
        params = ParamsParser(request.JSON)

        if len(AccountTeam.objects.filter_cache(account=self.auth.get_account())) > 0:
            raise TeamInfoExcept.already_in_team()
        # 队伍名称不得重复
        nickname = params.str('nickname', desc='队伍名称')
        if Team.objects.filter(nicknam=nickname).exists():
            raise TeamInfoExcept.nickname_is_exists()

        with transaction.atomic():
            team = Team.objects.create(
                nickname=nickname,
                leader=self.auth.get_account(),
                slogan=params.str('slogan', desc='口号', default='', require=False),
                password=params.str('password', desc='密码'),
            )
            AccountTeam.objects.create(
                team=team,
                account=self.auth.get_account(),
                role=int(TeamRoleEnum.LEADER),
            )

        return SuccessResult(id=team.id)

    def get(self, request, tid):
        """
        获取队伍信息
        :param request:
        :param tid:
        :return:
        """
        logic = TeamLogic(self.auth, tid)

        return SuccessResult(logic.get_team_info())

    def put(self, request, tid):
        """
        修改队伍信息
        :param request:
        :param tid:
        :return:
        """
        ...









