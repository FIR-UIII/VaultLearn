ui = true
cluster_addr = "http://192.168.100.5:8201"
cluster_name = "dev_cluster"
api_addr = "http://192.168.100.5:8200"
disable_mlock = true
log_level = "debug"

storage "postgresql" {
    connection_url = "postgresql://vault:strongpassword@database:5432/vault"
    ha_enabled = "true"
    ha_table = "vault_ha_locks"
}

listener "tcp" {
    address = "0.0.0.0:8200"
    tls_disable = true
}
