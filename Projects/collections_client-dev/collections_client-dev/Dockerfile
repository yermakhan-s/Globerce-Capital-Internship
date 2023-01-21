# Image for build packages
FROM python:3.9-alpine3.14 as build-python

ENV PYTHONUNBUFFERED 1

RUN apk update \
    && apk add --no-cache --virtual .build-deps \
    build-base \
    curl \
    postgresql-dev \
    libffi-dev \
    && curl -sSL https://raw.githubusercontent.com/python-poetry/poetry/master/get-poetry.py | POETRY_HOME=/opt/poetry python \
    && cd /usr/local/bin \
    &&  ln -s /opt/poetry/bin/poetry \
    && poetry config virtualenvs.create false \
    && poetry config virtualenvs.in-project false

# Copy poetry.lock* in case it doesn't exist in the repo
COPY ./pyproject.toml ./poetry.lock* /app/

WORKDIR /app/

# Allow installing dev dependencies to run tests
ARG DEV
ENV DEV ${DEV:-true}
RUN /bin/sh -c "if [ $DEV == 'true' ] ; then poetry install --no-root ; else poetry install --no-root --no-dev ; fi"


# use alpline image. final image
FROM python:3.9-alpine3.14

WORKDIR /app/

RUN addgroup --system collectinos_client \
    && adduser --no-create-home --system --ingroup collectinos_client collectinos_client

# copy dependens from build images
COPY --from=build-python /usr/local/lib/python3.9/site-packages/ /usr/local/lib/python3.9/site-packages/
COPY --from=build-python /usr/local/bin/ /usr/local/bin/
COPY --from=build-python /usr/lib/libldap_r-2.4.so.2 /usr/lib/liblber-2.4.so.2 /usr/lib/libpq.so.5 /usr/lib/libsasl2.so.3 /usr/lib/


COPY --chown=collectinos_client:collectinos_client . /app
USER collectinos_client

COPY --chown=collectinos_client:collectinos_client docker-entrypoint.sh /docker-entrypoint.sh
RUN chmod +x /docker-entrypoint.sh

ENV PYTHONUNBUFFERED 1
ENV PYTHONPATH /app:$PYTHONPATH

CMD ["/docker-entrypoint.sh"]
