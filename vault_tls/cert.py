import hvac
from hvac.api.auth_methods.cert import Cert
from init_vault import health_check, create_acl_policy, enable_auth_method
import urllib3

urllib3.disable_warnings() # disable warnings in logs - need to clear


cacert = "./certs/server.pem"
cert=("./certs/client-signed-cert.pem", "./certs/client-private-key.pem")


APP = hvac.Client(url="https://127.0.0.1:9200", token="hvs.7ZlguIL4WrFILfpc5fj3eq7e", verify=False, cert=cert)


### ENV
APP.token = 'hvs.7ZlguIL4WrFILfpc5fj3eq7e' # export token

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
    "certificate_file": "./certs/client-signed-cert.pem",
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
    try:
        Cert.login(
                    APP,
                    name=cert_role['name'],
                )
    except Exception as e:
        print(f"Caught an exception: {e}")
login_cert(cert_role)