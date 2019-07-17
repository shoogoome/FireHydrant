from apscheduler.schedulers.blocking import BlockingScheduler
import os
import time

def mysqldump():

    path = '/root/backups'
    # 筛选一个星期以前的备份
    os.system('find {}  -ctime +7 -name "*.sql" -delete '.format(path))
    # 创建新备份
    os.system('mysqldump -h mysqldb -u root -pFireHydrant19.7**com hoho > {}/{}.sql'.format(path, time.strftime("%Y-%m-%d.%H:%M:%S", time.localtime(time.time()))))

if __name__ == '__main__':

    scheduler = BlockingScheduler()
    # 每天2点开始备份和清理数据
    scheduler.add_job(mysqldump, 'cron', hour='2', minute='0', second='0-1')
    scheduler.start()