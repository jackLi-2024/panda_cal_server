
source ~/.bash_profile
# source conf/python.conf 

if [ ! -d log ];
then
    mkdir log
fi

# 1.0 start celery worker.
#nohup python -m celery -A src.task worker --loglevel=info -f ./log/celery.log &

#if [ $? -ne 0 ];
#then
#    echo "[ERROR] start celery worker failed."
#    exit -1
#else
#    echo "[INFO] start celery worker ok."
#fi

# 2.0 start web api
nohup uwsgi config.ini  &
if [ $? -ne 0 ];
then
    echo "[ERROR] start uwsgi server failed."
    exit -1
else
    echo "[INFO] start uwsgi server ok."
fi

echo "upload server is ready."
