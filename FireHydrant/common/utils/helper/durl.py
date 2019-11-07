import re
import base64

class DataUrlParser(object):

    def __init__(self, durl):

        self.__parse(durl)
        self.data = None
        self.mime = 'txt'
        self.__parse(durl)

    def __parse(self, durl):
        """
        解析data url
        :param durl:
        :return:
        """
        r = re.findall('^data:(.*?);base64,(.*?)$', durl)

        assert len(r) == 1, "no match"
        self.data = base64.b64decode(r[0][-1])
        self.mime = r[0][0].split('/')[-1]

