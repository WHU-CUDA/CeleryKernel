nohup celery -A kernel worker -n kernel@%h -l INFO -P eventlet -Q kernel &
nohup python3 ./kernel/tasks.py &