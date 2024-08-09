import hvac
import os
from hvac.api.auth_methods.cert import Cert
from init_vault import health_check, create_acl_policy, enable_auth_method
import urllib3

urllib3.disable_warnings() # disable warnings in logs - need to clear

APP = hvac.Client(url="https://127.0.0.1:9200", verify=False)

### ENV
APP.token = token=os.environ.get('VAULT_TOKEN')

policy = {
        'name': 'kv-read-policy',
        'policy': 'path "secret/*" { capabilities = [ "create", "read", "update", "list" ]}',
    }

auth_method = {
    "method_type": 'cert',
    "description": 'Enable TLS certificate authentification',
    "path": 'cert'
}

cert_role = {
    "name": "demo_certificate_role",
    "certificate_file": "/Users/artem/Projects/VaultLearn/vault_tls/certs/server.pem",
    "allowed_common_names": ["*"],
    "allowed_dns_sans": [],
    "allowed_email_sans": [],
    "allowed_uri_sans": [],
    "allowed_organizational_units": [],
    "required_extensions": ["basicConstraints", "keyUsage", "extendedKeyUsage", "subjectAltName"],
    "display_name": "Test CA Certificate Role",
    "token_ttl": 3600,
    "token_max_ttl": 7200,
    "token_policies": ["kv-read-policy"],
    "token_bound_cidrs": [],
    "token_explicit_max_ttl": 0,
    "token_no_default_policy": False,
    "token_num_uses": 0,
    "token_period": 0,
    "token_type": "service",
}

### Step 0: Initialization
health_check()

### Step 1: Create ACL policy
create_acl_policy(policy)

### Step 2: Enable cert authentification
enable_auth_method(auth_method)

### Step 3: Create CA Certificate Role
def create_ca_certificate_role(cert_role):
    print(f'[start] creating CA certificate role: {cert_role["name"]}')
    try:
        Cert.create_ca_certificate_role(APP,
                                    name=cert_role['name'],
                                    certificate_file=cert_role['certificate_file'],
                                    allowed_common_names="",
                                    allowed_dns_sans="",
                                    allowed_email_sans="",
                                    allowed_uri_sans="",
                                    allowed_organizational_units="",
                                    required_extensions="",
                                    display_name=cert_role['display_name'],
                                    token_ttl=0,
                                    token_max_ttl=0,
                                    token_policies=cert_role['token_policies'],
                                    token_bound_cidrs=[],
                                    token_explicit_max_ttl=0,
                                    token_no_default_policy=False,
                                    token_num_uses=0,
                                    token_period=0,
                                    token_type="",
                                    mount_point="cert",
    )
        print(f"[+] Success: cert role '{cert_role['name']}' created")
    except hvac.exceptions.InvalidPath:
        print("[-] Error: role already exists")
    except TypeError as e:
        print(f"[-] Error: {e}")

create_ca_certificate_role(cert_role)

### Step 4: Login and get token
def login_cert(cert_role):
    print(f'[start] login with cert role: {cert_role["name"]}')
    try:
        Cert.login(
                    APP,
                    name=cert_role['name'],
                    cacert='/Users/artem/Projects/VaultLearn/vault_tls/certs/server.pem',
                    cert_pem='/Users/artem/Projects/VaultLearn/vault_tls/certs/client-signed-cert.pem',
                    key_pem='/Users/artem/Projects/VaultLearn/vault_tls/certs/client-private-key.pem',
                )
    except Exception as e:
        if "certificate" in str(e):  # Check if the error message contains "certificate"
            print(f"[-] Error: {e}")
            # Handle the certificate authentication error here
            # For example, you can print a specific error message or retry the login process
        else:
            print(f"[-] Error: {e}")

login_cert(cert_role)