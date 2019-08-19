# -*- coding: utf-8
# coding: utf-8
from FireHydrant.settings import LIUMA_SYSTEM_TOKEN
import requests
from common.exceptions.resources.liuma import LiumaInfoExcept

class LiumaClient(object):

    def __init__(self):
        """
        流马文件服务器客户端
        """
        self.base_url = 'http://liuma.shoogoome.com'
        self.download_url = '/download/token'
        self.upload_url = '/upload/token'
        self.headers = {
            'systemToken': LIUMA_SYSTEM_TOKEN
        }

    def get_download_token(self, fhash):
        """
        获取文件下载token
        :param fhash 文件hash值
        :return:
        """
        return self.get_token('{}{}'.format(self.base_url, self.download_url), fhash)

    def get_upload_token(self, fhash):
        """
        获取文件上传token
        :param fhash:
        :return:
        """
        return self.get_token('{}{}'.format(self.base_url, self.upload_url), fhash)


    def get_token(self, url, fhash):
        """
        获取token
        :param url:
        :param fhash:
        :return:
        """
        response = requests.get('{}?hash={}'.format(url, fhash), headers=self.headers)

        if response.status_code != 200:
            raise LiumaInfoExcept.get_token_fail()
        try:
            return response.json()['data']['token']
        except:
            raise LiumaInfoExcept.get_token_fail()




