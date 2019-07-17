#!/bin/bash

# 环境变量初始化
ENV="dev"
SYSTEM_PASSWORD="FireHydrant19.7**com"
IMAGE_ROOT_NAME="docker.dev.shoogoome.com/firehydrant/"
if [ ! -z ${FIRE_HYRANT_ENV} ]; then
    if [ ${FIRE_HYRANT_ENV} == "online" ]; then
        ENV="online"
    fi
fi

cd ..
WORK_DIR=`pwd`

# 初始化系统hostname
init_hostname() {
    echo -e "
127.0.0.1 pma.firehydrant.server.com
127.0.0.1 rabbitmq.firehydrant.server.com
127.0.0.1 local.firehydrant.server.com
127.0.0.1 pma.fh.shoogoome.com
127.0.0.1 api.fh.shoogoome.com
127.0.0.1 rabbitmq.fh.shoogoome.com" >> /etc/hosts
}

# 初始化系统日志路径
init_logs_dir() {
    mkdir -p ${WORK_DIR}'/logs/mysql'
    mkdir -p ${WORK_DIR}'/logs/server'
    mkdir -p ${WORK_DIR}'/logs/server/backups'
    mkdir -p ${WORK_DIR}'/logs/server/server'
    mkdir -p ${WORK_DIR}'/logs/server/celery'
}

# 构建镜像
docker_image_build() {
    docker build -t ${IMAGE_ROOT_NAME}'redis-cluster:1.0' ${WORK_DIR}'/devops/redis-cluster'
    docker build -t ${IMAGE_ROOT_NAME}'mariadb:1.0' ${WORK_DIR}'/devops/mysql'
    docker tag phpmyadmin/phpmyadmin:latest ${IMAGE_ROOT_NAME}'phpmyadmin:1.0'
    docker build -t ${IMAGE_ROOT_NAME}'redis:1.0' ${WORK_DIR}'/devops/redis'
    docker tag rabbitmq:3.7-management ${IMAGE_ROOT_NAME}'rabbitmq:1.0'
    docker build -t ${IMAGE_ROOT_NAME}'server:1.0' ${WORK_DIR}'/devops/server'
    docker pull inem0o/redis-trib:latest
    docker tag inem0o/redis-trib:latest ${IMAGE_ROOT_NAME}'redis-cluster-manage:1.0'
    docker pull nginx:1.13
    docker_image_push
}

# 上传镜像
docker_image_push() {
    docker login --username fire --password FireHydrant19.7**com docker.dev.shoogoome.com
    docker push ${IMAGE_ROOT_NAME}'redis-cluster:1.0'
    docker push ${IMAGE_ROOT_NAME}'mariadb:1.0'
    docker push ${IMAGE_ROOT_NAME}'phpmyadmin:1.0'
    docker push ${IMAGE_ROOT_NAME}'redis:1.0'
    docker push ${IMAGE_ROOT_NAME}'rabbitmq:1.0'
    docker push ${IMAGE_ROOT_NAME}'server:1.0'
    docker push ${IMAGE_ROOT_NAME}'redis-cluster-manage:1.0'
    docker logout docker.dev.shoogoome.com

}

docker_image_pull() {
    docker login --username fire --password FireHydrant19.7**com docker.dev.shoogoome.com
    docker pull ${IMAGE_ROOT_NAME}'redis-cluster:1.0'
    docker pull ${IMAGE_ROOT_NAME}'mariadb:1.0'
    docker pull ${IMAGE_ROOT_NAME}'phpmyadmin:1.0'
    docker pull ${IMAGE_ROOT_NAME}'redis:1.0'
    docker pull ${IMAGE_ROOT_NAME}'rabbitmq:1.0'
    docker pull ${IMAGE_ROOT_NAME}'server:1.0'
    docker pull ${IMAGE_ROOT_NAME}'redis-cluster-manage:1.0'
    docker logout docker.dev.shoogoome.com
}

# 初始化本地环境变量
init_local_export() {
    # mariadb环境变量
    export FIRE_HYDRANT_MYSQL_CNF_DIR=${WORK_DIR}'/devops/mysql/my.cnf'
    export FIRE_HYDRANT_MYSQL_WORK_DIR=${WORK_DIR}'/mysql'
    export FIRE_HYDRANT_MYSQL_LOG_DIR=${WORK_DIR}'/logs/mysql'
    export FIRE_HYDRANT_MYSQL_ROOT_PASSWORD=${SYSTEM_PASSWORD}
    # redis环境变量
    export FIRE_HYDRANT_REDIS_WORK_DIR=${WORK_DIR}'/redis'
    # rabbitmq环境变量
    export FIRE_HYDRANT_RABBITMQ_WORK_DIR=${WORK_DIR}'/rabbitmq'
    export FIRE_HYDRANT_RABBITMQ_USERNAME=root
    export FIRE_HYDRANT_RABBITMQ_ROOT_PASSWORD=${SYSTEM_PASSWORD}
    # server环境变量
    export FIRE_HYDRANT_SERVER_WORK_DIR=${WORK_DIR}'/FireHydrant'
    export FIRE_HYDRANT_SERVER_LOG_DIR=${WORK_DIR}'/logs/server'
    export FIRE_HYDRANT_SERVER_CONF_DIR=${WORK_DIR}'/devops/server/config.yml'
    # redis-cluster环境变量
    export FIRE_HYDRANT_REDIS_CLUSTER_WORK_DIR=${WORK_DIR}'/redis-cluster'
    # web nginx 配置文件目录
    if [ ${ENV} == "dev" ]; then
        export FIRE_HYDRANT_WEB_CONF_DIR=${WORK_DIR}'/devops/web/firehydrant.dev.conf'
    else
        export FIRE_HYDRANT_WEB_CONF_DIR=${WORK_DIR}'/devops/web/firehydrant.online.conf'
    fi
}

