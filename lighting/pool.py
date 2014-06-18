from pip._vendor.requests.packages import urllib3

pool = urllib3.PoolManager(5)

def get_pool():
    return pool