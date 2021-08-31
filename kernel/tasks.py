import json
import os
import time

import pynvml
import psutil
import socket
from kernel import app
import redis

rds = redis.Redis("120.78.156.16", 6789, 0)


def get_gpu_info():
    pynvml.nvmlInit()
    count = pynvml.nvmlDeviceGetCount()
    res = []
    for gpu_id in range(0, count):
        if gpu_id < 0 or gpu_id >= pynvml.nvmlDeviceGetCount():
            print(r'gpu id {} 对应得显卡不存在！'.format(gpu_id))
            return res
        pynvml.nvmlInit()
        handler = pynvml.nvmlDeviceGetHandleByIndex(gpu_id)
        mem_info = pynvml.nvmlDeviceGetMemoryInfo(handler)
        name = pynvml.nvmlDeviceGetName(handler)
        total = round(mem_info.total / 1024 / 1024, 2)
        used = round(mem_info.used / 1024 / 1024, 2)
        free = round(mem_info.free / 1024 / 1024, 2)
        usage = round((mem_info.used / mem_info.total) * 100, 2)
        pynvml.nvmlShutdown()
        res.append({
            "name": str(name, encoding="utf-8"),
            "total": total,
            "used": used,
            "free": free,
            "usage": usage
        })

    return res


def get_cpu_mem_info():
    mem_total = round(psutil.virtual_memory().total / 1024 / 1024, 2)
    mem_free = round(psutil.virtual_memory().free / 1024 / 1024, 2)
    mem_used = round(psutil.virtual_memory().used / 1024 / 1024, 2)
    mem_process_used = round(psutil.Process(os.getpid()).memory_info().rss / 1024 / 1024, 2)
    return {
        'total': mem_total,
        'free': mem_free,
        'used': mem_used,
        'process_used': mem_process_used
    }


def get_cpu_info():
    cpu_count = psutil.cpu_count(logical=False)
    cpu_logic_count = psutil.cpu_count()
    cpu_usage = psutil.cpu_percent()
    print(r'CPU has {} cores and {} logical cores, usage: {}%'.format(cpu_count, cpu_logic_count, cpu_usage))
    return {
        'cores': cpu_count,
        'logical_counts': cpu_logic_count,
        'usage': cpu_usage
    }


@app.task
def all():
    hostname = socket.gethostname()
    data = {
        'gpu': get_gpu_info(),
        'cpu': get_cpu_info(),
        'mem': get_cpu_mem_info(),
        'hostname': 'kernel@' + hostname,
    }
    rds.setex(data['hostname'], 10, json.dumps(data))
    rds.save()


if __name__ == '__main__':
    while True:
        all()
        time.sleep(2)
