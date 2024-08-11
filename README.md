# Installation
```
1. Create a self-signed vault certificate and key with configuration `selfsigned.cfr`
openssl req -x509 -batch -nodes -newkey rsa:2048 -keyout vault.key -out vault.crt -config selfsigned.cfr -days 9999

2. Add self-signed client certificate to host's OS CA trusted root
For Windows:
    a. Convert to DER: openssl x509 -outform der -in vault.crt -out vault_win.crt
    b. Open MMS: run > mms > CTRL+M > certificates > Action > Import to trusted Root Certs
For MAC:

3. (optional) Create a client certificate and key - for mTLS and cert authentication
openssl genrsa -out client.key 2048
openssl req -new -key client.key -out client.csr
openssl x509 -req -in client.csr -signkey client.key -out client.crt

4. Run vault via docker 
docker-compose -f docker-compose-tls.yml up -d

5. Init and Unseal
### docker CLI 
$ vault operator init
$ vault operator unseal
$ vault status
    Initialized.......true
    Sealed............false

6. Export token to ENV
bash$   export VAULT_TOKEN=hvs.[put_here]
bash$   export VAULT_URL=https://localhost:9200
PS>     $env:VAULT_TOKEN="hvs.[put_here]"
PS>     $env:VAULT_URL="https://localhost:9200"
```

# Project info
[userpass](media/userpass.svg)
```
1. RUN userpass.py
2. OUTCOME:
    [info] Checking enviroment setup
    [info] Checking vault availability
    [info] vault is running: True 
    [info] vault sealed: False
    [+] vault is ready
    [+] active policies: ['default', 'kv-read-policy', 'root']
    [info] userpass is enable
    [info] skipping enabling auth method
    [+] New user 'test' created with policy 'kv-read-policy'
    [+] Successfully get token: hvs.<your_token> with policies: ['default', 'kv-read-policy']
    [info] trying create secret test_value_name with token hvs.<your_token> to kv
    [+] Secret created
    [+] Secret is: path "kv": value is "DEMO_SECRET"
```
[AppRole](media/AppRole.svg)
```
1. RUN approle.py
2. OUTCOME:
    [info] Checking enviroment setup
    [info] Checking vault availability
    [info] vault is running: True 
    [info] vault sealed: False
    [+] vault is ready
    [+] active policies: ['default', 'kv-read-policy', 'root']
    [info] approle is enable
    [info] skipping enabling auth method
    [+] New role 'test_approle' created with policy 'kv-read-policy'
    [info] the role ['test_approle'] is created
    [+] Success: secret id <your_secret_id>
    [+] Success: role id <your_role_id>
    [+] Successfully get token: hvs.<your_token> with policies: ['default', 'kv-read-policy']
    [info] trying create secret DEMO_APPROLE with token hvs.<your_token> to v1
    [+] Secret created
    [+] Secret is: path "v1": value is "DEMO_SECRET"
```

[Approle with wrapped token](media/AppRole_wrapped.svg)
```
1. RUN approle+wrapped.py
2. OUTCOME:
    [info] Checking enviroment setup
    [info] Checking vault availability
    [info] vault is running: True 
    [info] vault sealed: False
    [+] vault is ready
    [+] active policies: ['default', 'kv-read-policy', 'root']
    [info] approle is enable
    [info] skipping enabling auth method
    [+] New role 'test_approle' created with policy 'kv-read-policy'
    [info] the role ['test_approle'] was created before
    [+] Success: role id <your_role_id>
    [+] Success: accessor for wrapped secret id <your_token_accessor>
    [+] Success: unwrapped secret <your_secret_id>
    [+] Successfully get token: hvs.<your_token> with policies: ['default', 'kv-read-policy']
    [info] trying create secret DEMO_APPROLE_WRAPPED with token hvs.<your_token> to v1
    [+] Secret created
    [+] Secret is: path "v1": value is "DEMO_SECRET"
```