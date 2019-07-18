# -*- coding: utf-8 -*-
# coding:utf-8
import os
import json
import re
import yaml
import time
import re

def cluster():
    """
    构建redis集群
    :return:
    """
    env_dist = os.environ
    env = env_dist.get('FIRE_HYRANT_ENV', '')
    work_dir = os.getcwd()
    config_dir = work_dir + '/devops/server/config.yml'

    if env != 'online':
        os.system('docker network inspect fire-hydrant-redis-cluster_redis-net > data.json')
        with open('data.json', 'r') as fp:
            # 获取网络数据
            data = json.loads(fp.read())

        if len(data) == 0:
            print("[!] service isn't up...")
            return

        info = data[0]
        containers = info.get('Containers', {})
    else:
        os.system("kubectl get pod -owide -n fire-hydrant | grep redis-cluster | awk '{print $1,$6}' > data.txt")

    # 构建命令
    code = "docker run --rm -it --network fire-hydrant-redis-cluster_redis-net docker.dev.shoogoome.com/firehydrant/redis-cluster-manage:1.0 create --replicas 1 "
    if env != "online":
        for _, v in containers.items():
            try:
                num = re.findall('redis(\w)\.', v['Name'])[0]
                code += " {}:700{}".format(
                    v['IPv4Address'].split('/')[0], num)
            except:
                pass
    else:
        code = "cd " + work_dir + "/devops; ./cluster.sh `kubectl get pod -n fire-hydrant | grep redis-cluster-deloyment1 | awk '{print $1}'` "
        with open('data.txt', 'r') as fp:
            for i in range(6):
                n = fp.readline()
                code += ' {}:700{}'.format(n.split(' ')[-1].strip('\n'), n.split('-')[4][-1])
        code += " > " + work_dir + "/node.txt"
    print(code)
    # return
    os.system(code)
    # 修改系统配置文件
    time.sleep(5)
    if env != 'online':
        os.system('docker run --rm -it --network fire-hydrant-redis-cluster_redis-net inem0o/redis-trib info redis1:7001 | cut -d : -f 2 | cut -d @ -f 1 > node.txt')
    fp = open('node.txt', 'r')
    fy = open(config_dir, 'r')
    config = yaml.load(fy)
    fy.close()

    if env == "online":
        nodes = fp.read()
        ips = re.findall('Adding replica (\d+\.\d+\.\d+\.\d+:\d+) to (\d+\.\d+\.\d+\.\d+:\d+)', nodes)

    for i in range(1, 4):
        node = fp.readline() if env != "online" else ips[i - 1][1][-4:]
        config['redis-cluster']['masters' + str(i)]['host'] = 'localhost' if env != "online" else "fire-hydrant-redis-cluster-service" + str(node[3])
        config['redis-cluster']['masters' + str(i)]['port'] = int(node[:4])
    fp.close()

    with open(config_dir, 'w') as fp:
        yaml.dump(config, fp)

    os.system('rm -rf data.json node.txt data.txt')

if __name__ == '__main__':
    cluster()

