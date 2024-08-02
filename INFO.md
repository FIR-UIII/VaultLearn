# Vault with FastAPI integration
hvac library

```
# Run vault 
docker compose -f docker-compose-vault.yml up -d
  > check unseal key 
  > root key

# Go to Vault CLI
docker exec -it vault /bin/sh
  > $ export # to see env variables (VAULT_ADDR='http://127.0.0.1:8200', VAULT_DEV_LISTEN_ADDRESS='0.0.0.0:8200' VAULT_DEV_ROOT_TOKEN_ID='test')
  > $ vault login test

# Stop vault 
docker compose -f docker-compose-vault.yml down

# Run app
uvicorn main:app --reload
```