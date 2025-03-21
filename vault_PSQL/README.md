Данная директория содержит манифест docker-compose для быстрого поднятия кластера vault PostgreSQL:

|Имя пода    | IP адрес      |
|------------| ------------- |
| postgresql | 192.168.100.2 |
| vault_1    | 192.168.100.5 |
| vault_2    | 192.168.100.3 |
| vault_3    | 192.168.100.4 |

```sh
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
