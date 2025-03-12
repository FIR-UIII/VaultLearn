# Запуск vault в docker в режиме HA
Структура:
vault_1 – IP 192.168.100.2
vault_2 – IP 192.168.100.3
vault_3 – IP 192.168.100.4

### Шаг 1 подготовить TLS сертификаты
```bash
# 1 Выпускаем корневой CA сертификат
openssl genrsa 2048 > vault-ca-key.pem
openssl req -new -x509 -nodes -days 3650 -key vault-ca-key.pem -out vault-ca-cert.pem

# 2 Создать конфигурационные файлы (ниже пример для ноды vault_1)
    [req]
    distinguished_name = req_distinguished_name
    x509_extensions = v3_req
    prompt = no

    [req_distinguished_name]
    C = US
    ST = state
    L =  city
    O = company
    CN = *

    [v3_req]
    subjectKeyIdentifier = hash
    authorityKeyIdentifier = keyid,issuer
    basicConstraints = CA:TRUE
    subjectAltName = @alt_names

    [alt_names]
    DNS.1 = vault_1
    IP.1 = 192.168.100.2
    IP.2 = 127.0.0.1

# 3 Создать запрос на подписание CSR
openssl req -newkey rsa:2048 -nodes -keyout vault-1-key.pem -out vault-1-csr.pem -subj "/CN=vault_1"
openssl req -newkey rsa:2048 -nodes -keyout vault-2-key.pem -out vault-2-csr.pem -subj "/CN=vault_2"
openssl req -newkey rsa:2048 -nodes -keyout vault-3-key.pem -out vault-3-csr.pem -subj "/CN=vault_3"

# 4 Выпустить подписанные сертификаты
openssl x509 -req -set_serial 01 -days 3650 -in vault-1-csr.pem -out vault-1-cert.pem -CA vault-ca-cert.pem -CAkey vault-ca-key.pem -extensions v3_req -extfile ./selfsigned_v1.cfr
openssl x509 -req -set_serial 01 -days 3650 -in vault-2-csr.pem -out vault-2-cert.pem -CA vault-ca-cert.pem -CAkey vault-ca-key.pem -extensions v3_req -extfile ./selfsigned_v2.cfr
openssl x509 -req -set_serial 01 -days 3650 -in vault-3-csr.pem -out vault-3-cert.pem -CA vault-ca-cert.pem -CAkey vault-ca-key.pem -extensions v3_req -extfile ./selfsigned_v3.cfr

# 5 По итогу должно получиться по 3 для каждого узла + корневой сертификат

# 6 Копируем их в директории для сертификатов vault_N/certs каждой ноды и корневой vault-ca-cert.pem. На примере vault_1, должно получиться так:
Каталог: C:\Users\Admin\Desktop\Project\vault_dev\vault_1\certs
Mode                 LastWriteTime         Length Name
----                 -------------         ------ ----
-a----        12.03.2025      9:53           1192 vault-1-cert.pem
-a----        12.03.2025      9:53            887 vault-1-csr.pem
-a----        12.03.2025      9:53           1704 vault-1-key.pem
-a----        12.03.2025      9:53           1245 vault-ca-cert.pem
```

### Шаг 2. Проверка конфигурации vault и запуск docker compose
```bash
# vault_1\config\vault_1.hcl
api_addr = "https://192.168.100.2:9200"
cluster_addr = "https://192.168.100.2:9201"
ui = true
disable_mlock = "true"

listener "tcp" {
  address = "[::]:9200"
  tls_disable = false
  tls_ca_cert_file = "/certs/vault-ca-cert.pem"
  tls_cert_file = "/certs/vault-1-cert.pem"
  tls_key_file  = "/certs/vault-1-key.pem"
}

storage "raft" {
  path    = "/vault/data"
  node_id = "vault_1"

  retry_join {
    leader_tls_servername   = "vault_1"
    leader_api_addr         = "https://192.168.100.2:9200"
    leader_ca_cert_file     = "/certs/vault-ca-cert.pem"
    leader_client_cert_file = "/certs/vault-1-cert.pem"
    leader_client_key_file  = "/certs/vault-1-key.pem"
  }
  retry_join {
    leader_tls_servername   = "vault_2"
    leader_api_addr         = "https://192.168.100.3:9200"
    leader_ca_cert_file     = "/certs/vault-ca-cert.pem"
    leader_client_cert_file = "/certs/vault-1-cert.pem"
    leader_client_key_file  = "/certs/vault-1-key.pem"
  }
  retry_join {
    leader_tls_servername   = "vault_3"
    leader_api_addr         = "https://192.168.100.4:9200"
    leader_ca_cert_file     = "/certs/vault-ca-cert.pem"
    leader_client_cert_file = "/certs/vault-1-cert.pem"
    leader_client_key_file  = "/certs/vault-1-key.pem"
  }
}

# Запуск docker compose
$ docker-compose up -d
Creating network "vault_dev_cluster_dev" with driver "bridge"
Creating vault_1 ... done
Creating vault_2 ... done
Creating vault_3 ... done
```

### Шаг 3. Инициализация волта
```bash
# 1. Заходим в консоль docker vault_1

vault_1$ vault status
Key                     Value
---                     -----
Seal Type               shamir
Initialized             false
Sealed                  true
Total Shares            1
Threshold               1
Unseal Progress         0/1
Unseal Nonce            n/a
Storage Type            raft
Removed From Cluster    false
HA Enabled              true

vault_1$ vault operator init -n=1 -t=1
>>> получаем секреты

vault_1$ vault operator unseal
>>> вводим unseal ключ

vault_1$ vault status
Key                     Value
---                     -----
Initialized             true
Sealed                  false

# 2. Далее на нодах vault_2 и vault_3 нужно сделать unseal. Важно - что статус Initialized = true, должен быть у всех
vault_2$ vault operator unseal
vault_3$ vault operator unseal

# 3. Далее на ноде vault_1 проходим аутентификацию и проверяем членов кластера vault и raft
vault_1$ vault login
>>> root token

vault_1$ vault operator members
Host Name       API Address                   Cluster Address               Active Node    Version    Upgrade Version    Redundancy Zone    Last Echo
---------       -----------                   ---------------               -----------    -------    ---------------    ---------------    ---------
2220406b4ec6    https://192.168.100.2:9200    https://192.168.100.2:9201    true           1.19.0     1.19.0             n/a                n/a
29e050cccf67    https://192.168.100.3:9200    https://192.168.100.3:9201    false          1.19.0     1.19.0             n/a                2025-03-12T09:23:42Z
6dfeca0ba7ec    https://192.168.100.4:9200    https://192.168.100.4:9201    false          1.19.0     1.19.0             n/a                2025-03-12T09:23:41Z

vault_1$ vault operator raft list-peers
Node       Address               State       Voter
----       -------               -----       -----
vault_1    192.168.100.2:9201    leader      true
vault_2    192.168.100.3:9201    follower    true
vault_3    192.168.100.4:9201    follower    true
```

На этом первоначальная настройка завершена. Можно проверить UI
