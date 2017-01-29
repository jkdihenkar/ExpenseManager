
SERVER_APP='Server.py'
BIND_ADDR='0.0.0.0'
PORT=2678
PYTHON_BIN='python3.5'
REDIS_BIN='redis-server'

# make dir logs
mkdir -pv logs

# start redis
$REDIS_BIN --port 7781 >> logs/redis-stdout.log 2>&1 &

# start message sender service
$PYTHON_BIN db_libs/utils/mailsender_service.py >> logs/mailsender.stdout.log 2>&1 &

export FLASK_APP=Server.py
flask run --host $BIND_ADDR --port $PORT