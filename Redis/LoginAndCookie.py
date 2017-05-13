import  redis
import time

def check_toke(conn,token):
    conn = redis.Redis(host='192.168.31.132 ', port=6379, db=0)
    return conn.hget('login',token) #尝试获取并返回令牌对应的用户
##
##程序更新令牌的方法
def update_toke(conn,token,user,item=None):
    conn = redis.Redis(host='192.168.31.132 ', port=6379, db=0)
    timestamp=time.time()
    conn.hset('login:',token, user) #
    conn.zadd('recent',token,timestamp)

