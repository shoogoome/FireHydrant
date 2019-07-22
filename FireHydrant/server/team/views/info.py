# -*- coding: utf-8 -*-
# coding: utf-8

from django.db import transaction

from common.core.auth.check_login import check_login
from common.core.http.view import FireHydrantView
from common.enum.team.role import TeamRoleEnum
from common.exceptions.team.info import TeamInfoExcept
from common.utils.helper.params import ParamsParser
from common.utils.helper.result import SuccessResult
from ..logics.team import TeamLogic
from common.constants.length_limitation import *
from ..models import Team, AccountTeam


class TeamInfoView(FireHydrantView):

    @check_login
    def post(self, request):
        """
        创建队伍
        :param request:
        :return:
        """
        params = ParamsParser(request.JSON)

        if AccountTeam.objects.filter(account=self.auth.get_account()).exists():
            raise TeamInfoExcept.already_in_team()
        # 队伍名称不得重复
        nickname = params.str('nickname', desc='队伍名称', max_length=MAX_TEAM_NICKNAME_LENGTH)
        if Team.objects.filter(nickname=nickname).exists():
            raise TeamInfoExcept.nickname_is_exists()

        with transaction.atomic():
            team = Team.objects.create(
                nickname=nickname,
                leader=self.auth.get_account(),
                slogan=params.str('slogan', desc='口号', default='', require=False, max_length=MAX_SLOGAN_LENGTH),
                password=params.str('password', desc='密码', min_length=MIN_TEAM_PASSWORD, max_length=MAX_TEAM_PASSWORD),
                public=params.bool('public', desc='是否开放组队', default=False, require=False)
            )
            AccountTeam.objects.create(
                team=team,
                account=self.auth.get_account(),
                role=int(TeamRoleEnum.LEADER),
            )

        return SuccessResult(id=team.id)

    @check_login
    def get(self, request, tid):
        """
        获取队伍信息
        :param request:
        :param tid:
        :return:
        """
        logic = TeamLogic(self.auth, tid)

        return SuccessResult(logic.get_team_info())

    @check_login
    def put(self, request, tid):
        """
        修改队伍信息
        :param request:
        :param tid:
        :return:
        """
        logic = TeamLogic(self.auth, tid)
        params = ParamsParser(request.JSON)

        # TODO: 卡队伍 卡队长
        team = logic.team
        with params.diff(team):
            team.slogan = params.str('slogan', desc='口号', max_length=MAX_SLOGAN_LENGTH)
            team.password = params.str('password', desc='入队密码', min_length=MIN_TEAM_PASSWORD, max_length=MAX_TEAM_PASSWORD)
            team.public = params.bool('public', desc='是否公开队伍')

        if params.has('nickname'):
            nickname = params.str('nickname', desc='队伍名称', max_length=MAX_TEAM_NICKNAME_LENGTH)
            if Team.objects.filter(nickname=nickname).exclude(id=tid).exists():
                raise TeamInfoExcept.nickname_is_exists()
            team.nickname = nickname
        if params.has('leader'):
            leader = AccountTeam.objects.get_once(pk=params.int('leader', desc='队长id'))
            if leader is None or leader.team != logic.team:
                raise TeamInfoExcept.leader_is_not_exists()
            # 队长修改时需改变角色 管理员不用
            if logic.account is not None:
                logic.account.role = int(TeamRoleEnum.MEMBER)
                logic.account.save()
            team.leader = leader

        team.save()
        return SuccessResult(id=tid)

    @check_login
    def delete(self, request, tid):
        """
        解散队伍或退出队伍
        :param request:
        :param tid:
        :return:
        """
        logic = TeamLogic(self.auth, tid)
        # 成员则退出队伍
        if logic.account is not None and logic.account.role != int(TeamRoleEnum.LEADER):
            logic.account.delete()
            logic.team.full = False
            logic.team.save()
        # 否则解散队伍
        else:
            logic.team.delete()

        return SuccessResult(id=tid)


class TeamJoinView(FireHydrantView):

    @check_login
    def post(self, request, tid):
        """
        加入队伍
        :param request:
        :param tid:
        :return:
        """
        logic = TeamLogic(self.auth, tid)

        if AccountTeam.objects.filter(account=self.auth.get_account()).exists():
            raise TeamInfoExcept.already_in_team()











