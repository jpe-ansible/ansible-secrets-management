# openbao

The role installs [OpenBao](https://openbao.org/) as a native binary on Debian,
runs it as a Raft HA cluster with static-key auto-unseal, initializes the
cluster on its bootstrap host, and converges the declared policies, AppRoles
and secrets-engine configuration.

## Installation

The role ships in this collection under `roles/openbao/`. Reference it from a
play that targets `openbao_group`:

```yaml
- hosts: openbao_group
  become: true
  roles:
    - role: openbao
```

## Usage

```sh
ansible-playbook playbooks/site.yml --tags openbao
```

[Installation and usage](docs/installation-and-usage.md) lists the inputs,
tags, selective runs, restart order, and first-run behavior.

Org-secrets and org-variables sets find installations by org name; adding an org to these sets requires one catalog entry.
