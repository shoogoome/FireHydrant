

from common.core.auth.check_login import check_login
from common.core.http.facec import FireHydrantFacecView
from common.enum.account.role import AccountRoleEnum
from common.utils.helper.pagination import slicer
from common.utils.helper.params import ParamsParser
from common.utils.helper.result import SuccessResult
from server.faceU.logic.record import FaceURecordLogic
from server.faceU.models import FaceUDistinguishRecord
from ...models import FaceUAccount


class FaceURecordListMgetView(FireHydrantFacecView):

    @check_login
    def get(self, request):
        """
        获取记录列表
        :param request:
        :return:
        """
        params = ParamsParser(request.GET)
        limit = params.int('limit', desc='每页最大渲染数', require=False, default=10)
        page = params.int('page', desc='当前页数', require=False, default=1)

        if self.auth.get_account().role == int(AccountRoleEnum.ADMIN) and \
            params.has('account'):
            _account = FaceUAccount.objects.get_once(pk=params.int('account', desc="用户id"))
        else:
            _account = self.auth.get_account()

        record = FaceUDistinguishRecord.objects.filter(author=_account)\
            .values('id', 'update_time', 'group_id').order_by('-create_time')
        if params.has('group'):
            record = record.filter(group_id=params.int('group', desc='分组id'))
        if params.has('start_time'):
            record = record.filter(create_time__gte=params.float('start_time', desc='开始时间'))
        if params.has('end_time'):
            record = record.filter(create_time__lte=params.float('end_time', desc='结束时间'))
        if params.has('overall'):
            record = record.filter(group__isnull=params.bool('overall', desc='全局与否'))
        record_list, pagination = slicer(record, limit=limit, page=page)()()
        return SuccessResult(records=record_list, pagination=pagination)

    @check_login
    def post(self, request):
        """
        批量获取记录信息
        :param request:
        :return:
        """
        params = ParamsParser(request.JSON)
        logic = FaceURecordLogic(self.auth)
        ids = params.list('ids', desc='id列表')
        _admin = self.auth.get_account().role == int(AccountRoleEnum.ADMIN)
        _auth = self.auth.get_account().id

        data = []
        records = FaceUDistinguishRecord.objects.get_many(pks=ids)
        for record in records:
            if not _admin and record.author_id != _auth:
                continue
            try:
                logic.record = record
                data.append(logic.get_record_info())
            except:
                pass

        return SuccessResult(data)

