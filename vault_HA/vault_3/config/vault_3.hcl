api_addr = "https://192.168.100.4:9200"
cluster_addr = "https://192.168.100.4:9201"
ui = true
disable_mlock = "true"

listener "tcp" {
  address = "[::]:9200"
  tls_disable = false
  tls_ca_cert_file = "/certs/vault-ca-cert.pem"
  tls_cert_file = "/certs/vault-3-cert.pem"
  tls_key_file  = "/certs/vault-3-key.pem"
}

storage "raft" {
  path    = "/vault/data"
  node_id = "vault_3"

  retry_join {
    leader_tls_servername   = "vault_1"
    leader_api_addr         = "https://192.168.100.2:9200"
    leader_ca_cert_file     = "/certs/vault-ca-cert.pem"
    leader_client_cert_file = "/certs/vault-3-cert.pem"
    leader_client_key_file  = "/certs/vault-3-key.pem"
  }
  retry_join {
    leader_tls_servername   = "vault_2"
    leader_api_addr         = "https://192.168.100.3:9200"
    leader_ca_cert_file     = "/certs/vault-ca-cert.pem"
    leader_client_cert_file = "/certs/vault-3-cert.pem"
    leader_client_key_file  = "/certs/vault-3-key.pem"
  }
  retry_join {
    leader_tls_servername   = "vault_3"
    leader_api_addr         = "https://192.168.100.4:9200"
    leader_ca_cert_file     = "/certs/vault-ca-cert.pem"
    leader_client_cert_file = "/certs/vault-3-cert.pem"
    leader_client_key_file  = "/certs/vault-3-key.pem"
  }
}
