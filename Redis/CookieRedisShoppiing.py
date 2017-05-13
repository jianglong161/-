import redis
##使用reids实现购物车
def add_to_cart(conn,session,item,count):
    conn = redis.Redis(host='192.168.31.132 ', port=6379, db=0)
    if count<=0:
        conn.hrem('cart:'+session,item)
    else:
        conn.hset('cart:'+session,item,count)