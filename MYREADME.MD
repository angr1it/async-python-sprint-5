# Запуск

## Тесты

```
docker compose --profile test up -d --build
docker compose run test pytest
```

## Приложение

```
docker compose --profile dev up
```

Приложение доступно на:
http://localhost/api/docs#/
