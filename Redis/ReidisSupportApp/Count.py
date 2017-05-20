import  redis
import time
###更新计数器的方法
PRECISION=[1,5,60,300,3600,18000,86400]
def update_counter(conn,name, count=1,now=None):
    conn = redis.Redis(host='192.168.31.132 ', port=6379, db=0)
    #通过取得当前时间来判断应该对那个时间片执行自增记录
    now = now or time.time()
    pipe=conn.pipeline()
    #为了保证以后清理，创建一个事务型流水线
    for prec in PRECISION:
        #取得当前时间片的开始时间
        pnow=int(now/prec)*prec
        hash='%s:%s'%(prec,name)
        pipe.zadd('know:',hash,0)
        pipe.hincrby('count:'+hash,pnow,count)
    pipe.execute()

def get_count(conn,name , precision):
    conn = redis.Redis(host='192.168.31.132 ', port=6379, db=0)
    hash='%s:%s'%(precision,name)
    data=conn.hgetall('count:'+hash)
    to_return=[]
    for key,valaue in data.iteritems():
        to_return.append((int(key),int(valaue)))
        to_return.sort()
        return  to_return

