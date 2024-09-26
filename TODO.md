# TASKS:
#0. Bugfix or typo issues
[+] #0.1. Fix init of create_acl_policy() enable_userpass_auth() create_user_userpass(). Need to add param inside func
[+] #0.2. Remove secrets into .env
[+] #0.3. Make app modular
#0.4. __init__.py file for packages
#0.5. TLS and cert errors
#0.6. add hash of project of sha256sum
#0.7. jwt.py Error: 'Client' has no attribute 'resolve_path'
[+] #0.8. hide secret in console

#1. Authentification
[+] #1.1. Approle
[+] #1.2. Userpass 
#1.3. TLS certificate [login error]
#1.4. LDAP 
[+] #1.5. JWT AuthMethod
#1.6. Gitlab JWT

#2. SecretEngine
[+] #2.1. KV SecretEngine v2
#2.1.1. добавить функционал проверки активации движка и его активацию
#2.2. Database
    Собрать докер сеть и БД в ней + подготовить БД и пользователя
#2.3. LDAP
#2.4. Transit
#2.5. PKI

#3. Integration
#3.1. Agent
[+] #3.2. SDK python hvac library
#3.3. Sidecar

#4. Key management + PKI
#4.1. X.509 cert rotation
#4.2. secret rotation

#5. Token
[+] #5.1. Wrapping/unwrapping a token
#5.2. token management https://hvac.readthedocs.io/en/stable/usage/auth_methods/token.html#token-management

#6. Feature
#6.1. seal/unseal
#6.2. vault as OIDC Provider

#7. K8S https://github.com/ducmeit1/vault-agent-tutorial