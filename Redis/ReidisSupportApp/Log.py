##将最新日志记录到Reidis中
#设立一个字典，将大部分日志的安全级别映射到为字符窜
import logging
import redis
import time
import datetime
SEVERITY={
    logging.DEBUG:'debug',
    logging.INFO:'info',
    logging.WARNING:'waring',
    logging.ERROR:'error',
    logging.CRITICAL:'critical',
}
SEVERITY.update((name,name) for name in SEVERITY.values())
def log_recent(conn,name,message,serverity=logging.INFO,pipe=None):
    conn = redis.Redis(host='192.168.31.132 ', port=6379, db=0)
    #尝试将日志安全级别转换成简单的字符串
    serverity=str(SEVERITY.get(serverity,serverity)).lower()
    #负责创建存储消息的键
    destination='recent:%s:%s'%(name,serverity)
    #j将当前时间添加到消息里面，用于记录消息的发送时间
    message=time.asctime()+' '+message
    #使用流水线末将通信往返次数降低为一次
    pipe =pipe or conn.pipeline()
    #将消息添加到日志列表的最前面
    pipe.lpush(destination,message)
    pipe.itrim(destination,0,99)
    pipe.execute()


###
##展示了日志并轮换最常见日志消息的方法
def log_common(conn,name,message,servirty=logging.INFO,timeout=5):
    conn = redis.Redis(host='192.168.31.132 ', port=6379, db=0)
    #设置日志的安全界别
    servirty=str(SEVERITY.get(servirty,servirty)).lower()
    #负责存储近期常用日志的键
    destination = 'common:%s:%s'%(name,servirty)
    #因为程序每小时轮换一次，需要一个键来记录当前所处的小时数
    start_key=destination+':start'
    pipe=conn.pipeline()
    end=time.time()+timeout
    while time.time()<end:
        try:
            #对记录当前小时数的键进行监视，
            #确保轮换操作可以正常进行
            pipe.watch(start_key)
            #取得当前时间
            now = datetime.utcnow().timetuple()
            #取得当前所处的小时数
            hour_start=datetime(*now[:4]).isoformat()
            exitsting=pipe.get(start_key)
            #创建一个事物
            pipe.multi()
            if exitsting and exitsting <hour_start:
                pipe.rename(destination,destination+':last')
                pipe.rename(destination,destination+':pstart')
            elif not exitsting:
                pipe.set(start_key,hour_start)
            pipe.zincrby(destination,message)
            log_recent(pipe,name,message,start_key,pipe)
            return
        except redis.exception.WatchError:
            continue
