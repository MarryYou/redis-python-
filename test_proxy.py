#coding:utf-8
import aiohttp
import asyncio
import time
from data_base import RedisClient
VALID_STATUS_CODE = [200]
TEST_URL = 'http://www.baidu.com'
BATCH_TEST_SIZE = 100
class Tester(object):
    def __init__(self):
        #初始化redis
        self.redis = RedisClient()
    async def test_single_proxy(self,proxy):
        #异步函数测试ip是否可用
        conn = aiohttp.TCPConnector(verify_ssl=False)
        async with aiohttp.ClientSession(connector=conn) as session:
            try:
                if isinstance(proxy,bytes):
                    proxy = proxy.decode('utf-8')
                real_proxy = 'http://'+proxy
                print('test proxy begining',proxy)
                async with session.get(TEST_URL,proxy=real_proxy,timeout=3) as r:
                    if r.status in VALID_STATUS_CODE:
                        self.redis.Max(proxy)
                        print('can connect')
                    else:
                        self.redis.decrease(proxy)
                        print("status_code Error")
            except:
                self.redis.decrease(proxy)
                print("can't connect")
    def run(self):
        #测试主函数
        try:
            proxies = self.redis.all()
            loop = asyncio.get_event_loop()
            for i in range(0,len(proxies),BATCH_TEST_SIZE):
                test_proxies = proxies[i:i+BATCH_TEST_SIZE]
                tasks = [self.test_single_proxy(proxy) for proxy in test_proxies]
                loop.run_until_complete(asyncio.wait(tasks))
                time.sleep(5)
        except Exception as e:
            print('Error',e.args)
        
                
            

                        
