import requests

from chrome import Chrome


class Index:
    def __init__(self):
        self.ss = requests.session()
        chrome = Chrome()
        cookies = chrome.cookie('.baidu.com')
        self.ss.cookies.update(cookies)
        baseheaders = {
            'Accept': 'application/json, text/plain, */*',
            'Accept-Encoding': 'gzip, deflate',
            'Accept-Language': 'zh-CN,zh;q=0.9',
            'Cache-Control': 'no-cache',
            'DNT': '1',
            'Host': 'index.baidu.com',
            'Pragma': 'no-cache',
            'Referer': 'http://index.baidu.com/v2/main/index.html',
            'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_0) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/79.0.3945.88 Safari/537.36',
            'X-Requested-With': 'XMLHttpRequest',
        }
        self.ss.headers.update(baseheaders)

    def __get(self, url):
        ret = self.ss.get(url, timeout=10)
        data = ret.json()
        if data['status'] != 0:
            raise Exception('request error')
        return data['data']

    def __ptbk(self, uniqid):
        url = f'http://index.baidu.com/Interface/ptbk?uniqid={uniqid}'
        data = self.__get(url)
        return data

    def index(self, word, area=0, start_date='2014-01-01', end_date='2019-12-31'):
        url = f'http://index.baidu.com/api/SearchApi/index?area={area}&word={word}&startDate={start_date}&endDate={end_date}'
        data = self.__get(url)
        key = self.__ptbk(data['uniqid'])
        for idx in range(len(data['userIndexes'])):
            data['userIndexes'][idx]['all']['data'] = self.decrypt(
                key, data['userIndexes'][idx]['all']['data'])

            data['userIndexes'][idx]['pc']['data'] = self.decrypt(
                key, data['userIndexes'][idx]['pc']['data'])

            data['userIndexes'][idx]['wise']['data'] = self.decrypt(
                key, data['userIndexes'][idx]['wise']['data'])

        return data

    @staticmethod
    def decrypt(key, data):
        temp = {}
        res = []
        lk = len(key)
        ld = len(data)
        for i in range(lk // 2):
            temp[key[i]] = key[lk // 2 + i]

        for i in range(ld):
            res.append(temp[data[i]])
        return "".join(res)
