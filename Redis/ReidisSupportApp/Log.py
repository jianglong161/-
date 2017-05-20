##将最新日志记录到Reidis中
#设立一个字典，将大部分日志的安全级别映射到为字符窜
import logging
import redis
import time
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
