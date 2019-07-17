# coding=utf-8

import sys

path_of_current_dir = "/firehydrant"

# sys.path.insert(0, path_of_current_dir)

worker_class = 'sync'
workers = 1

chdir = path_of_current_dir

worker_connections = 1000
timeout = 30
max_requests = 2000
graceful_timeout = 30

loglevel = 'debug'

reload = True
debug = True

bind = "%s:%s" % ("0.0.0.0", 80)

log_path = "/logs/server"
errorlog = '%s/server_debug.log' % log_path
accesslog = '%s/server_access.log' % log_path