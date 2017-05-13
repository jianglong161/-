import  redis
def test():
    r=redis.Redis(host='192.168.31.132 ',port = 6379, db = 0)
    r.set("s","sss")