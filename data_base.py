MAX_SCORE = 100
MIN_SCORE = 0
INIT_SCORE = 10
REDIS_HOST = 'localhost'
REDIS_PORT = '6379'
REDIS_PASSWORD =None
REDIS_KEY='proxies'
import redis
from random import choice
class RedisClient(object):
    def __init__(self,host=REDIS_HOST,port=REDIS_PORT,password=REDIS_PASSWORD):
        #初始化redis连接
        self.db = redis.StrictRedis(host=host,port=port,password=password,decode_responses=True)
    def add(self,proxy,score=INIT_SCORE):
        #新增ip
        if not self.db.zscore(REDIS_KEY,proxy):
            self.db.zadd(REDIS_KEY,score,proxy)
    def radom(self):
        #随机ip获取
        result = self.db.zrangebyscore(REDIS_KEY,MAX_SCORE,MAX_SCORE)
        if len(result):
            return choice(result)
        else:
            result = self.db.zrangebyscore(REDIS_KEY,0,100)
            if len(result):
                return choice(result)
            else:
                raise 'PoolEmptyError'
    def decrease(self,proxy):
        #检测ip得分 低分移除
        score = self.db.zscore(REDIS_KEY,proxy)
        if score  and score >MIN_SCORE:
            print('ipProxy',proxy,score,'-10')
            return self.db.zincrby(REDIS_KEY,proxy,-10)
        else:
            print('ipProxy', proxy,score, 'remove')
            return self.db.zrem(REDIS_KEY,proxy)
    def exists(self,proxy):
        #判断ip是否存在
        return not self.db.zscore(REDIS_KEY,proxy) == None
    def Max(self,proxy):
        #ip可用
        print('ipproxy',proxy,'can connect website','score:',MAX_SCORE)
        return self.db.zadd(REDIS_KEY,MAX_SCORE,proxy)
    def count(self):
        #ip数量
        return self.db.zcard(REDIS_KEY)
    def all(self):
        #获取全部
        return self.db.zrangebyscore(REDIS_KEY,MIN_SCORE,MAX_SCORE)

        
