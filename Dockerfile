FROM python AS dev

RUN mkdir app

COPY ./requirements.txt /app

WORKDIR /app

RUN pip install -r requirements.txt

ARG DATABASE__CREATE=False

ENV FLASK_ENV=development \
    REDIS_URL=redis \
    DATABASE__USER=postgres_development \
    DATABASE__PWD=dbs_development \
    DATABASE__HOST=postgres_development:5432 \
    DATABASE__DBS=text_classification_development \
    DATABASE__CREATE=$DATABASE__CREATE

EXPOSE 5000

CMD ["python", "-m", "run"]

# Production image with different env values
FROM dev AS prod

ARG DATABASE__CREATE=False

ENV FLASK_ENV=production \
    REDIS_URL=redis \
    FLASK_PORT=8000 \
    DATABASE__USER=postgres_production \
    DATABASE__PWD=dbs_production \
    DATABASE__HOST=postgres_production:5432 \
    DATABASE__DBS=text_classification_production \
    DATABASE__CREATE=$DATABASE__CREATE

CMD  ["celery",  "-A", "celery_worker.celery worker",  "-l", "INFO"]