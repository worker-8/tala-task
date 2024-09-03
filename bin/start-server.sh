source env/bin/activate
# this will set the defa"ult backoffice port to 5000 and can be overwritten
gunicorn_port=${1:-"5000"}
# by default gunicorn will start with 2 workers
workers=${2:-"1"}

gunicorn \
    --bind 0.0.0.0:$gunicorn_port \
    --workers $workers \
    "server:app"