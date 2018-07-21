TESTER_CYCLE = 20
GETTER_CYCLE = 20
TESTER_ENABLED = True
GETTER_ENABLED = True
API_ENABLED = True
API_HOST = '0.0.0.0'
API_PORT = '5000'
from multiprocessing import Process
from restful_api import app
from crawl import crawl
from test_proxy import Tester
import time

class Scheduler():
    def schedule_tester(self,cycle=TESTER_CYCLE):
        #定时测试代理
        tester = Tester()
        while True:
            tester.run()
            time.sleep(cycle)

    def schedule_getProxy(self, cycle=GETTER_CYCLE):
        #定时抓取代理
        while True:
            crawl()
            time.sleep(cycle)
    def schedule_api(self):
        #启动api服务
        app.run(API_HOST,API_PORT)
    def run(self):
        print('代理池开始运行')
        if TESTER_ENABLED:
            tester_process = Process(target=self.schedule_tester)
            tester_process.start()
        if GETTER_ENABLED:
            getter_process = Process(target=self.schedule_getProxy)
            getter_process.start()
        if API_ENABLED:
            api_process = Process(target=self.schedule_api)
            api_process.start()
def main():
    scheduler = Scheduler()
    scheduler.run()

if __name__ == '__main__':
    main()