# Social Manager

## Start project

```
pipenv run python manage.py runserver
```

## Start Redis

```
docker run --name redis -p 6379:6379 -d redis
```

## Start Celery worker

### With beat

This command _only_ works if you need to start one worker. If you need multiple workers use the 'Without beat' command
and then run the command in 'Start Celery beat'.

```
pipenv run celery -B -A social_manager worker
```

### Without beat

```
pipenv run celery -A social_manager worker
```

## Start Celery beat

If you start the worker using the 'With beat' command, you don't need to start an external service. If you need to launch
more than one worker, you will need to start the beat service using:

```
pipenv run celery -A social_manager beat
```
