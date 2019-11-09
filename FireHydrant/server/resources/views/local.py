# -*- coding: utf-8 -*-
# coding:utf-8

import os
from django.http.response import HttpResponse
from common.core.http.firehydrant import FireHydrantView
from common.utils.helper.params import ParamsParser
from common.core.dao.storage.local import FireHydrantLocalStorage
from common.constants.storages import MIME_TO_EXT_MAPPING, NGINX_RESOURCE_PATH, FIRE_HYDRANT_DATA_ROOT

class FireHydrantLocalResourceView(FireHydrantView):

    def get(self, request, token):
        """
        全局资源文件下载
        :param request:
        :param token:
        :return:
        """
        path, filename = FireHydrantLocalStorage.decode_token(token, self.auth)
        params = ParamsParser(request.GET)
        download = params.bool('download', desc='下载与否', require=False, default=False)

        mime = MIME_TO_EXT_MAPPING.get(filename.split('.')[-1], 'text/html')
        resp = HttpResponse(content_type=mime)
        resp['X-Accel-Redirect'] = os.path.join(
            path.replace(FIRE_HYDRANT_DATA_ROOT, NGINX_RESOURCE_PATH),
            filename
        )
        resp['Content-Disposition'] = '{0}; filename={1}'.format(
            'attachment' if download else 'inline',
            filename
        )
        resp['Via'] = "FireHydrant"
        return resp
