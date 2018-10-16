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

```
pipenv run celery -A social_manager worker
```
