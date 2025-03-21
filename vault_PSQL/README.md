Данная директория содержит манифест docker-compose для быстрого поднятия кластера vault PostgreSQL:
```sh
# Структура
|__postgresql 
|__vault_1 
|__vault_2
|__vault_3

# поднятие кластера
docker-compose -f docker-compose.yaml up -d --build

# check status
http://127.0.0.1:8200/v1/sys/health

# To to Docker in vault CLI
vault operator init -key-shares=1 -key-threshold=1

# unseal via UI
http://127.0.0.1:8200/

docker-compose down
```
