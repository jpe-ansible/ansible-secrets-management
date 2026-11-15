# ansible-secrets-management

Ansible collection `dryvist.secrets_management` for OpenBao server install and Raft cluster
bootstrap, AppRole and policy sync, secret rotation, TOTP and admin-group bootstrap, the
Authelia role, and the OpenBao voter-health role.

[![CI Gate][ci-badge]][ci-workflow] [![License: Apache-2.0][license-badge]][license]

## Installation

`requirements.yml` lists the collection dependencies. The `openbao` role consumes the
`llm_router_key_catalog` role from the `dryvist.homelab` collection, following its v5 major tag.
The `authelia` role seeds its service secrets through the shared
`dryvist.homelab.openbao_secrets` role pinned in `requirements.yml`.

```sh
ansible-galaxy install -r requirements.yml --force
```

## Usage

Consume a role by its fully qualified name, for example `dryvist.secrets_management.openbao`.
Each role's README and defaults files list the inputs that the role reads.

## Consumer inputs

The roles read these names from the consuming playbook, inventory, or environment:

- Inventory groups `openbao_group` and `traefik_group`.
- `tofu_data`, a mapping with the keys `domain`, `ingress_vip`, and `constants`
  (`service_ports`, `ai_log_routing`).
- `ingress_domain`.
- The `PROXMOX_SUBDOMAIN` environment variable.
- `bao_apps_secrets`, a keyed secret map.
- `bao_postgres_backup_s3_secrets`, a keyed secret map.

## Roles

| Role | Purpose |
| --- | --- |
| `openbao` | Installs and configures an OpenBao Raft cluster member, then provisions the KV mount, secret hierarchy, policies, and AppRoles. |
| `authelia` | Configures the Authelia SSO provider and seeds its service secrets into OpenBao. |
| `openbao_voter_health` | Samples each Raft voter's health endpoints and sends one event per voter per cycle. |

## Layout

The collection root is the repository root: `galaxy.yml`, `roles/`, `playbooks/`,
`molecule/`, and `tests/` sit at the top level.

## Checks

- `pre-commit run --all-files` runs ansible-lint (production profile), yamllint,
  markdownlint, and gitleaks.
- `molecule test -s openbao` runs the openbao scenario in a privileged Debian container.
  CI runs it.
- `molecule test -s openbao_voter_health` converges only the openbao_voter_health role in the
  same container and checks its timer. CI runs it.
- `pytest` runs the test modules under `tests/`.
- `ansible-playbook -e render_tmp=<dir> tests/template_render/verify/<file>.yml` runs one
  template-render check.

## Releases

release-please (simple type) maintains `CHANGELOG.md`. `VERSION` and the `version` key in
`galaxy.yml` move together; the `x-release-please-version` marker on that line lets
release-please update it.

## Contributing

Open a pull request against `develop`. Run `pre-commit run --all-files` before pushing.

## License

Apache-2.0. See [LICENSE][license].

---

[docs.jacobpevans.com](https://docs.jacobpevans.com)

[ci-badge]: https://github.com/jpe-ansible/ansible-secrets-management/actions/workflows/ci-gate.yml/badge.svg
[ci-workflow]: https://github.com/jpe-ansible/ansible-secrets-management/actions/workflows/ci-gate.yml
[license-badge]: https://img.shields.io/badge/license-Apache--2.0-blue.svg
[license]: LICENSE
