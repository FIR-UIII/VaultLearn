


# docker pull hashicorp/vault-agent
# docker run --rm -d --name vault-agent -p 8222:8200 -e VAULT_ADDR=http://127.0.0.1:8200 -e VAULT_TOKEN=demo_token hashicorp/vault-agent
# touch agent-config.hcl
# $ vault agent -config=/path/to/agent-config.hcl
# 