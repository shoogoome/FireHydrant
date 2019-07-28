# -*- coding: utf-8 -*-
# coding: utf-8
from django.db import transaction

from common.core.auth.check_login import check_login
from common.core.http.view import FireHydrantView
from common.exceptions.team.info import TeamInfoExcept
from common.utils.helper.pagination import slicer
from common.utils.helper.params import ParamsParser
from common.utils.helper.result import SuccessResult
from common.enum.account.role import AccountRoleEnum
from ..logics.team import TeamLogic
from ..models import AccountTeam


class TeamManageView(FireHydrantView):

    @check_login
    def post(self, request, tid):
        """
        加入队伍
        :param request:
        :param tid:
        :return:
        """
        if AccountTeam.objects.filter(account=self.auth.get_account()).exists():
            raise TeamInfoExcept.already_in_team()

        logic = TeamLogic(self.auth, tid)
        params = ParamsParser(request.JSON)
        # 检查入队密码
        password = params.str('password', desc='入队密码', default='', require=False)
        if not logic.team.public and password != logic.team.password:
            raise TeamInfoExcept.password_error()
        # 检查队伍人员是否满员
        if logic.team.full:
            raise TeamInfoExcept.team_is_full()

        with transaction.atomic():
            account = AccountTeam.objects.create(
                team=logic.team,
                account=self.auth.get_account(),
            )
        if AccountTeam.objects.filter(team=logic.team).count() >= logic.team.maximum_number:
            logic.team.full = True
            logic.team.save()

        return SuccessResult(id=account.id)

    @check_login
    def get(self, request, tid):
        """
        获取队伍成员列表
        :param request:
        :param tid:
        :return:
        """
        logic = TeamLogic(self.auth, tid)
        params = ParamsParser(request.GET)
        limit = params.int('limit', desc='每页最大渲染数', require=False, default=10)
        page = params.int('page', desc='当前页数', require=False, default=1)

        accounts = AccountTeam.objects.filter(team=logic.team).values(
            'id', 'role', 'account', 'account__nickname',
            'free', 'update_time',
        )
        if params.has('role'):
            accounts = accounts.filter(role=params.int('role', desc='角色'))
        if params.has('free'):
            accounts = accounts.filter(free=params.bool('free', desc='空闲与否'))
        if params.has('key'):
            accounts.filter(account__nickname__contains=params.str('key', desc='关键字'))

        @slicer(
            accounts,
            limit=limit,
            page=page
        )
        def get_accounts_list(obj):
            obj['account'] = {
                'id': obj.get('account', ''),
                'nickname': obj.get('account__nickname', '')
            }
            if 'account__nickname' in obj: del obj['account__nickname']
            return obj

        account_list, pagination = get_accounts_list()
        return SuccessResult(accounts=account_list, pagination=pagination)

    @check_login
    def put(self, request, tid):
        """
        修改成员角色
        :param request:
        :param tid:
        :return:
        """
        logic = TeamLogic(self.auth, tid)
        params = ParamsParser(request.JSON)

        ids = params.list('ids', desc='成员id列表')
        role = params.int('role', desc='角色enum')
        # 过滤错误role
        if not AccountRoleEnum.has_value(role):
            raise TeamInfoExcept.role_error()

        status = dict()
        accounts = AccountTeam.objects.get_many(pks=ids)
        for account in accounts:
            if account.team == logic.team:
                account.role = role
                account.save()
                status[str(account.id)] = 1
            else:
                status[str(account.id)] = 0
        return SuccessResult(status=status)


