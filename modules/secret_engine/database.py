import hvac
import os
from hvac.api.secrets_engines import Database

APP = hvac.Client(url=os.environ.get("VAULT_URL"), verify=False, token=os.environ.get("VAULT_TOKEN"))

assert APP.is_authenticated(), "Failed to authenticate with Vault."

# ENV
database_config = {
'name': 'mydatabase',
'plugin_name': 'postgresql-database-plugin',
'allowed_roles': 'role-name',
'connection_url': 'postgresql://{username}:{password}@postgres:5432/postgres?sslmode=disable',
'username': 'myuser',
'password': 'mypassword'
}

# Step 1: Enable Database Secrets Engine
def enable_database_secrets():  
    if APP.sys.list_mounted_secrets_engines()['database/'] is None:
        print('[start] Step 1: Enable Database Secrets Engine')
        try:
            APP.sys.enable_secrets_engine(
            backend_type='database',
            path='database'
            )
            print('[+] Success: Database Secrets Engine is enabled [1]')
        except Exception as e:
            print(f'[-] Error: {e}')
    else:
        print('[+] Success: Database Secrets Engine is enabled [2]')


# Step 2: Configuring database 
def configure_database(database_config):
    ''''Note: The database needs to be created and available to connect before you can configure 
    the database secrets engine using the above configure method'''
    print('[start] Step 2: Configuring database')
    try:
        Database.configure(APP,
                        name=database_config['name'],
                        plugin_name=database_config['plugin_name'],
                        allowed_roles=database_config['allowed_roles'],
                        connection_url=database_config['connection_url'],
                        username=database_config['username'],
                        password=database_config['password'],
                        )
    except Exception as e:
        print(f'[-] Error configuring database: {e}')

# Starting point
if __name__ == '__main__':
    enable_database_secrets()
    configure_database(database_config)