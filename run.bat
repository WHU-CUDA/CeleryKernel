conda activate celerytest
celery -A kernel worker -n kernel@%h -l INFO -P eventlet -Q kernel
python .\kernel\tasks.py