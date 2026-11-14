#!/usr/bin/env bash
set -euo pipefail

export RUN_ANSIBLE_NO_SSH="${RUN_ANSIBLE_NO_SSH:-1}"
export BAO_ADDR="${SECRET_STORE_ADDR:-${BAO_ADDR:-}}"
export ANSIBLE_INVENTORY="${ANSIBLE_INVENTORY:-localhost,}"
export RUN_ANSIBLE_CHECKOUT_GUARD="${RUN_ANSIBLE_CHECKOUT_GUARD:-1}"
export RUN_ANSIBLE_LOG_DIR="${RUN_ANSIBLE_LOG_DIR:-.ansible-run-logs}"
export RUN_ANSIBLE_RECAP_CHECK="${RUN_ANSIBLE_RECAP_CHECK:-1}"
export RUN_ANSIBLE_REQUIRE_RECAP="${RUN_ANSIBLE_REQUIRE_RECAP:-1}"

# renovate: datasource=github-releases depName=jpe-ansible/homelab-contracts
HOMELAB_CONTRACTS_REF=v5.66.0
exec nix run "github:jpe-ansible/homelab-contracts/${HOMELAB_CONTRACTS_REF}#run-ansible" -- "$@"
