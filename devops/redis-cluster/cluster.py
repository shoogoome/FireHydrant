# -*- coding: utf-8 -*-
# coding:utf-8
import os
import json
import re
import yaml
import time

def cluster():
    """
    构建redis集群
    :return:
    """
    work_dir = os.getcwd()
    config_dir = work_dir + '/devops/server/config.yml'
    os.system('docker network inspect fire-hydrant-redis-cluster_redis-net > data.json')
    with open('data.json', 'r') as fp:
        # 获取网络数据
        data = json.loads(fp.read())

    if len(data) == 0:
        print("[!] service isn't up...")
        return

    info = data[0]
    containers = info.get('Containers', {})

    # 构建命令
    code = "docker run --rm -it --network fire-hydrant-redis-cluster_redis-net docker.dev.shoogoome.com/firehydrant/redis-cluster-manage:1.0 create --replicas 1 "
    for _, v in containers.items():
        try:
            num = re.findall('redis(\w)\.', v['Name'])[0]
            code += " {}:700{}".format(
                v['IPv4Address'].split('/')[0], num)
        except:
            pass
    os.system(code)
    # 修改系统配置文件
    time.sleep(5)
    os.system('docker run --rm -it --network fire-hydrant-redis-cluster_redis-net inem0o/redis-trib info redis1:7001 | cut -d : -f 2 | cut -d @ -f 1 > node.txt')
    fp = open('node.txt', 'r')
    fy = open(config_dir, 'r')
    config = yaml.load(fy)
    fy.close()

    for i in range(1, 4):
        node = fp.readline()
        config['redis-cluster']['masters' + str(i)]['host'] = 'localhost'
        config['redis-cluster']['masters' + str(i)]['port'] = int(node[:4])
    fp.close()
    with open(config_dir, 'w') as fp:
        yaml.dump(config, fp)

    os.system('rm -rf data.json node.txt')

if __name__ == '__main__':
    cluster()

