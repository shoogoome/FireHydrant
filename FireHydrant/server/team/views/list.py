# -*- coding: utf-8 -*-
# coding: utf-8

from common.core.http.firehydrant import FireHydrantView
from common.utils.helper.pagination import slicer
from common.utils.helper.params import ParamsParser
from common.utils.helper.result import SuccessResult
from ..models import Team


class TeamListView(FireHydrantView):

    def get(self, request):
        """
        获取队伍列表
        :param request:
        :return:
        """
        params = ParamsParser(request.GET)
        limit = params.int('limit', desc='每页最大渲染数', require=False, default=10)
        page = params.int('page', desc='当前页数', require=False, default=1)

        teams = Team.objects.values('id', 'nickname', 'full', 'public',
                                    'leader','leader__nickname', 'update_time')
        if params.has('nickname'):
            teams = teams.filter(nickname__contains=params.str('nickname', desc='队伍名称'))
        if params.has('full'):
            teams = teams.filter(full=params.bool('full', desc='是否满员'))
        if params.has('public'):
            teams = teams.filter(public=params.bool('public', desc='是否公开'))

        @slicer(
            teams,
            limit=limit,
            page=page
        )
        def get_team_list(obj):
            obj['leader'] = {
                'nickname': obj.get('leader__nickname', ''),
                'id': obj.get('leader')
            }
            if 'leader__nickname' in obj: del obj['leader__nickname']
            return obj

        team_list, pagination = get_team_list()
        return SuccessResult(teams=team_list, pagination=pagination)