# 系统运行环境
fire_system() {
    init_local_export
    if [ ${ENV} == "dev" ]; then
        if [ -z "`docker images | grep docker.dev.shoogoome.com/firehydrant/`" ]; then
            docker_image_build
        fi
        case ${1} in
            "up")
                echo -e "\n================       启动FireHydrant本地开发环境        ================\n"
                echo -e "================ 创建redis-cluster集群, 请对默认配置输入yes ================\n"
                export FIRE_HYDRANT_REDIS_CLUSTER_WORK_DIR=${WORK_DIR}'/redis-cluster'
                rm -rf ${FIRE_HYDRANT_REDIS_CLUSTER_WORK_DIR}
                for i in `seq 7001 7006`; do
                    mkdir -p ${FIRE_HYDRANT_REDIS_CLUSTER_WORK_DIR}/${i}/data
                done
                docker stack deploy --compose-file ${WORK_DIR}'/devops/redis-cluster/docker-stack.yml' 'fire-hydrant-redis-cluster'
                sleep 5s
                python3 ${WORK_DIR}'/devops/redis-cluster/cluster.py'
            ;;
            "down")
                docker stack rm 'fire-hydrant-redis-cluster'
            ;;
        esac
        docker-compose -f ${WORK_DIR}'/devops/docker-compose.yml' ${@}
    else
        case $1 in
            "up")
                echo -e "\n================ 启动FireHydrant线上环境 ================\n"
                cd devops
                docker_image_pull
                helm install \
                --username fire --password ${SYSTEM_PASSWORD} \
                --ca-file ${WORK_DIR}'/devops/firehydrant/cert/ca.crt' \
                --key-file ${WORK_DIR}'/devops/firehydrant/cert/tls.key' \
                --cert-file ${WORK_DIR}'/devops/firehydrant/cert/tls.crt' \
                --version 1.0.0 --name fire \
                --set FIRE_HYDRANT_MYSQL_WORK_DIR=${FIRE_HYDRANT_MYSQL_WORK_DIR} \
                --set FIRE_HYDRANT_MYSQL_ROOT_PASSWORD=${FIRE_HYDRANT_MYSQL_ROOT_PASSWORD} \
                --set FIRE_HYDRANT_RABBITMQ_WORK_DIR=${FIRE_HYDRANT_RABBITMQ_WORK_DIR} \
                --set FIRE_HYDRANT_RABBITMQ_USERNAME=${FIRE_HYDRANT_RABBITMQ_USERNAME} \
                --set FIRE_HYDRANT_RABBITMQ_ROOT_PASSWORD=${FIRE_HYDRANT_RABBITMQ_ROOT_PASSWORD} \
                --set FIRE_HYDRANT_REDIS_WORK_DIR=${FIRE_HYDRANT_REDIS_WORK_DIR} \
                --set FIRE_HYDRANT_SERVER_WORK_DIR=${FIRE_HYDRANT_SERVER_WORK_DIR} \
                --set FIRE_HYDRANT_SERVER_LOG_DIR=${FIRE_HYDRANT_SERVER_LOG_DIR} \
                --set FIRE_HYDRANT_SERVER_CONF_DIR=${FIRE_HYDRANT_SERVER_CONF_DIR} \
                --set FIRE_HYDRANT_WEB_CONF_DIR=${FIRE_HYDRANT_WEB_CONF_DIR} \
                firehydrant/firehydrant
                cd ..
            ;;
            "down")
                helm del --purge fire
            ;;
            "exec")
                kubectl exec -it `kubectl get pod -n fire-hydrant | grep $2 | awk '{print $1}' ` bash
            ;;
            "manage")
                kubectl exec `kubectl get pod -n fire-hydrant | grep server | awk '{print $1}' ` python3 /firehydrant/manage.py ${@:2}
            ;;
        esac
    fi
}

case $1 in
    "up")
        fire_system up -d
    ;;
    "down")
        echo -e "\n================ 关闭FireHydrant环境 ================\n"
        fire_system down
    ;;
    "alldown")
        echo -e "\n================ 关闭FireHydrant环境 ================\n"
        fire_system alldown
    ;;
    "build")
        echo -e "\n================ 构建FireHydrant环境所需镜像 ================\n"
        docker_image_build
    ;;
    "manage")
        fire_system manage ${@:2}
    ;;
    "restart")
        fire_system down
        fire_system up -d
    ;;
    "bash")
        fire_system exec $2 bash
    ;;
    "update")
        # 从Jenkins获取当前构建分支
        git fetch origin ${BRANCH_NAME}
        git merge origin/${BRANCH_NAME}
        fire_system manage migrate
    ;;
    "push")
        helm push \
        --username fire --password ${SYSTEM_PASSWORD} \
        --ca-file ${WORK_DIR}'/devops/firehydrant/cert/ca.crt' \
        --key-file ${WORK_DIR}'/devops/firehydrant/cert/tls.key' \
        --cert-file ${WORK_DIR}'/devops/firehydrant/cert/tls.crt' \
        ${WORK_DIR}'/devops/firehydrant' firehydrant
    ;;
    "pull")
        docker_image_pull
    ;;
    "init")
        init_hostname
        init_logs_dir
        helm repo add firehydrant https://docker.dev.shoogoome.com/chartrepo/firehydrant \
        --username fire --password ${SYSTEM_PASSWORD} \
        --ca-file ${WORK_DIR}'/devops/firehydrant/cert/ca.crt' \
        --key-file ${WORK_DIR}'/devops/firehydrant/cert/tls.key' \
        --cert-file ${WORK_DIR}'/devops/firehydrant/cert/tls.crt'
        helm repo update
    ;;
esac
