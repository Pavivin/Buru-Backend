FROM python:3.10

ENV PYTHONUNBUFFERED 1

RUN mkdir -p /app/src /config
WORKDIR /app/src

COPY config/requirements.txt /config/
RUN pip install -U pip && pip install -r /config/requirements.txt

COPY VERSION /app
COPY alembic.ini /app
COPY alembic /app/alembic
COPY src /app/src
COPY setup.cfg setup.py /app/

RUN cd /app && pip install .
ENV PYTHONPATH=/app/src

EXPOSE 8000

CMD ["uvicorn", "entrypoints.api:app", "--host", "0.0.0.0", "--port", "8000", "--no-access-log"]
