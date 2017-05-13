import redis
import os
##处理新日志的函数
def process_log(conn, path, callback):
    conn = redis.Redis(host='192.168.31.132 ', port=6379, db=0)
    #获取文件的处理进度
    current_file,offset=conn.mget('progress:file','progress:position')
    pipe=conn.pipeline();

    #通过使用闭包来减少重复代码
    def update_progress():
        pipe.mset({
            'progress:file':fname,
            'progress:position:':offset
        })
        pipe.execute()
    #有序的遍历各个日志文件
    for fname in sorted(os.listdir(path)):
        if fname<current_file:
            continue
        inp=open(os.path.join(path, fname),'rb')
        #处理一个因为系统崩溃而未完成处理日志文件时，略过已经处理的内容
        if fname==current_file:
            inp.seek(int(offset,10))
        else:
            offset=0
        current_file=None
        #枚举函数遍历一个由文件行组成的序列，并返回任意多个二元组
        #每个二元组包含了行号lno和行数据line，其中行号从0开始
        for lno,line in enumerate(inp):
            callback(pipe,line)
            offset+=int(offset)+len(line)#更新已经偏移的内容

            if not (lno+1)%1000:
                update_progress()
        update_progress()
        inp.close()
