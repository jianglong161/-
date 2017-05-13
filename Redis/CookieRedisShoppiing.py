import redis
import time
##使用reids实现购物车
def add_to_cart(conn,session,item,count):
    conn = redis.Redis(host='192.168.31.132 ', port=6379, db=0)
    if count<=0:
        conn.hrem('cart:'+session,item) #从购物车里面删除指定商品
    else:
        conn.hset('cart:'+session,item,count)  #将指定产品增加到购物车里
##
QUIT=False
LIMIT=1000000
def clean_full_seesion(conn):
    conn = redis.Redis(host='192.168.31.132 ', port=6379, db=0)
    while not QUIT:
        size=conn.zcard('recent:')
        if size<=LIMIT:
            time.sleep(1)
            continue
        end_index=min(size-LIMIT,100)
        sessions=conn.zrange('recnet:',0,end_index-1)

        session_key=[]
        for sss in sessions:
            session_key.append('viewed:'+sss)
            session_key.append('cart:'+sss)

        conn.delete(*session_key)
        conn.hdel('longin:',*sessions)
        conn.zrem('recent:',*sessions)