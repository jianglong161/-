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
    conn.hset('login:',token, user) #维持令牌与用户之间的映射
    conn.zadd('recent',token,timestamp)    #记录令盘出现的最后时间
    if item:
        conn.zadd('view:'+token,item,timestamp) #记录用户浏览过的产品
        conn.zremrangebyrank('view:'+token,0,-26)# 移除旧的记录只保存用户浏览过26个产片

