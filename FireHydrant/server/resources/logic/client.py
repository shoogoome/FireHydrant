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
        self.download_token_url = '/download/token'
        self.upload_token_url = '/upload/token'
        self.upload_finish_url = '/upload/finish'
        self.file_info_url = '/file/info'
        self.headers = {
            'systemToken': LIUMA_SYSTEM_TOKEN
        }

    def get_download_token(self, fhash):
        """
        获取文件下载token
        :param fhash 文件hash值
        :return:
        """
        return self.get_token('{}{}'.format(self.base_url, self.download_token_url), fhash)

    def get_upload_token(self, fhash):
        """
        获取文件上传token
        :param fhash:
        :return:
        """
        return self.get_token('{}{}'.format(self.base_url, self.upload_token_url), fhash)

    def upload_finish(self, token, name):
        """
        完成上传
        :param token:
        :param name:
        :return:
        """
        self.headers['token'] = token
        # 查看是否为单文件上传
        response = requests.get("{}{}".format(self.base_url, self.file_info_url), headers=self.headers)
        try:
            data = response.json()
            if data.get('data', None) is not None:
                return True
        except:
            pass
        # 分片合并
        response = requests.get('{}{}?fire_name={}'.format(
            self.base_url, self.upload_finish_url, name), headers=self.headers)

        if response.status_code != 200:
            return False
        return True

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




