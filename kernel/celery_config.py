from kombu import Queue
from kombu import Exchange
from datetime import timedelta
broker_url = 'redis://120.78.156.16:6789/0'

result_backend = 'redis://120.78.156.16:6789/1'

timezone = 'Asia/Shanghai'

# 导入指定任务模块
imports = (
    'kernel.run',
    'kernel.tasks'
)

beat_schedule = {
    'get_cpu_info_five_second': {
        'task': 'kernel.tasks.get_cpu_info',
        'schedule': timedelta(seconds=5),
        'args': ''
    },
    'get_gpu_info_five_second': {
        'task': 'kernel.tasks.get_gpu_info',
        'schedule': timedelta(seconds=5),
        'args': ''
    }
}
# ---------------------定义路由、交换、队列------------------------
task_queues = (
    Queue('default', exchange=Exchange('default'), routing_key='default'),
    Queue('kernel', exchange=Exchange('kernel'), routing_key='kernel')
)

task_routes = {
    'kernel.run.run': {'queue': 'kernel', 'routing_key': 'kernel'},
    'kernel.tasks.get_cpu_info':  {'queue': 'kernel', 'routing_key': 'kernel'},
    'kernel.tasks.get_gpu_info': {'queue': 'kernel', 'routing_key': 'kernel'},
}


# 一个生产者，多个消费者，每一个消费者都有自己的一个队列，生产者没有将消息直接发送到队列，
# 而是发送到了交换机，每个队列绑定交换机，生产者发送的消息经过交换机，到达队列，
# 实现一个消息被多个消费者获取的目的。需要注意的是，如果将消息发送到一个没有队列绑定的exchange上面，
# 那么该消息将会丢失

# 广播模式
# celery -A tasks worker -Q broadcast_tasks -l info -n worker2
# task_queues = (Broadcast('broadcast_tasks'),)
# task_routes = ([
#     ('tasks.add', {'queue': 'broadcast.add', 'exchange': 'broadcast_tasks'}),
#     ('tasks.multiply', {'queue': 'broadcast.multiply', 'exchange': 'broadcast_tasks'}),
# ],)
