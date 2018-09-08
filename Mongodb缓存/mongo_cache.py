import pickle  # 对象序列化
import zlib  # 压缩数据
from datetime import datetime, timedelta  # 设置缓存超时间隔
from pymongo import MongoClient
from bson.binary import Binary  # MongoDB存储二进制的类型


class MongoCache(object):
    '''
    数据库缓存
    '''

    # # 连接数据库
    # client = pymongo.MongoClient(host='localhost', port=27017)
    # # 获取数据库实例
    # db = client.test
    # # 创建studnets集合
    # collection = db.students

    # result = requests.get('https://www.qiushibaike.com/8hr/page/1')



    def __init__(self, client=None, expires=timedelta(days=30)):
        self.client = MongoClient("localhost", 27017),
        self.db = self.client.cache,
        web_page = self.db.webpage,
        self.db.webpage.create_index('timestamp', expireAfterSeconds=expires.total_seconds())


    def __setitem__(self, key, value):
        record = {"result": Binary(zlib.compress(pickle.dumps(value))), "timestamp": datetime.utcnow()}
        self.db.webpage.update({"_id": key}, {"$set": record}, upsert=True)


    def __getitem__(self, item):
        '''
        将缓存数据照item作为key取出（key任然是下载的url）
        :param self:
        :param item:
        :return:
        '''
        record = self.db.webpage.find_one({"_id": item})
        if record:
            return pickle.loads(zlib.decompress(record['result']))
        else:
            raise KeyError(item + "does not exist")

    def __contains__(self, item):
        '''
        当调用in,not in 会调用该方法判断链接对应网址是否在数据库中
        :param self:
        :param item:        下载的url链接
        :return:
        '''
        try:
            self[item]
        except KeyError:
            return False
        else:
            return True

    def clear(self):
        self.db.webpage.drop()
