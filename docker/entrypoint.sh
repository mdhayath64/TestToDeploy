#!/bin/bash

set -o errexit
set -o pipefail
set -o nounset

postgres_ready() {
    python << END
import sys

from psycopg2 import connect
from psycopg2.errors import OperationalError
import traceback
try:
    connect(
        dbname="${DJANGO_POSTGRES_DATABASE}",
        user="${DJANGO_POSTGRES_USER}",
        password="${DJANGO_POSTGRES_PASSWORD}",
        host="${DJANGO_POSTGRES_HOST}",
        port="${DJANGO_POSTGRES_PORT}",

    )
except OperationalError:
    traceback.print_exc()
    sys.exit(-1)
END
}


until postgres_ready; do
  >&2 echo "Waiting for PostgreSQL to become available..."
  sleep 5
done
>&2 echo "PostgreSQL is available"

python3 manage.py migrate
python3 manage.py collectstatic --noinput
# python manage.py createsuperuser --no-input
python3 manage.py initadmin

#echo "Celery okay!!"
celery -A ecommerce beat -l info --s celery/celerybeat-scheduler &
celery -A ecommerce worker -l error --pool=solo &

exec "$@"