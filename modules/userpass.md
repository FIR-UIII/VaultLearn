1. Enable userpass authentication and create user
```
vault auth enable userpass
vault write auth/userpass/users/admin password=[put]
```

2. Create an ACL Policy for Token
Create file 
```sh
vi kv-read-policy.hcl
```
### or
```sh
tee kv-read-policy.hcl <<EOF
# Policy for kv engine 
path "secret/*" {
    capabilities = [ "create", "read", "update", "list" ]
}
EOF
```
Apply this policy using the Vault CLI:
```sh
vault policy write my-kv-read-policy kv-read-policy.hcl
```
3. Create a Token for Userpass Access
```sh
vault token create -policy=my-kv-read-policy -metadata="user=myuser"
```

4. Enable KV v2 Engine
```sh
vault secrets enable -version=2 kv
```
5. Update a Secret into KV v2 Engine Using API and Curl
```sh
curl \
    --header "X-Vault-Token: hvs..." \
    --request POST \
    --data '{"data": {"myname": "data"}}' \
    http://127.0.0.1:8200/v1/kv/data/data
```

6. Read the Secret from Step 5
```sh
curl \
    --header "X-Vault-Token: hvs..." \
    http://127.0.0.1:8200/v1/kv/data/data
```

## https://hvac.readthedocs.io/en/stable/source/hvac_api_auth_methods.html#