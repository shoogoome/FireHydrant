
# 根目录
FIRE_HYDRANT_DATA_ROOT = "/firehydrant/data"

# ==========
# 模块目录

FIRE_HYDRANT_DATA_ACCOUNT = FIRE_HYDRANT_DATA_ROOT + "/accounts"

FIRE_HYDRANR_DATA_PRACTICE = FIRE_HYDRANT_DATA_ROOT + "/practice"

FIRE_HYDRANT_DATA_FACEC = FIRE_HYDRANT_DATA_ROOT + "/facec"

# ==========
# 模块子目录

# account
FIRE_HYDRANT_DATA_ACCOUNT_AVATOR = FIRE_HYDRANT_DATA_ACCOUNT + "/avator"

# facec
FIRE_HYDRANT_DATA_FACEC_ACCOUNT = FIRE_HYDRANT_DATA_FACEC + "/accounts"
FIRE_HYDRANT_DATA_FACEC_ACCOUNT_AVATOR = FIRE_HYDRANT_DATA_FACEC_ACCOUNT + "/avator"

# practice
FIRE_HYDRANR_DATA_PRACTICE_ACCOUNT = FIRE_HYDRANR_DATA_PRACTICE + "/accounts"
FIRE_HYDRANR_DATA_PRACTICE_ACCOUNT_AVATOR = FIRE_HYDRANR_DATA_PRACTICE_ACCOUNT + "/avator"

# 路由映射
STORAGE_MAPPING = {
    'account_avator': FIRE_HYDRANT_DATA_ACCOUNT_AVATOR,
    'facec_avator': FIRE_HYDRANT_DATA_FACEC_ACCOUNT_AVATOR,
    'practice_avator': FIRE_HYDRANR_DATA_PRACTICE_ACCOUNT_AVATOR,
}


MIME_TO_EXT_MAPPING = {
    'jpg': 'image/jpg',
    'jpeg': 'image/jpeg',
    'bmp': 'image/bmp',
    'png': 'image/png',
    'gif': 'image/gif',
    'svg': 'image/svg',
}

NGINX_RESOURCE_PATH = "/resource_internal"