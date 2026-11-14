# Changelog

## [0.111.1](https://github.com/jpe-ansible/ansible-secrets-management/compare/v0.111.0...v0.111.1) (2026-11-14)


### Bug Fixes

* **openbao:** derive the router snapshot installation from the docs repository owner ([#717](https://github.com/jpe-ansible/ansible-secrets-management/issues/717)) ([d78c879](https://github.com/jpe-ansible/ansible-secrets-management/commit/d78c879b8bdfbe53869398bd180e884225cced8b))

## [0.111.0](https://github.com/jpe-ansible/ansible-secrets-management/compare/v0.110.0...v0.111.0) (2026-11-14)


### Features

* **openbao:** read extra org-secrets source leaves from the converge env ([#714](https://github.com/jpe-ansible/ansible-secrets-management/issues/714)) ([45aff4e](https://github.com/jpe-ansible/ansible-secrets-management/commit/45aff4e6f5d439a35353984b85b6adc0fc674c72))

## [0.110.0](https://github.com/jpe-ansible/ansible-secrets-management/compare/v0.109.0...v0.110.0) (2026-11-14)


### Features

* **openbao:** declare one policy per arrangement identity ([#708](https://github.com/jpe-ansible/ansible-secrets-management/issues/708)) ([c5b1434](https://github.com/jpe-ansible/ansible-secrets-management/commit/c5b1434dd1b2a14540e680d2088d9cd67ff0a187))


### Bug Fixes

* **openbao:** reject arrangement grants the schema rejects ([#711](https://github.com/jpe-ansible/ansible-secrets-management/issues/711)) ([ed541bf](https://github.com/jpe-ansible/ansible-secrets-management/commit/ed541bf457d308c73c1d33b545e83ccf8f1254f3))

## [0.109.0](https://github.com/jpe-ansible/ansible-secrets-management/compare/v0.108.0...v0.109.0) (2026-11-14)


### Features

* **openbao:** render identity policies from a secrets arrangement ([#706](https://github.com/jpe-ansible/ansible-secrets-management/issues/706)) ([e7869c5](https://github.com/jpe-ansible/ansible-secrets-management/commit/e7869c5385d0b69f549f5ef43a23c1368d8b8569))

## 0.108.0 (2026-11-14)


### Features

* **openbao:** declare the agent-session search token path in the converge policy (#699)

## [0.107.0](https://github.com/jpe-ansible/ansible-secrets-management/compare/v0.106.0...v0.107.0) (2026-11-14)


### Features

* **openbao:** declare the Splunk rotator path in the converge policy ([#695](https://github.com/jpe-ansible/ansible-secrets-management/issues/695)) ([4c085c0](https://github.com/jpe-ansible/ansible-secrets-management/commit/4c085c05ad673ac3da65300ba603ddeb76fcf2b9))


### Bug Fixes

* **openbao:** grant converge the Splunk rotator credential path ([4c085c0](https://github.com/jpe-ansible/ansible-secrets-management/commit/4c085c05ad673ac3da65300ba603ddeb76fcf2b9))

## [0.106.0](https://github.com/jpe-ansible/ansible-secrets-management/compare/v0.105.1...v0.106.0) (2026-11-13)


### Features

* **openbao:** declare a workflow-dispatch permission set ([#688](https://github.com/jpe-ansible/ansible-secrets-management/issues/688)) ([f93355e](https://github.com/jpe-ansible/ansible-secrets-management/commit/f93355e0f8706aadc8f4a03106fcf3b7f4de0a4e))
* **openbao:** declare runner registration sets for env-listed owners ([#691](https://github.com/jpe-ansible/ansible-secrets-management/issues/691)) ([d7f418e](https://github.com/jpe-ansible/ansible-secrets-management/commit/d7f418e08513065180ffe64a69a6b08abf65244a))


### Bug Fixes

* **openbao:** cover the scheduled rotator's own AppRole ([#681](https://github.com/jpe-ansible/ansible-secrets-management/issues/681)) ([145c4de](https://github.com/jpe-ansible/ansible-secrets-management/commit/145c4dedbc068f1c83001e419e25180c9ec9ffc0))

## [0.105.1](https://github.com/jpe-ansible/ansible-secrets-management/compare/v0.105.0...v0.105.1) (2026-11-13)


### Bug Fixes

* **openbao:** name every org-secrets permission set in lower case ([#686](https://github.com/jpe-ansible/ansible-secrets-management/issues/686)) ([814c6ab](https://github.com/jpe-ansible/ansible-secrets-management/commit/814c6ab465c1c2362a462de7a6b12f66c110b217))

## [0.105.0](https://github.com/jpe-ansible/ansible-secrets-management/compare/v0.104.0...v0.105.0) (2026-11-13)


### Features

* **openbao:** add the pr-reconcile-sweep OIDC role and policy ([#675](https://github.com/jpe-ansible/ansible-secrets-management/issues/675)) ([26f7963](https://github.com/jpe-ansible/ansible-secrets-management/commit/26f79631e1a134a436fa670690986b60d01881a9))
* **openbao:** declare org-secrets sets for two more organizations ([#680](https://github.com/jpe-ansible/ansible-secrets-management/issues/680)) ([3561585](https://github.com/jpe-ansible/ansible-secrets-management/commit/356158577bf1077b5f6558dfb1f0713c1a0cb7ca))
* **openbao:** generate svc_mcp_clerk_password for vikunja ([#678](https://github.com/jpe-ansible/ansible-secrets-management/issues/678)) ([19f1cb7](https://github.com/jpe-ansible/ansible-secrets-management/commit/19f1cb7b28936617ae1861406b6c341bbb92d19f))


### Bug Fixes

* **openbao:** add org-secrets leaves and per-owner permission sets ([#677](https://github.com/jpe-ansible/ansible-secrets-management/issues/677)) ([abeccaf](https://github.com/jpe-ansible/ansible-secrets-management/commit/abeccafd2a150252405f2e29dc2ba20230ae3bde))

## [0.104.0](https://github.com/dryvist/ansible-secrets-management/compare/v0.103.0...v0.104.0) (2026-11-13)


### Features

* **openbao:** add a BAO_AGENT_ADDR mode ([#673](https://github.com/dryvist/ansible-secrets-management/issues/673)) ([a0085db](https://github.com/dryvist/ansible-secrets-management/commit/a0085db654755ecfedd66997939ffe664ed23b6b))


### Bug Fixes

* **openbao:** update the evals OIDC repository binding ([#674](https://github.com/dryvist/ansible-secrets-management/issues/674)) ([bf1dabf](https://github.com/dryvist/ansible-secrets-management/commit/bf1dabfbdbcf616e82f3b2487af50e07ef78938a))

## [0.103.0](https://github.com/dryvist/ansible-secrets-management/compare/v0.102.0...v0.103.0) (2026-11-12)


### Features

* **openbao:** admin window manages declared protected policies and AppRoles ([#670](https://github.com/dryvist/ansible-secrets-management/issues/670)) ([1aa64ed](https://github.com/dryvist/ansible-secrets-management/commit/1aa64edb656c38b4eb107689d82daa8c2acd3e7e))

## [0.102.0](https://github.com/dryvist/ansible-secrets-management/compare/v0.101.1...v0.102.0) (2026-11-12)


### Features

* **openbao:** select the reconcile policy in a selected run ([#666](https://github.com/dryvist/ansible-secrets-management/issues/666)) ([d285a08](https://github.com/dryvist/ansible-secrets-management/commit/d285a08db31c311ac56aafb3538d972941bcce30))

## [0.101.1](https://github.com/dryvist/ansible-secrets-management/compare/v0.101.0...v0.101.1) (2026-11-12)


### Bug Fixes

* **openbao:** scope the molecule ssh-sign apply invariant around the declared unifi role ([#661](https://github.com/dryvist/ansible-secrets-management/issues/661)) ([93fee66](https://github.com/dryvist/ansible-secrets-management/commit/93fee662b8987486371c3692680b0297eb2d0eb7))

## [0.101.0](https://github.com/dryvist/ansible-secrets-management/compare/v0.100.0...v0.101.0) (2026-11-12)


### Features

* **openbao:** add one exact converge policy path ([#662](https://github.com/dryvist/ansible-secrets-management/issues/662)) ([b3509e8](https://github.com/dryvist/ansible-secrets-management/commit/b3509e8a16b4407b5bcde309aaaa88667a2cfa69))
* **openbao:** let converge publish the Splunk platform search token ([b3509e8](https://github.com/dryvist/ansible-secrets-management/commit/b3509e8a16b4407b5bcde309aaaa88667a2cfa69))

## [0.100.0](https://github.com/dryvist/ansible-secrets-management/compare/v0.99.0...v0.100.0) (2026-11-12)


### Features

* **openbao:** add Dify PR automation GitHub mint sets ([#656](https://github.com/dryvist/ansible-secrets-management/issues/656)) ([fd53e8d](https://github.com/dryvist/ansible-secrets-management/commit/fd53e8df0e445a07365a40212aa58b847139fd5a))
* **openbao:** seed generated Crawl4AI API token ([#657](https://github.com/dryvist/ansible-secrets-management/issues/657)) ([4f1c1e5](https://github.com/dryvist/ansible-secrets-management/commit/4f1c1e53956dac3d085d6f888259e97a53845a72))

## [0.99.0](https://github.com/dryvist/ansible-secrets-management/compare/v0.98.0...v0.99.0) (2026-11-12)


### Features

* **openbao:** add selective GitHub permission-set runs ([#651](https://github.com/dryvist/ansible-secrets-management/issues/651)) ([363a711](https://github.com/dryvist/ansible-secrets-management/commit/363a711a7440b91dc134a66d24c3515539821efe))
* **openbao:** tiered unifi controller credential access ([#601](https://github.com/dryvist/ansible-secrets-management/issues/601)) ([c0009f4](https://github.com/dryvist/ansible-secrets-management/commit/c0009f4126bb8a7ab5d4676b199dd8affec0e59a))


### Bug Fixes

* **authelia:** cap the signing-writer token at 10m and log in under check mode ([#653](https://github.com/dryvist/ansible-secrets-management/issues/653)) ([074a5d9](https://github.com/dryvist/ansible-secrets-management/commit/074a5d994cab5ef0a96462b3247cb2f07799e46d))
* **openbao:** give the Authelia signing writer its own login ([#639](https://github.com/dryvist/ansible-secrets-management/issues/639)) ([894dac1](https://github.com/dryvist/ansible-secrets-management/commit/894dac1107eb52a9274cbf52799190304992f690))

## [0.98.0](https://github.com/dryvist/ansible-secrets-management/compare/v0.97.0...v0.98.0) (2026-11-12)


### Features

* **openbao:** let the workstation identity read the Slack reader token ([#649](https://github.com/dryvist/ansible-secrets-management/issues/649)) ([79bbebe](https://github.com/dryvist/ansible-secrets-management/commit/79bbebe31eadc0f58d1c53fbf15cb9cbb1edf8ad))

## [0.97.0](https://github.com/dryvist/ansible-secrets-management/compare/v0.96.0...v0.97.0) (2026-11-12)


### Features

* **openbao:** deliver the QwenCloud key to the router role ([#644](https://github.com/dryvist/ansible-secrets-management/issues/644)) ([58ebcdf](https://github.com/dryvist/ansible-secrets-management/commit/58ebcdfe5e5e6697103ace508271772bc3a50e02))


### Bug Fixes

* **openbao:** use the declared secret_id_bound_cidrs for each AppRole ([#631](https://github.com/dryvist/ansible-secrets-management/issues/631)) ([e8ec3c9](https://github.com/dryvist/ansible-secrets-management/commit/e8ec3c9822d40311f58abf1059bc3eaeb3753297))

## [0.96.0](https://github.com/dryvist/ansible-secrets-management/compare/v0.95.2...v0.96.0) (2026-11-11)


### Features

* **openbao:** add a declared GitHub App key rotation mode ([#634](https://github.com/dryvist/ansible-secrets-management/issues/634)) ([d23e3ec](https://github.com/dryvist/ansible-secrets-management/commit/d23e3ec9f83c0f37c7a188ddf9db5c728fa3e81d))
* **openbao:** add the Dify agent secret-id issuer AppRole ([#632](https://github.com/dryvist/ansible-secrets-management/issues/632)) ([8197aec](https://github.com/dryvist/ansible-secrets-management/commit/8197aec7091a15b5908a762e587aa68c6edc9c23))
* **openbao:** declare a workflows-write permission set per installation ([#637](https://github.com/dryvist/ansible-secrets-management/issues/637)) ([4657406](https://github.com/dryvist/ansible-secrets-management/commit/46574063fcaaa79a6493b60f4ac95fb4456d9b1d))
* **openbao:** remove the pr-reconcile AppRole, policy and token sets ([#635](https://github.com/dryvist/ansible-secrets-management/issues/635)) ([acc4ff9](https://github.com/dryvist/ansible-secrets-management/commit/acc4ff92ae2b8a2b1c0b97b6ba3c7ab34648ba64))


### Bug Fixes

* **openbao:** accept the loopback source in both binds of every loopback-client identity ([#638](https://github.com/dryvist/ansible-secrets-management/issues/638)) ([d695724](https://github.com/dryvist/ansible-secrets-management/commit/d695724cea2826c586740bbb5268398a06203638))
* **openbao:** read the Dify issuer bound value from the environment document ([#640](https://github.com/dryvist/ansible-secrets-management/issues/640)) ([809ae9a](https://github.com/dryvist/ansible-secrets-management/commit/809ae9ad1966f65ea52c248ce6ec37e8ef4e7fd1))

## [0.95.2](https://github.com/dryvist/ansible-secrets-management/compare/v0.95.1...v0.95.2) (2026-11-11)


### Bug Fixes

* **openbao:** stamp disclosure-denylist metadata on the github-org path ([#609](https://github.com/dryvist/ansible-secrets-management/issues/609)) ([bcdefdd](https://github.com/dryvist/ansible-secrets-management/commit/bcdefdd3df1d4d7c77ddf37e586dd4719bf99ec8))

## [0.95.1](https://github.com/dryvist/ansible-secrets-management/compare/v0.95.0...v0.95.1) (2026-11-11)


### Bug Fixes

* **openbao:** route rotate and secret-age login through loopback ([#625](https://github.com/dryvist/ansible-secrets-management/issues/625)) ([4c118af](https://github.com/dryvist/ansible-secrets-management/commit/4c118afe41691731de0df946569035cef6accd8f))

## [0.95.0](https://github.com/dryvist/ansible-secrets-management/compare/v0.94.0...v0.95.0) (2026-11-11)


### Features

* **openbao:** add the jacobpevans-workflows-write permission set for PR-automation workflow files ([#624](https://github.com/dryvist/ansible-secrets-management/issues/624)) ([14b2546](https://github.com/dryvist/ansible-secrets-management/commit/14b2546dc193124aaf6684a193ae30288bdf4c4a))
* **openbao:** let the seed-writer login issue Dify agent SecretIDs ([#622](https://github.com/dryvist/ansible-secrets-management/issues/622)) ([c0a1a3d](https://github.com/dryvist/ansible-secrets-management/commit/c0a1a3de58596bab03aff6f541543adac3fc9751))

## [0.94.0](https://github.com/dryvist/ansible-secrets-management/compare/v0.93.0...v0.94.0) (2026-11-11)


### Features

* **openbao:** add the pr-reconcile token sets, AppRole and policy ([#620](https://github.com/dryvist/ansible-secrets-management/issues/620)) ([eabeff2](https://github.com/dryvist/ansible-secrets-management/commit/eabeff277b1bc56067e2098994724705f0546447))

## [0.93.0](https://github.com/dryvist/ansible-secrets-management/compare/v0.92.0...v0.93.0) (2026-11-11)


### Features

* **openbao:** bind the openhands secret_id to its own /32 ([#615](https://github.com/dryvist/ansible-secrets-management/issues/615)) ([820e5f4](https://github.com/dryvist/ansible-secrets-management/commit/820e5f4eb758c4602111a801ffcc7d2e1e173bb8))


### Bug Fixes

* **openbao:** read the openhands bind from the platform environment ([#616](https://github.com/dryvist/ansible-secrets-management/issues/616)) ([588aef9](https://github.com/dryvist/ansible-secrets-management/commit/588aef93db3def521011f451a2dbb45d7b7c1566))
* **openbao:** run the GitHub engine converge on its own tag ([#612](https://github.com/dryvist/ansible-secrets-management/issues/612)) ([3fc76cc](https://github.com/dryvist/ansible-secrets-management/commit/3fc76ccb015b109e395fa5b84d2c445ad1fe3a33))

## [0.92.0](https://github.com/dryvist/ansible-secrets-management/compare/v0.91.0...v0.92.0) (2026-11-10)


### Features

* **openbao:** add the JacobPEvans-ai org-secrets permission set and webhook read path ([#610](https://github.com/dryvist/ansible-secrets-management/issues/610)) ([7db1edf](https://github.com/dryvist/ansible-secrets-management/commit/7db1edf5e6dfe2f11abbde12c577c67137577801))

## [0.91.0](https://github.com/dryvist/ansible-secrets-management/compare/v0.90.0...v0.91.0) (2026-11-10)


### Features

* **openbao:** add the git-mirror read-only token sets, AppRole and Apps secret ([#605](https://github.com/dryvist/ansible-secrets-management/issues/605)) ([daa69dc](https://github.com/dryvist/ansible-secrets-management/commit/daa69dc8852a37c9b7cc211ad5d2464c2c20f69c))

## [0.90.0](https://github.com/dryvist/ansible-secrets-management/compare/v0.89.0...v0.90.0) (2026-11-10)


### Features

* **openbao:** let agent-workstation read the Zammad MCP secret ([#603](https://github.com/dryvist/ansible-secrets-management/issues/603)) ([8cffe1c](https://github.com/dryvist/ansible-secrets-management/commit/8cffe1c70cdd042fe68d83055e94eaa05747a1db))

## [0.89.0](https://github.com/dryvist/ansible-secrets-management/compare/v0.88.0...v0.89.0) (2026-11-09)


### Features

* **agent:** opencode-local run j-818c1878e5c36855 ([62ca033](https://github.com/dryvist/ansible-secrets-management/commit/62ca033cc6c278546bb00fb009becc07ce327569))
* **agent:** zcode run j-fbeff26faf068c6f ([35dd70a](https://github.com/dryvist/ansible-secrets-management/commit/35dd70a908f4a2cd8005693c17f046e319743a8d))
* **openbao:** generate the evals router key and an OIDC read role for the scheduled eval workflow ([#597](https://github.com/dryvist/ansible-secrets-management/issues/597)) ([35dd70a](https://github.com/dryvist/ansible-secrets-management/commit/35dd70a908f4a2cd8005693c17f046e319743a8d))


### Bug Fixes

* **openbao:** remove the snapshot login stderr temp file on exit ([#598](https://github.com/dryvist/ansible-secrets-management/issues/598)) ([62ca033](https://github.com/dryvist/ansible-secrets-management/commit/62ca033cc6c278546bb00fb009becc07ce327569))

## [0.88.0](https://github.com/dryvist/ansible-secrets-management/compare/v0.87.1...v0.88.0) (2026-11-09)


### Features

* **openbao:** generate a local-only sandbox router key field ([#591](https://github.com/dryvist/ansible-secrets-management/issues/591)) ([92ced7f](https://github.com/dryvist/ansible-secrets-management/commit/92ced7f08642ca02f92e7132ba02d937e2bf5d60))

## [0.87.1](https://github.com/dryvist/ansible-secrets-management/compare/v0.87.0...v0.87.1) (2026-11-09)


### Bug Fixes

* **openbao:** let sandbox job tokens outlive the job guard ([#588](https://github.com/dryvist/ansible-secrets-management/issues/588)) ([c35ed69](https://github.com/dryvist/ansible-secrets-management/commit/c35ed6993e213db5bf57ed30b1a45bc92d81b237))

## [0.87.0](https://github.com/dryvist/ansible-secrets-management/compare/v0.86.0...v0.87.0) (2026-11-09)


### Features

* **agent:** autonomous zcode run j-a4ef550529d9c48c ([#585](https://github.com/dryvist/ansible-secrets-management/issues/585)) ([a76b29b](https://github.com/dryvist/ansible-secrets-management/commit/a76b29b12358a75be173dba69f86b6db98eca6da))
* **agent:** zcode run j-a4ef550529d9c48c ([a76b29b](https://github.com/dryvist/ansible-secrets-management/commit/a76b29b12358a75be173dba69f86b6db98eca6da))

## [0.86.0](https://github.com/dryvist/ansible-secrets-management/compare/v0.85.1...v0.86.0) (2026-11-09)


### Features

* **openbao:** add sandbox-cursor read and write AppRoles ([#580](https://github.com/dryvist/ansible-secrets-management/issues/580)) ([22e00b5](https://github.com/dryvist/ansible-secrets-management/commit/22e00b555066ffbc62f68a381ac410f50928c001))


### Bug Fixes

* **openbao:** route snapshot login through loopback ([#579](https://github.com/dryvist/ansible-secrets-management/issues/579)) ([25c00c9](https://github.com/dryvist/ansible-secrets-management/commit/25c00c92f4a6914834e494edf91669ddb093b107))

## [0.85.1](https://github.com/dryvist/ansible-secrets-management/compare/v0.85.0...v0.85.1) (2026-11-09)


### Bug Fixes

* **openbao:** grant the new Slack secret paths beside the old ones ([#576](https://github.com/dryvist/ansible-secrets-management/issues/576)) ([dcd079f](https://github.com/dryvist/ansible-secrets-management/commit/dcd079fb3335a8c710674ed38fd179b3f9a609c8))

## [0.85.0](https://github.com/dryvist/ansible-secrets-management/compare/v0.84.0...v0.85.0) (2026-11-09)


### Features

* **openbao:** add the github-openhands App mount and its AppRole ([#573](https://github.com/dryvist/ansible-secrets-management/issues/573)) ([a3ec8f0](https://github.com/dryvist/ansible-secrets-management/commit/a3ec8f00d07d27b773d9b2e23fe1e39b80182b7a))

## [0.84.0](https://github.com/dryvist/ansible-secrets-management/compare/v0.83.0...v0.84.0) (2026-11-08)


### Features

* **openbao:** add the openhands AppRole and policy ([#567](https://github.com/dryvist/ansible-secrets-management/issues/567)) ([04d9557](https://github.com/dryvist/ansible-secrets-management/commit/04d9557447c977a33fc4d19d8b6c9fa1a2776e2d))
* **openbao:** grant list on the Dify MCP URL metadata path ([#570](https://github.com/dryvist/ansible-secrets-management/issues/570)) ([ee13fd1](https://github.com/dryvist/ansible-secrets-management/commit/ee13fd1a811f92fda2141b9d5be8a29cf92c0635))
* **openbao:** let the converge identity seed Dify MCP URL leaves ([#568](https://github.com/dryvist/ansible-secrets-management/issues/568)) ([b615f5e](https://github.com/dryvist/ansible-secrets-management/commit/b615f5e73d396e69078b06e25b5917fd12e7881f))

## [0.83.0](https://github.com/dryvist/ansible-secrets-management/compare/v0.82.1...v0.83.0) (2026-11-08)


### Features

* **openbao:** generate OpenHands secrets and its Vikunja bot login ([#561](https://github.com/dryvist/ansible-secrets-management/issues/561)) ([d37e8b4](https://github.com/dryvist/ansible-secrets-management/commit/d37e8b422cf497d5fcc0af3ce2d9c392c64ff4d4))

## [0.82.1](https://github.com/dryvist/ansible-secrets-management/compare/v0.82.0...v0.82.1) (2026-11-08)


### Bug Fixes

* **openbao:** let the converge seed write Dify agent app key leaves ([#562](https://github.com/dryvist/ansible-secrets-management/issues/562)) ([1dfc544](https://github.com/dryvist/ansible-secrets-management/commit/1dfc544e728a53a5ea0c1f9f660c30fd9fabf11b))

## [0.82.0](https://github.com/dryvist/ansible-secrets-management/compare/v0.81.0...v0.82.0) (2026-11-08)


### Features

* **openbao:** give Pepper's GitHub read set a repository list ([#558](https://github.com/dryvist/ansible-secrets-management/issues/558)) ([b10a943](https://github.com/dryvist/ansible-secrets-management/commit/b10a943e9a685e1621e446b8a9123cd6228e8ee7))

## [0.81.0](https://github.com/dryvist/ansible-secrets-management/compare/v0.80.0...v0.81.0) (2026-11-07)


### Features

* **openbao:** let the write identity mint repo-scoped personal tokens ([#554](https://github.com/dryvist/ansible-secrets-management/issues/554)) ([5c8bbea](https://github.com/dryvist/ansible-secrets-management/commit/5c8bbeaff78bdf03b208d835edd2c42a2ad3c150))

## [0.80.0](https://github.com/dryvist/ansible-secrets-management/compare/v0.79.0...v0.80.0) (2026-11-07)


### Features

* **openbao:** grant Pepper and Donna their exact vendor paths ([20b9f85](https://github.com/dryvist/ansible-secrets-management/commit/20b9f855b733cf86772f517a541a5c1f8db13a62))
* **openbao:** update the Pepper and Donna policies ([#551](https://github.com/dryvist/ansible-secrets-management/issues/551)) ([20b9f85](https://github.com/dryvist/ansible-secrets-management/commit/20b9f855b733cf86772f517a541a5c1f8db13a62))

## [0.79.0](https://github.com/dryvist/ansible-secrets-management/compare/v0.78.1...v0.79.0) (2026-11-07)


### Features

* **openbao:** add a dedicated GitHub mount for Pepper ([#548](https://github.com/dryvist/ansible-secrets-management/issues/548)) ([4d35b2b](https://github.com/dryvist/ansible-secrets-management/commit/4d35b2be5544dbcbdb30687f008ccdf8e56d1d3f))

## [0.78.1](https://github.com/dryvist/ansible-secrets-management/compare/v0.78.0...v0.78.1) (2026-11-07)


### Bug Fixes

* **authelia:** correct the Phoenix redirect URI ([#544](https://github.com/dryvist/ansible-secrets-management/issues/544)) ([b6ef72e](https://github.com/dryvist/ansible-secrets-management/commit/b6ef72e8362b1b979c818899f47e7b98288fd26f))
* **authelia:** register the Phoenix OAuth2 tokens callback ([b6ef72e](https://github.com/dryvist/ansible-secrets-management/commit/b6ef72e8362b1b979c818899f47e7b98288fd26f))

## [0.78.0](https://github.com/dryvist/ansible-secrets-management/compare/v0.77.0...v0.78.0) (2026-11-07)


### Features

* **openbao:** add one selector for individual lanes ([#542](https://github.com/dryvist/ansible-secrets-management/issues/542)) ([559ecec](https://github.com/dryvist/ansible-secrets-management/commit/559ecec3b6b2bfc61afa046c91f77c25a09ef797))

## [0.77.0](https://github.com/dryvist/ansible-secrets-management/compare/v0.76.0...v0.77.0) (2026-11-07)


### Features

* **openbao:** grant the media stack's four-segment secret paths ([#539](https://github.com/dryvist/ansible-secrets-management/issues/539)) ([21d8ff3](https://github.com/dryvist/ansible-secrets-management/commit/21d8ff3c04000a01dc6e01381435f263279fa384))

## [0.76.0](https://github.com/dryvist/ansible-secrets-management/compare/v0.75.0...v0.76.0) (2026-11-07)


### Features

* **openbao:** add the Pepper agent identity ([#530](https://github.com/dryvist/ansible-secrets-management/issues/530)) ([cd1d8a9](https://github.com/dryvist/ansible-secrets-management/commit/cd1d8a98f8161b5a6aafc5576fd53c0b98f671e2))


### Bug Fixes

* **openbao:** keep session backup credentials valid between runs ([2c5395f](https://github.com/dryvist/ansible-secrets-management/commit/2c5395fd8f738bb6606e20958e83b100bdceb78c))
* **openbao:** keep the ai-sessions-backup secret_id alive between runs ([#529](https://github.com/dryvist/ansible-secrets-management/issues/529)) ([2c5395f](https://github.com/dryvist/ansible-secrets-management/commit/2c5395fd8f738bb6606e20958e83b100bdceb78c))
* **openbao:** let the roster check read roster AppRoles and keep upgrades out of policy runs ([#532](https://github.com/dryvist/ansible-secrets-management/issues/532)) ([8fbd6bf](https://github.com/dryvist/ansible-secrets-management/commit/8fbd6bf55a522df2c8987b3cfe495f7905d7a668))

## [0.75.0](https://github.com/dryvist/ansible-secrets-management/compare/v0.74.0...v0.75.0) (2026-11-07)


### Features

* **openbao:** scope window service credentials ([#523](https://github.com/dryvist/ansible-secrets-management/issues/523)) ([5ccb7bc](https://github.com/dryvist/ansible-secrets-management/commit/5ccb7bca39d277d5464eb7389343a97bad69c0c8))

## [0.74.0](https://github.com/dryvist/ansible-secrets-management/compare/v0.73.0...v0.74.0) (2026-11-06)


### Features

* seed Home Assistant router key ([#520](https://github.com/dryvist/ansible-secrets-management/issues/520)) ([4c1393f](https://github.com/dryvist/ansible-secrets-management/commit/4c1393ffd53122c3039807e8b9ef42ed3909f865))


### Bug Fixes

* **openbao:** generate and authorize the Langflow and Grafana router keys ([#524](https://github.com/dryvist/ansible-secrets-management/issues/524)) ([3814fb7](https://github.com/dryvist/ansible-secrets-management/commit/3814fb7b5a8a34be51b30c16d7c3ac2fda069b55))

## [0.73.0](https://github.com/dryvist/ansible-secrets-management/compare/v0.72.0...v0.73.0) (2026-11-06)


### Features

* **openbao:** seed the langflow router key leaf ([#521](https://github.com/dryvist/ansible-secrets-management/issues/521)) ([c10584c](https://github.com/dryvist/ansible-secrets-management/commit/c10584c964c1950b3c2c92c8ce3813bf4884ebbb))

## [0.72.0](https://github.com/dryvist/ansible-secrets-management/compare/v0.71.0...v0.72.0) (2026-11-05)


### Features

* **openbao:** add two read-only paths to the agent-workstation policy ([#517](https://github.com/dryvist/ansible-secrets-management/issues/517)) ([5cad2df](https://github.com/dryvist/ansible-secrets-management/commit/5cad2df078d8f6f3eb896d8119b40174e297b27c))
* **openbao:** let agent-workstation read the YouTrack agent token and Dify app keys ([5cad2df](https://github.com/dryvist/ansible-secrets-management/commit/5cad2df078d8f6f3eb896d8119b40174e297b27c))


### Bug Fixes

* **openbao:** skip the approle-issuer liveness probe in check mode ([#514](https://github.com/dryvist/ansible-secrets-management/issues/514)) ([12057f4](https://github.com/dryvist/ansible-secrets-management/commit/12057f4d9993df29eef13c260a14596b406abf9b))

## [0.71.0](https://github.com/dryvist/ansible-secrets-management/compare/v0.70.0...v0.71.0) (2026-11-05)


### Features

* **openbao:** read the grafana-alerts domain from the Slack ops leaf ([#510](https://github.com/dryvist/ansible-secrets-management/issues/510)) ([5447766](https://github.com/dryvist/ansible-secrets-management/commit/5447766db075d40ec1cd7d480c139856c2113385))

## [0.70.0](https://github.com/dryvist/ansible-secrets-management/compare/v0.69.0...v0.70.0) (2026-11-04)


### Features

* **openbao:** separate Authelia's service secrets and pin who can read them ([#506](https://github.com/dryvist/ansible-secrets-management/issues/506)) ([cb85798](https://github.com/dryvist/ansible-secrets-management/commit/cb8579829d4b99b6005685604caf8a46d30399ce))

## [0.69.0](https://github.com/dryvist/ansible-secrets-management/compare/v0.68.0...v0.69.0) (2026-11-04)


### Features

* **openbao:** add the grafana-alerts secret domain ([#501](https://github.com/dryvist/ansible-secrets-management/issues/501)) ([0f166a5](https://github.com/dryvist/ansible-secrets-management/commit/0f166a577b49e7c73834fe5ce3e5bb0c2b550762))

## [0.68.0](https://github.com/dryvist/ansible-secrets-management/compare/v0.67.1...v0.68.0) (2026-11-04)


### Features

* **openbao:** let the reconcile identity read apps/grafana ([#498](https://github.com/dryvist/ansible-secrets-management/issues/498)) ([d61a6b3](https://github.com/dryvist/ansible-secrets-management/commit/d61a6b338367001710bc992d1b87d6860712fcb9))
* **openbao:** raise the ai-admin-session hard max to 12h ([#495](https://github.com/dryvist/ansible-secrets-management/issues/495)) ([a2bbc42](https://github.com/dryvist/ansible-secrets-management/commit/a2bbc42662ee75e33349e6f90fa84bec3aaaef1d))

## [0.67.1](https://github.com/dryvist/ansible-secrets-management/compare/v0.67.0...v0.67.1) (2026-11-04)


### Bug Fixes

* **openbao:** grant KV metadata read on external write paths ([#496](https://github.com/dryvist/ansible-secrets-management/issues/496)) ([3ee8492](https://github.com/dryvist/ansible-secrets-management/commit/3ee84924fb9ace777333bcf19a3bcdedbd6c4724))
* **openbao:** grant metadata read on external KV paths written by Terrakube workspaces ([3ee8492](https://github.com/dryvist/ansible-secrets-management/commit/3ee84924fb9ace777333bcf19a3bcdedbd6c4724))

## [0.67.0](https://github.com/dryvist/ansible-secrets-management/compare/v0.66.1...v0.67.0) (2026-11-04)


### Features

* **openbao:** add the slack-approvals AppRole ([#490](https://github.com/dryvist/ansible-secrets-management/issues/490)) ([a8e1ea9](https://github.com/dryvist/ansible-secrets-management/commit/a8e1ea9c63774e456d5e6aa37235b8be6cb68220))
* **openbao:** name one command per policy and gate full-set text changes ([#487](https://github.com/dryvist/ansible-secrets-management/issues/487)) ([8fe8256](https://github.com/dryvist/ansible-secrets-management/commit/8fe825675bc13cd8fdedf29fe9dcbe1d038f1008))


### Bug Fixes

* **openbao:** declare the platform env and Terrakube read leaves ([#486](https://github.com/dryvist/ansible-secrets-management/issues/486)) ([5c0a984](https://github.com/dryvist/ansible-secrets-management/commit/5c0a98493b2143596498a544e935835c0d40da0c))
* **openbao:** pass the runtime token to inventory resolution in scheduled mode ([#489](https://github.com/dryvist/ansible-secrets-management/issues/489)) ([e072003](https://github.com/dryvist/ansible-secrets-management/commit/e072003f605c306f817a57a19ece9062adf8422f))

## [0.66.1](https://github.com/dryvist/ansible-secrets-management/compare/v0.66.0...v0.66.1) (2026-11-03)


### Bug Fixes

* **openbao:** grant the semaphore identity read on the config env document ([f1ab58f](https://github.com/dryvist/ansible-secrets-management/commit/f1ab58f4de8600239f23594d9f4cf0f7bf5628bd))
* **openbao:** grant the Semaphore policy read on the config-mount env document ([#485](https://github.com/dryvist/ansible-secrets-management/issues/485)) ([f1ab58f](https://github.com/dryvist/ansible-secrets-management/commit/f1ab58f4de8600239f23594d9f4cf0f7bf5628bd))

## [0.66.0](https://github.com/dryvist/ansible-secrets-management/compare/v0.65.0...v0.66.0) (2026-11-03)


### Features

* **openbao:** add one read path to an agent policy ([#482](https://github.com/dryvist/ansible-secrets-management/issues/482)) ([1421d5a](https://github.com/dryvist/ansible-secrets-management/commit/1421d5a29ba3072815e402f533a1ef7365745ef4))

## [0.65.0](https://github.com/dryvist/ansible-secrets-management/compare/v0.64.0...v0.65.0) (2026-11-03)


### Features

* **openbao:** clickhouse-wall secret domain ([#467](https://github.com/dryvist/ansible-secrets-management/issues/467)) ([9b73d1b](https://github.com/dryvist/ansible-secrets-management/commit/9b73d1be868ef5954edd0137a82af0bb5f352d0d))


### Bug Fixes

* **authelia:** extend the device-code lifespan to fifteen minutes ([#474](https://github.com/dryvist/ansible-secrets-management/issues/474)) ([4d88088](https://github.com/dryvist/ansible-secrets-management/commit/4d88088b7c93eb73d01ea36540469f0be450795a))
* **authelia:** register the YouTrack Hub auth module callback ([#472](https://github.com/dryvist/ansible-secrets-management/issues/472)) ([1e82b76](https://github.com/dryvist/ansible-secrets-management/commit/1e82b76acaee9019179cff694abd46a301195a63))

## [0.64.0](https://github.com/dryvist/ansible-secrets-management/compare/v0.63.1...v0.64.0) (2026-11-03)


### Features

* **openbao:** hatchet-killtest per-call reader of the power-only PVE token ([#431](https://github.com/dryvist/ansible-secrets-management/issues/431)) ([13b3682](https://github.com/dryvist/ansible-secrets-management/commit/13b36824185427fb19c822675eb05ed1232d994b))

## [0.63.1](https://github.com/dryvist/ansible-secrets-management/compare/v0.63.0...v0.63.1) (2026-11-03)


### Bug Fixes

* **openbao:** split the legacy kept-fields set_fact into its own task ([#464](https://github.com/dryvist/ansible-secrets-management/issues/464)) ([4af5fe7](https://github.com/dryvist/ansible-secrets-management/commit/4af5fe7daca8fa9a8a270f61c9cb498b8d73e639))

## [0.63.0](https://github.com/dryvist/ansible-secrets-management/compare/v0.62.0...v0.63.0) (2026-11-03)


### Features

* **agent:** autonomous zcode run j-9a0f9c1d8e7acc09 ([#461](https://github.com/dryvist/ansible-secrets-management/issues/461)) ([f5c1869](https://github.com/dryvist/ansible-secrets-management/commit/f5c1869ae9ee50de547a13b1e938e3d98017b08a))
* **agent:** zcode run j-9a0f9c1d8e7acc09 ([f5c1869](https://github.com/dryvist/ansible-secrets-management/commit/f5c1869ae9ee50de547a13b1e938e3d98017b08a))

## [0.62.0](https://github.com/dryvist/ansible-secrets-management/compare/v0.61.0...v0.62.0) (2026-11-03)


### Features

* **openbao:** add the agent-vikunja-triage Dify agent identity ([#455](https://github.com/dryvist/ansible-secrets-management/issues/455)) ([0ce24be](https://github.com/dryvist/ansible-secrets-management/commit/0ce24bebfaa6d5ff9a7163ddfda5496151036391))
* **openbao:** add the claude-code-router-key workstation AppRole ([#456](https://github.com/dryvist/ansible-secrets-management/issues/456)) ([9215b8a](https://github.com/dryvist/ansible-secrets-management/commit/9215b8a7dd273c6af1a4b622d7aedd3354c15bbf))

## [0.61.0](https://github.com/dryvist/ansible-secrets-management/compare/v0.60.3...v0.61.0) (2026-11-02)


### Features

* **authelia:** add YouTrack, Leantime and Vikunja OIDC clients ([#453](https://github.com/dryvist/ansible-secrets-management/issues/453)) ([c46cf17](https://github.com/dryvist/ansible-secrets-management/commit/c46cf17302ebebe7b5fcba461937104fb528c167))

## [0.60.3](https://github.com/dryvist/ansible-secrets-management/compare/v0.60.2...v0.60.3) (2026-11-02)


### Bug Fixes

* **openbao:** let sandbox job tokens renew for the full job budget ([#450](https://github.com/dryvist/ansible-secrets-management/issues/450)) ([fa2345e](https://github.com/dryvist/ansible-secrets-management/commit/fa2345e3f60815aac0c9a2b7eaf7e70aba049bf2))

## [0.60.2](https://github.com/dryvist/ansible-secrets-management/compare/v0.60.1...v0.60.2) (2026-11-02)


### Bug Fixes

* **openbao:** read the policy write rc from its registered result ([#445](https://github.com/dryvist/ansible-secrets-management/issues/445)) ([835ac61](https://github.com/dryvist/ansible-secrets-management/commit/835ac61b471711104dc4c70ba4797c95381173ca))
* **tests:** render the KV develop-path baseline from the in-file snapshot ([#447](https://github.com/dryvist/ansible-secrets-management/issues/447)) ([3ea4871](https://github.com/dryvist/ansible-secrets-management/commit/3ea48715b83561ae723e65c1795f300646e6413d))

## [0.60.1](https://github.com/dryvist/ansible-secrets-management/compare/v0.60.0...v0.60.1) (2026-11-02)


### Bug Fixes

* **openbao:** bound reconcile KV grants to exact declared leaves ([#400](https://github.com/dryvist/ansible-secrets-management/issues/400)) ([e35697b](https://github.com/dryvist/ansible-secrets-management/commit/e35697be33b80efff76feaff90d9fdd5d70c6787))

## [0.60.0](https://github.com/dryvist/ansible-secrets-management/compare/v0.59.0...v0.60.0) (2026-11-02)


### Features

* **authelia:** require WebAuthn user verification and guard the UV flag ([#433](https://github.com/dryvist/ansible-secrets-management/issues/433)) ([fd0b4a5](https://github.com/dryvist/ansible-secrets-management/commit/fd0b4a55af13ac17515e42638e27997f350f9862))
* **openbao:** add global read for the operator and trusted AI roles ([#440](https://github.com/dryvist/ansible-secrets-management/issues/440)) ([8d552aa](https://github.com/dryvist/ansible-secrets-management/commit/8d552aa401553c2d04783194271b256fa584bad4))
* **openbao:** add single-object policy and AppRole selectors ([8ba7a5e](https://github.com/dryvist/ansible-secrets-management/commit/8ba7a5e935b775eca8c93458a24996002dc5ee70))
* **openbao:** generate hermes_eval_api_server_key at apps/hermes-eval ([#434](https://github.com/dryvist/ansible-secrets-management/issues/434)) ([ded1a52](https://github.com/dryvist/ansible-secrets-management/commit/ded1a52d229ea931bfd6e350b0727e596f80105d))
* **openbao:** let the apps reader read the OpenCode Go key ([#439](https://github.com/dryvist/ansible-secrets-management/issues/439)) ([fd3c21c](https://github.com/dryvist/ansible-secrets-management/commit/fd3c21c312e285eef7bba6b7f17c30efe3704774))
* **openbao:** single-object selectors for policy and AppRole runs ([#437](https://github.com/dryvist/ansible-secrets-management/issues/437)) ([8ba7a5e](https://github.com/dryvist/ansible-secrets-management/commit/8ba7a5e935b775eca8c93458a24996002dc5ee70))


### Bug Fixes

* **authelia:** require discoverable WebAuthn credentials for passkey login ([#435](https://github.com/dryvist/ansible-secrets-management/issues/435)) ([e2a7385](https://github.com/dryvist/ansible-secrets-management/commit/e2a73853e26302c9e40a316ed16103f0761df574))
* **openbao:** let reconcile read the two pinned human-gated policies ([#441](https://github.com/dryvist/ansible-secrets-management/issues/441)) ([1eef962](https://github.com/dryvist/ansible-secrets-management/commit/1eef962bc5d89fab99661005728bb8229605ee40))

## [0.59.0](https://github.com/dryvist/ansible-secrets-management/compare/v0.58.0...v0.59.0) (2026-11-02)


### Features

* **openbao:** add agent-tier mount grants ([#430](https://github.com/dryvist/ansible-secrets-management/issues/430)) ([ba61cdb](https://github.com/dryvist/ansible-secrets-management/commit/ba61cdbdcc7260bc9b3a4dd4ebc55e23c77cec99))

## [0.58.0](https://github.com/dryvist/ansible-secrets-management/compare/v0.57.0...v0.58.0) (2026-11-02)


### Features

* **openbao:** add the converge-published apps/dify/eval leaf ([#423](https://github.com/dryvist/ansible-secrets-management/issues/423)) ([a0a02c7](https://github.com/dryvist/ansible-secrets-management/commit/a0a02c7656e2dcdccde17591cd0f4e7babba1908))
* **openbao:** generate app-agent identity credentials ([#427](https://github.com/dryvist/ansible-secrets-management/issues/427)) ([9684496](https://github.com/dryvist/ansible-secrets-management/commit/96844961677c2fb427d8cd1240878aeef4646c61))
* **openbao:** per-field valid patterns for generated app secrets ([#421](https://github.com/dryvist/ansible-secrets-management/issues/421)) ([9fc5f4b](https://github.com/dryvist/ansible-secrets-management/commit/9fc5f4bdcd44ad12223d38cba77644ab46cb8ca3))


### Bug Fixes

* **openbao:** generate the Hatchet cookie secret as one 32-character key ([#425](https://github.com/dryvist/ansible-secrets-management/issues/425)) ([41c9b43](https://github.com/dryvist/ansible-secrets-management/commit/41c9b43c0dbe73f4383d46ae4cba31886aaf1abf))
* **openbao:** parse the rotate request and fail on unknown field names ([#422](https://github.com/dryvist/ansible-secrets-management/issues/422)) ([fbcecb5](https://github.com/dryvist/ansible-secrets-management/commit/fbcecb57911017b76c1e1d5d2478cf04fa946b7c))
* **openbao:** warn and continue on pinned reconcile policy denials ([#424](https://github.com/dryvist/ansible-secrets-management/issues/424)) ([7b32741](https://github.com/dryvist/ansible-secrets-management/commit/7b327413431d2b44f6b8975bbf2c74d45b4eadb3))

## [0.57.0](https://github.com/dryvist/ansible-secrets-management/compare/v0.56.0...v0.57.0) (2026-11-02)


### Features

* **openbao:** add AppRoles for the vikunja-clerk and docs-updater fleet agents ([#416](https://github.com/dryvist/ansible-secrets-management/issues/416)) ([06f7bc9](https://github.com/dryvist/ansible-secrets-management/commit/06f7bc946307eb3ef0593e39708c93e1863c5935))
* **openbao:** add the converge-published apps/hatchet/eval leaf ([#417](https://github.com/dryvist/ansible-secrets-management/issues/417)) ([316ae2f](https://github.com/dryvist/ansible-secrets-management/commit/316ae2f1973e344fbf338f65787075754bfbeaaf))
* **openbao:** add the role-eval-status GitHub set and hatchet-eval-status AppRole ([#418](https://github.com/dryvist/ansible-secrets-management/issues/418)) ([0f6fd09](https://github.com/dryvist/ansible-secrets-management/commit/0f6fd09b1e16d16cc75d5d830c5122547648f577))

## [0.56.0](https://github.com/dryvist/ansible-secrets-management/compare/v0.55.0...v0.56.0) (2026-11-02)


### Features

* **openbao:** add the inert hatchet-token-publisher AppRole and policy ([#414](https://github.com/dryvist/ansible-secrets-management/issues/414)) ([64c3c8c](https://github.com/dryvist/ansible-secrets-management/commit/64c3c8cd18e5bfa1001027a264e160221a257954))


### Bug Fixes

* **openbao:** let the operator SSO token load the UI ([#411](https://github.com/dryvist/ansible-secrets-management/issues/411)) ([ed7f089](https://github.com/dryvist/ansible-secrets-management/commit/ed7f0893c7e66b781cb1df6e3daf9a443d8e99cf))

## [0.55.0](https://github.com/dryvist/ansible-secrets-management/compare/v0.54.1...v0.55.0) (2026-11-01)


### Features

* **openbao:** add per-agent AppRoles for the Dify fleet agents ([#410](https://github.com/dryvist/ansible-secrets-management/issues/410)) ([26debff](https://github.com/dryvist/ansible-secrets-management/commit/26debff38d31750124bb652e01e7fa4ec703b3bd))

## [0.54.1](https://github.com/dryvist/ansible-secrets-management/compare/v0.54.0...v0.54.1) (2026-11-01)


### Bug Fixes

* **authelia:** define the OpenBao UI public URL in the authelia role ([#407](https://github.com/dryvist/ansible-secrets-management/issues/407)) ([ae34e7f](https://github.com/dryvist/ansible-secrets-management/commit/ae34e7fb93ab5e8a7c246c4e5b1017861f4ed3b9))

## [0.54.0](https://github.com/dryvist/ansible-secrets-management/compare/v0.53.1...v0.54.0) (2026-11-01)


### Features

* **openbao:** add Authelia SSO login for the OpenBao UI ([#403](https://github.com/dryvist/ansible-secrets-management/issues/403)) ([0889cdc](https://github.com/dryvist/ansible-secrets-management/commit/0889cdc9b239c78d3448d9fb9aed5664abcd53a1))
* **openbao:** add per-tool sandbox AppRoles for zcode and opencode ([#402](https://github.com/dryvist/ansible-secrets-management/issues/402)) ([98af847](https://github.com/dryvist/ansible-secrets-management/commit/98af8473c4e1d01b4718e520b5f7a947d984b5b6))


### Bug Fixes

* **openbao:** drop the hermes-author-private permission set ([#401](https://github.com/dryvist/ansible-secrets-management/issues/401)) ([c8625db](https://github.com/dryvist/ansible-secrets-management/commit/c8625db67ef4a4e871b3a1836e3ba4ac80837d15))

## [0.53.1](https://github.com/dryvist/ansible-secrets-management/compare/v0.53.0...v0.53.1) (2026-11-01)


### Bug Fixes

* **openbao:** assign a dedicated agent workstation read policy ([#398](https://github.com/dryvist/ansible-secrets-management/issues/398)) ([cbc32d4](https://github.com/dryvist/ansible-secrets-management/commit/cbc32d48b141074549f4e651f510cdb0b7fb509b))

## [0.53.0](https://github.com/dryvist/ansible-secrets-management/compare/v0.52.0...v0.53.0) (2026-11-01)


### Features

* **openbao:** generate the Hermes eval profile router key ([#393](https://github.com/dryvist/ansible-secrets-management/issues/393)) ([241186a](https://github.com/dryvist/ansible-secrets-management/commit/241186a7045ca681c075c4b5368d24e34af6dec8))

## [0.52.0](https://github.com/dryvist/ansible-secrets-management/compare/v0.51.1...v0.52.0) (2026-10-31)


### Features

* **openbao:** grant converge seeding for specialist-platform evaluation instances ([#391](https://github.com/dryvist/ansible-secrets-management/issues/391)) ([13941a1](https://github.com/dryvist/ansible-secrets-management/commit/13941a1c957966b6ce1f78b5ecd3dc64c1bfe13e))

## [0.51.1](https://github.com/dryvist/ansible-secrets-management/compare/v0.51.0...v0.51.1) (2026-10-31)


### Bug Fixes

* **openbao:** rotate the converge writer secret_id on the 12h schedule ([#388](https://github.com/dryvist/ansible-secrets-management/issues/388)) ([f1561b1](https://github.com/dryvist/ansible-secrets-management/commit/f1561b18f49c0114a571be94a4ac89208e7b8d93))

## [0.51.0](https://github.com/dryvist/ansible-secrets-management/compare/v0.50.0...v0.51.0) (2026-10-31)


### Features

* **openbao:** grant the converge policy the ai/hermes-private Langfuse key record ([#385](https://github.com/dryvist/ansible-secrets-management/issues/385)) ([5c6382a](https://github.com/dryvist/ansible-secrets-management/commit/5c6382acbccad0726f126e153e7d129bb79c2974))

## [0.50.0](https://github.com/dryvist/ansible-secrets-management/compare/v0.49.2...v0.50.0) (2026-10-31)


### Features

* **openbao:** add a short-lived seed writer AppRole ([#382](https://github.com/dryvist/ansible-secrets-management/issues/382)) ([5b480ca](https://github.com/dryvist/ansible-secrets-management/commit/5b480cae8dd3ca674135e1baf0dd1b9ff0953cc7))

## [0.49.2](https://github.com/dryvist/ansible-secrets-management/compare/v0.49.1...v0.49.2) (2026-10-30)


### Bug Fixes

* **openbao:** redeem approle-secret-id-rotate from the workstation ([#377](https://github.com/dryvist/ansible-secrets-management/issues/377)) ([0a19648](https://github.com/dryvist/ansible-secrets-management/commit/0a1964853f1cf07f8389aa68e47dec67285286e3))

## [0.49.1](https://github.com/dryvist/ansible-secrets-management/compare/v0.49.0...v0.49.1) (2026-10-30)


### Bug Fixes

* **openbao:** keep the secret-age digest count after the title separator ([#375](https://github.com/dryvist/ansible-secrets-management/issues/375)) ([f15e1ae](https://github.com/dryvist/ansible-secrets-management/commit/f15e1aed5708671d00bf8fe905abc86e44a5a04a))

## [0.49.0](https://github.com/dryvist/ansible-secrets-management/compare/v0.48.1...v0.49.0) (2026-10-30)


### Features

* extend organization secret delivery configuration ([#370](https://github.com/dryvist/ansible-secrets-management/issues/370)) ([bdd82a2](https://github.com/dryvist/ansible-secrets-management/commit/bdd82a2920a9a866be482d5fe8b5f9ea3175e6aa))
* **openbao:** page when a standing AppRole secret_id nears expiry ([#340](https://github.com/dryvist/ansible-secrets-management/issues/340)) ([c9ded2f](https://github.com/dryvist/ansible-secrets-management/commit/c9ded2f61ff3f3e2a9edf4e613b36aff020d01db))


### Bug Fixes

* **openbao:** give the scheduled rotator a domain-only policy ([#371](https://github.com/dryvist/ansible-secrets-management/issues/371)) ([e834a3d](https://github.com/dryvist/ansible-secrets-management/commit/e834a3d9ea413bfd8dd5c084721f33802a6b2835))

## [0.48.1](https://github.com/dryvist/ansible-secrets-management/compare/v0.48.0...v0.48.1) (2026-10-30)


### Bug Fixes

* **openbao:** re-seed a dead host secret-zero pair only on a human-gated run ([#368](https://github.com/dryvist/ansible-secrets-management/issues/368)) ([dc81039](https://github.com/dryvist/ansible-secrets-management/commit/dc81039e6ec7e90b39b732f9b729c5db54da870d))

## [0.48.0](https://github.com/dryvist/ansible-secrets-management/compare/v0.47.1...v0.48.0) (2026-10-30)


### Features

* **openbao:** converge seed grants and hermes Home Assistant read ([#361](https://github.com/dryvist/ansible-secrets-management/issues/361)) ([885a570](https://github.com/dryvist/ansible-secrets-management/commit/885a570052bbff8feadb76e8530fc32e076f1932))
* **openbao:** run the secret-age audit daily at 06:05 UTC ([#358](https://github.com/dryvist/ansible-secrets-management/issues/358)) ([aa78a67](https://github.com/dryvist/ansible-secrets-management/commit/aa78a673b974028627af0a318a812622022f4f1f))
* **runner:** delegate run-ansible and credential publish to v5.34.0 ([#360](https://github.com/dryvist/ansible-secrets-management/issues/360)) ([072ed6d](https://github.com/dryvist/ansible-secrets-management/commit/072ed6db3e0fafabfad8817770b5b998439e658a))

## [0.47.1](https://github.com/dryvist/ansible-secrets-management/compare/v0.47.0...v0.47.1) (2026-10-26)


### Bug Fixes

* **openbao:** bind nautobot-token-publisher to the workstation CIDR class ([#355](https://github.com/dryvist/ansible-secrets-management/issues/355)) ([3b29b03](https://github.com/dryvist/ansible-secrets-management/commit/3b29b03ce863fee829f1cf3bced32e057a2661da))

## [0.47.0](https://github.com/dryvist/ansible-secrets-management/compare/v0.46.0...v0.47.0) (2026-10-26)


### Features

* **openbao:** add the inert nautobot-token-publisher AppRole and policy ([#352](https://github.com/dryvist/ansible-secrets-management/issues/352)) ([6e34592](https://github.com/dryvist/ansible-secrets-management/commit/6e345927353c491862ce25fbfef53749415b3245))
* **openbao:** grant the PBS API token path to the converge identity ([#350](https://github.com/dryvist/ansible-secrets-management/issues/350)) ([f2fe33f](https://github.com/dryvist/ansible-secrets-management/commit/f2fe33f364ade5ff4c6f5b09d33cad4cc336be20))

## [0.46.0](https://github.com/dryvist/ansible-secrets-management/compare/v0.45.1...v0.46.0) (2026-10-26)


### Features

* **openbao:** grant the Homebox service API key path ([#348](https://github.com/dryvist/ansible-secrets-management/issues/348)) ([c28040f](https://github.com/dryvist/ansible-secrets-management/commit/c28040f8fc3e2c52eaaae17950e79cd0ee06fa60))


### Bug Fixes

* **rotation:** load the caller registry so the gateway key reader rotates ([#346](https://github.com/dryvist/ansible-secrets-management/issues/346)) ([d6e20c0](https://github.com/dryvist/ansible-secrets-management/commit/d6e20c0d1f50485274a37e16d0bd61b1114f602a))

## [0.45.1](https://github.com/dryvist/ansible-secrets-management/compare/v0.45.0...v0.45.1) (2026-10-26)


### Bug Fixes

* track dependency pins with Renovate ([#312](https://github.com/dryvist/ansible-secrets-management/issues/312)) ([5058819](https://github.com/dryvist/ansible-secrets-management/commit/50588197d9d2d44cb62ab3f1899420abf96e61d0))

## [0.45.0](https://github.com/dryvist/ansible-secrets-management/compare/v0.44.1...v0.45.0) (2026-10-25)


### Features

* **openbao:** add the nautobot_backup_b2 record and its apps grant ([#341](https://github.com/dryvist/ansible-secrets-management/issues/341)) ([b34b143](https://github.com/dryvist/ansible-secrets-management/commit/b34b14335df1a4dfe7f2bc9983fb9bc25ad48066))

## [0.44.1](https://github.com/dryvist/ansible-secrets-management/compare/v0.44.0...v0.44.1) (2026-10-25)


### Bug Fixes

* **openbao:** gate rotation inventory loading on the roster-owned key reader only ([#337](https://github.com/dryvist/ansible-secrets-management/issues/337)) ([58f7315](https://github.com/dryvist/ansible-secrets-management/commit/58f731531448a3fb11823ff34a0af21bbafcca02))

## [0.44.0](https://github.com/dryvist/ansible-secrets-management/compare/v0.43.0...v0.44.0) (2026-10-25)


### Features

* **openbao_secrets:** declare consumer domain paths ([#335](https://github.com/dryvist/ansible-secrets-management/issues/335)) ([9dc2b10](https://github.com/dryvist/ansible-secrets-management/commit/9dc2b10914fc7c96ec904d223d9c1feb0103c9eb))

## [0.43.0](https://github.com/dryvist/ansible-secrets-management/compare/v0.42.1...v0.43.0) (2026-10-25)


### Features

* add a short-lived read-only SSH diagnostic identity for trusted AI ([#331](https://github.com/dryvist/ansible-secrets-management/issues/331)) ([dfa4130](https://github.com/dryvist/ansible-secrets-management/commit/dfa41304833e2b31d9654adc1e24afc2934774d1))

## [0.42.1](https://github.com/dryvist/ansible-secrets-management/compare/v0.42.0...v0.42.1) (2026-10-25)


### Bug Fixes

* **openbao:** adopt a roster owner marker when the same agent becomes a caller ([#328](https://github.com/dryvist/ansible-secrets-management/issues/328)) ([42b1c93](https://github.com/dryvist/ansible-secrets-management/commit/42b1c93a204b5e84467e1a9e22aa176a3c602376))

## [0.42.0](https://github.com/dryvist/ansible-secrets-management/compare/v0.41.1...v0.42.0) (2026-10-25)


### Features

* **openbao:** generate the lane-walk probe router key ([#326](https://github.com/dryvist/ansible-secrets-management/issues/326)) ([073970b](https://github.com/dryvist/ansible-secrets-management/commit/073970bbfa27b66e700868e232be5bb4b6239297))

## [0.41.1](https://github.com/dryvist/ansible-secrets-management/compare/v0.41.0...v0.41.1) (2026-10-25)


### Bug Fixes

* **openbao:** mark roster leaf owners with a metadata merge-patch ([#323](https://github.com/dryvist/ansible-secrets-management/issues/323)) ([dafd409](https://github.com/dryvist/ansible-secrets-management/commit/dafd409f291256f8572c0f288d1243ffbb2391ed))

## [0.41.0](https://github.com/dryvist/ansible-secrets-management/compare/v0.40.0...v0.41.0) (2026-10-25)


### Features

* **openbao:** sync the gateway key reader pair to Doppler while callers exist ([#320](https://github.com/dryvist/ansible-secrets-management/issues/320)) ([2fd4a88](https://github.com/dryvist/ansible-secrets-management/commit/2fd4a88f7cdb5c2f5fe4a6d675b71304d99ad4f9))

## [0.40.0](https://github.com/dryvist/ansible-secrets-management/compare/v0.39.0...v0.40.0) (2026-10-25)


### Features

* add Backblaze admin identity ([#309](https://github.com/dryvist/ansible-secrets-management/issues/309)) ([d0892cf](https://github.com/dryvist/ansible-secrets-management/commit/d0892cf9fd9b02243a8c93021adaa54441f99b34))
* **openbao:** add the ClickHouse ingest writer secret and its reader domain ([#317](https://github.com/dryvist/ansible-secrets-management/issues/317)) ([0e03fdd](https://github.com/dryvist/ansible-secrets-management/commit/0e03fdd45e37ed1dc37f5c1b980e2cfc4f11a905))
* **openbao:** declare the Hatchet app secrets ([#315](https://github.com/dryvist/ansible-secrets-management/issues/315)) ([c0150ed](https://github.com/dryvist/ansible-secrets-management/commit/c0150eddee27eda361698e314fc71372ad21ac04))
* **openbao:** seed gateway key leaves and policies for registry callers ([#316](https://github.com/dryvist/ansible-secrets-management/issues/316)) ([ad54478](https://github.com/dryvist/ansible-secrets-management/commit/ad54478ffdc56a86e585f6454fed0873394d98b8))


### Bug Fixes

* report AppRole logins as unchanged ([#310](https://github.com/dryvist/ansible-secrets-management/issues/310)) ([283c659](https://github.com/dryvist/ansible-secrets-management/commit/283c659fc955c59b1cbdbf0a59ad448fa7ec564e))
* scope Homebox API access through Authelia ([#313](https://github.com/dryvist/ansible-secrets-management/issues/313)) ([fcf551f](https://github.com/dryvist/ansible-secrets-management/commit/fcf551f1b490701e69646274218ce313e22aa70d))
* use the shared Molecule workflow ([#314](https://github.com/dryvist/ansible-secrets-management/issues/314)) ([ee5caf6](https://github.com/dryvist/ansible-secrets-management/commit/ee5caf6067bcef487db47e972080a9986489576e))

## [0.39.0](https://github.com/dryvist/ansible-secrets-management/compare/v0.38.0...v0.39.0) (2026-10-23)


### Features

* **openbao:** give ai-apply roles the union CIDR class ([#304](https://github.com/dryvist/ansible-secrets-management/issues/304)) ([9e38dbd](https://github.com/dryvist/ansible-secrets-management/commit/9e38dbd7e141abaedc30e0807545b83428996bc0))


### Bug Fixes

* grant read access to required media paths ([#302](https://github.com/dryvist/ansible-secrets-management/issues/302)) ([80f19c0](https://github.com/dryvist/ansible-secrets-management/commit/80f19c00cf3d83fe04f66d6f31325184f0162b64))

## [0.38.0](https://github.com/dryvist/ansible-secrets-management/compare/v0.37.0...v0.38.0) (2026-10-23)


### Features

* **openbao-secrets:** declare homebox API key pepper field ([#303](https://github.com/dryvist/ansible-secrets-management/issues/303)) ([809f05b](https://github.com/dryvist/ansible-secrets-management/commit/809f05b64bfe8e86ce365c88d91764462e8f4840))
* **openbao-secrets:** declare homebox app secrets and backup read path ([#299](https://github.com/dryvist/ansible-secrets-management/issues/299)) ([493f90f](https://github.com/dryvist/ansible-secrets-management/commit/493f90f1150b047ef2633b5f151c16705c41da88))
* **openbao-secrets:** declare homebox Backblaze B2 backup domain ([#300](https://github.com/dryvist/ansible-secrets-management/issues/300)) ([8ade271](https://github.com/dryvist/ansible-secrets-management/commit/8ade2714e97f2034ee8227e480d3c1382a432645))


### Bug Fixes

* make console credential paths optional ([#298](https://github.com/dryvist/ansible-secrets-management/issues/298)) ([d953d7c](https://github.com/dryvist/ansible-secrets-management/commit/d953d7c0e32e685b90694ef7f0b5ce03ddf48529))
* make console secret paths optional ([d953d7c](https://github.com/dryvist/ansible-secrets-management/commit/d953d7c0e32e685b90694ef7f0b5ce03ddf48529))
* **openbao-secrets:** declare media and OpenProject paths ([#297](https://github.com/dryvist/ansible-secrets-management/issues/297)) ([8c45a6d](https://github.com/dryvist/ansible-secrets-management/commit/8c45a6d70e09e4a00adafede1627ccff02913be3))

## [0.37.0](https://github.com/dryvist/ansible-secrets-management/compare/v0.36.0...v0.37.0) (2026-10-21)


### ⚠ BREAKING CHANGES

* **openbao:** drop the github-write repository allowlist ([#2528](https://github.com/dryvist/ansible-secrets-management/issues/2528))

### Features

* add GitHub agent flow identities ([7d5b714](https://github.com/dryvist/ansible-secrets-management/commit/7d5b714027b3c2602fed00272f6e3db9f0c338b4))
* **agent_sandbox:** host dispatcher with terminal sessions and a login check ([c7def81](https://github.com/dryvist/ansible-secrets-management/commit/c7def81b3fda3a9814b47e1c80568fb46c55a27e))
* **agent_sandbox:** install the pinned host dispatcher with terminal sessions ([01bc2ee](https://github.com/dryvist/ansible-secrets-management/commit/01bc2ee63917eb4e85db7ea61bf5c5f6e62c313b))
* **agent_sandbox:** provide dispatcher alert settings ([#2382](https://github.com/dryvist/ansible-secrets-management/issues/2382)) ([cc5da81](https://github.com/dryvist/ansible-secrets-management/commit/cc5da8120ecb9e3e64bc7c3a3781c86ec92aaff5))
* **authelia,openbao:** seed a UI check service user with TOTP ([bcf07ec](https://github.com/dryvist/ansible-secrets-management/commit/bcf07ec9565c1f85d813f99e770f9484af73b627))
* **authelia:** add OpenBao elevation device-code clients and elevate policy ([#24](https://github.com/dryvist/ansible-secrets-management/issues/24)) ([7fa9ed2](https://github.com/dryvist/ansible-secrets-management/commit/7fa9ed2df1dbe47c65fe3d70109bca3287a2a1c0))
* **authelia:** generate the trusted elevation client secret ([#166](https://github.com/dryvist/ansible-secrets-management/issues/166)) ([50952a9](https://github.com/dryvist/ansible-secrets-management/commit/50952a9b054890fde3e1b4d72b2089da1654b6d7))
* **authelia:** generate the trusted elevation client secret and use client_secret_basic ([5370088](https://github.com/dryvist/ansible-secrets-management/commit/5370088a97db8facfb9e7331162edc9f90a2e410))
* **config:** add exact path entries ([5663df7](https://github.com/dryvist/ansible-secrets-management/commit/5663df74122ea0b08572dba7ad322c1dd0660ff5))
* **config:** add exact path entries ([2eec5d8](https://github.com/dryvist/ansible-secrets-management/commit/2eec5d81551c564b19512cf5beca96d4d70da64f))
* **glance:** add Network + Media page and wall kiosk bypass ([#2212](https://github.com/dryvist/ansible-secrets-management/issues/2212)) ([0471738](https://github.com/dryvist/ansible-secrets-management/commit/04717381b250c60c4bcb3224e1c3661455c8dc51))
* **glance:** enable the deployment-profile tile with a generated router key ([#2449](https://github.com/dryvist/ansible-secrets-management/issues/2449)) ([177c3a5](https://github.com/dryvist/ansible-secrets-management/commit/177c3a54e34b583fbb30e0ac78c057e795fe48c0))
* **homarr:** add the homarr-v2 instance with declarative boards ([#2278](https://github.com/dryvist/ansible-secrets-management/issues/2278)) ([2bc7b39](https://github.com/dryvist/ansible-secrets-management/commit/2bc7b39490c9bda8613ec0d337330c077c5a8519))
* **ntfy:** fan every topic out to one all-alerts Slack channel ([#2276](https://github.com/dryvist/ansible-secrets-management/issues/2276)) ([d7128d5](https://github.com/dryvist/ansible-secrets-management/commit/d7128d5ca0373d68d83590a6d0f843e59aaa86f1))
* **ntfy:** provision a publish-only ai-jobs token ([6890f01](https://github.com/dryvist/ansible-secrets-management/commit/6890f0194f14d6d75e060db1fe8b973c0dd68ae4))
* **ntfy:** provision a publish-only ai-jobs token ([45f1508](https://github.com/dryvist/ansible-secrets-management/commit/45f15083a501a21be83aa3895fdba05e595e5d38))
* **object_storage:** mint scoped per-bucket RustFS IAM credentials ([#2200](https://github.com/dryvist/ansible-secrets-management/issues/2200)) ([0b53919](https://github.com/dryvist/ansible-secrets-management/commit/0b5391969f3ec183f01e78add71b30c0c6741f94))
* **openbao_secrets:** add PostgreSQL backup S3 domain ([#272](https://github.com/dryvist/ansible-secrets-management/issues/272)) ([eb0646a](https://github.com/dryvist/ansible-secrets-management/commit/eb0646a752c2fc6be41ed78273d59cb224358966))
* **openbao_secrets:** drop owned MCP paths from non-owner fetch domains ([6eda816](https://github.com/dryvist/ansible-secrets-management/commit/6eda81668a11e89646ab0dde5e84ac3be6626a70))
* **openbao_secrets:** drop owned MCP paths from non-owner fetch domains ([#78](https://github.com/dryvist/ansible-secrets-management/issues/78)) ([499d28d](https://github.com/dryvist/ansible-secrets-management/commit/499d28dedcc3b6c27a994cb0f24209ca324ca1aa))
* **openbao:** accept a pre-issued rotator token in the rotation play ([#2363](https://github.com/dryvist/ansible-secrets-management/issues/2363)) ([b339e98](https://github.com/dryvist/ansible-secrets-management/commit/b339e9840e6eabba79d687fe67343549d5f3e006))
* **openbao:** add a github-personal App mount with one write set ([#251](https://github.com/dryvist/ansible-secrets-management/issues/251)) ([96bcd1d](https://github.com/dryvist/ansible-secrets-management/commit/96bcd1d1d45fb5ac6ed636afb7cd2e56df2e3aac))
* **openbao:** add a tofu-state transit AppRole ([#234](https://github.com/dryvist/ansible-secrets-management/issues/234)) ([0127a07](https://github.com/dryvist/ansible-secrets-management/commit/0127a0782bc0f7814cd87604fc4bd7608edeaf06))
* **openbao:** add a work-admin permission set ([#183](https://github.com/dryvist/ansible-secrets-management/issues/183)) ([d0a5af4](https://github.com/dryvist/ansible-secrets-management/commit/d0a5af46103fab0b847977d7774fe62e5fbb8ce3))
* **openbao:** add a workstation-bound tofu-state transit AppRole ([0127a07](https://github.com/dryvist/ansible-secrets-management/commit/0127a0782bc0f7814cd87604fc4bd7608edeaf06))
* **openbao:** add agent-ssh-sign AppRole for workstation SSH signing ([#2359](https://github.com/dryvist/ansible-secrets-management/issues/2359)) ([78652e1](https://github.com/dryvist/ansible-secrets-management/commit/78652e17fb99090ff72c927d506a70ab330dd148))
* **openbao:** add azure secrets engine with roles from environment ([#88](https://github.com/dryvist/ansible-secrets-management/issues/88)) ([1242bf2](https://github.com/dryvist/ansible-secrets-management/commit/1242bf2bd980218d54200e6d467d4432c5e1177c))
* **openbao:** add bounded admin session role ([a56d9e6](https://github.com/dryvist/ansible-secrets-management/commit/a56d9e67d14d68aac748a106e6dc25aa3df25a89))
* **openbao:** add Cribl Edge generated fields and readers ([#2386](https://github.com/dryvist/ansible-secrets-management/issues/2386)) ([a6ef6ba](https://github.com/dryvist/ansible-secrets-management/commit/a6ef6bafd87f5825f1d9b9095d6f9dbc7713c6a0))
* **openbao:** add GitHub Enterprise App mounts and inert tiers ([#30](https://github.com/dryvist/ansible-secrets-management/issues/30)) ([278493a](https://github.com/dryvist/ansible-secrets-management/commit/278493a9e3732616fa41d0160465ac37b3830268))
* **openbao:** add github-hermes App mount with visibility-split sets ([#2284](https://github.com/dryvist/ansible-secrets-management/issues/2284)) ([043f741](https://github.com/dryvist/ansible-secrets-management/commit/043f7412588953deb8fd8df8d912ea9344668c5d))
* **openbao:** add github-runner mount for runner registration by org ([#225](https://github.com/dryvist/ansible-secrets-management/issues/225)) ([79b42b8](https://github.com/dryvist/ansible-secrets-management/commit/79b42b89f9e1a82b2f90959549b60d07a3ef5e85))
* **openbao:** add github-work App mount, policy and AppRole ([0601245](https://github.com/dryvist/ansible-secrets-management/commit/0601245dfb0e40c267eaee884d7cda8d7dec4cf8))
* **openbao:** add github-work App mount, policy and AppRole ([09d9251](https://github.com/dryvist/ansible-secrets-management/commit/09d925190958c83e970ecc6b3fac0d6839312579))
* **openbao:** add Hermes configuration ([#2379](https://github.com/dryvist/ansible-secrets-management/issues/2379)) ([5314292](https://github.com/dryvist/ansible-secrets-management/commit/531429297e6b38c5604ba33f35e35430bb48f99d))
* **openbao:** add local-llm-workstation AppRole for workstation reads ([#2352](https://github.com/dryvist/ansible-secrets-management/issues/2352)) ([be55ae3](https://github.com/dryvist/ansible-secrets-management/commit/be55ae32b455ac76295805313a3288eda83b80ca))
* **openbao:** add owner-neutral GitHub token grants ([#163](https://github.com/dryvist/ansible-secrets-management/issues/163)) ([6270354](https://github.com/dryvist/ansible-secrets-management/commit/627035489ce67a6bfeac15c38be6ce3baea3f129))
* **openbao:** add per-engine component tags ([94b12ee](https://github.com/dryvist/ansible-secrets-management/commit/94b12ee10847db896781b8d12af369df99e71e06))
* **openbao:** add per-engine component tags ([#105](https://github.com/dryvist/ansible-secrets-management/issues/105)) ([a883ff2](https://github.com/dryvist/ansible-secrets-management/commit/a883ff2eba591796c68c28ac23bdb4555478acf2))
* **openbao:** add per-organisation repo-create permission sets ([7742019](https://github.com/dryvist/ansible-secrets-management/commit/7742019de807a0ce1fdd7f51f4cf432a2a88b384))
* **openbao:** add per-organisation repo-create permission sets ([#123](https://github.com/dryvist/ansible-secrets-management/issues/123)) ([1ea7e1a](https://github.com/dryvist/ansible-secrets-management/commit/1ea7e1af92f713b8056b88c8187d6dcc4d2043ad))
* **openbao:** add router and gateway reader roles for roster agent keys ([#75](https://github.com/dryvist/ansible-secrets-management/issues/75)) ([39f1a6e](https://github.com/dryvist/ansible-secrets-management/commit/39f1a6ede05ea360d6db6b64684b3242e23a79fd))
* **openbao:** add sandbox agent AppRoles and identity classes ([#128](https://github.com/dryvist/ansible-secrets-management/issues/128)) ([1fbcca7](https://github.com/dryvist/ansible-secrets-management/commit/1fbcca78cf78532177dde2ebe3ed9cbce6fdd99c))
* **openbao:** add sandbox agent roles ([dd51987](https://github.com/dryvist/ansible-secrets-management/commit/dd5198763a084cecabffa8f1f229688270ff0a5c))
* **openbao:** add ssh host-cert signing role ([#2203](https://github.com/dryvist/ansible-secrets-management/issues/2203)) ([3e9cbc4](https://github.com/dryvist/ansible-secrets-management/commit/3e9cbc4f54bf35726518cd206d1db80c41164700))
* **openbao:** add the ai-admin-guard deny overlay ([4b13726](https://github.com/dryvist/ansible-secrets-management/commit/4b137261d56e20bce67011145c75ffeae34aef06))
* **openbao:** add the Authelia JWT elevation roles and a 1h work-identity token ([#25](https://github.com/dryvist/ansible-secrets-management/issues/25)) ([7127d8b](https://github.com/dryvist/ansible-secrets-management/commit/7127d8b0dac6dbe1b7c458fb11569cbcec99c242))
* **openbao:** add the azure-iac-admin AppRole and policy ([6d58f66](https://github.com/dryvist/ansible-secrets-management/commit/6d58f66887276a535d6552ddd13a5066dd1b6824))
* **openbao:** add the azure-iac-admin AppRole and policy ([#119](https://github.com/dryvist/ansible-secrets-management/issues/119)) ([e2e5065](https://github.com/dryvist/ansible-secrets-management/commit/e2e5065a388f861d480ff9a2a0d7a6f499808a32))
* **openbao:** add the ci-resolver GitHub identity ([#53](https://github.com/dryvist/ansible-secrets-management/issues/53)) ([7eca696](https://github.com/dryvist/ansible-secrets-management/commit/7eca69625ada89e662c8de7fe170921e69988ac3))
* **openbao:** add the clickhouse resource domain ([#100](https://github.com/dryvist/ansible-secrets-management/issues/100)) ([2c60338](https://github.com/dryvist/ansible-secrets-management/commit/2c60338b8e222a63e7af6025192289d8b939dc44))
* **openbao:** add the docs router snapshot key, set and OIDC role ([#2505](https://github.com/dryvist/ansible-secrets-management/issues/2505)) ([551e4d9](https://github.com/dryvist/ansible-secrets-management/commit/551e4d922bd93066dc080982300a9996bb6696cf))
* **openbao:** add the github-enterprise-owner mount and the ai-admin-guard overlay ([#48](https://github.com/dryvist/ansible-secrets-management/issues/48)) ([a1b7dc6](https://github.com/dryvist/ansible-secrets-management/commit/a1b7dc66bb398fde7408478b08ebd0be2c0db5e7))
* **openbao:** add the github-enterprise-owner token mount ([e4f413b](https://github.com/dryvist/ansible-secrets-management/commit/e4f413b8c585926c9f8e37a77fb5af7c55ea7832))
* **openbao:** add the herdr-hail workstation AppRole ([#168](https://github.com/dryvist/ansible-secrets-management/issues/168)) ([a19574a](https://github.com/dryvist/ansible-secrets-management/commit/a19574ab5ce61bad9c9690aea662d1fd2f8511b0))
* **openbao:** add the hermes orchestrator generated app secret ([#129](https://github.com/dryvist/ansible-secrets-management/issues/129)) ([dba4b84](https://github.com/dryvist/ansible-secrets-management/commit/dba4b84927d706a3cc32fafaebe764bc4ef97f62))
* **openbao:** add the litellm-local-workstation generated field ([69af118](https://github.com/dryvist/ansible-secrets-management/commit/69af118134aa27b02331c73cb6ad9904febcb615))
* **openbao:** add the work-admin GitHub tier ([d0a5af4](https://github.com/dryvist/ansible-secrets-management/commit/d0a5af46103fab0b847977d7774fe62e5fbb8ce3))
* **openbao:** add tofu-state transit paths to terraform-apply policy ([#218](https://github.com/dryvist/ansible-secrets-management/issues/218)) ([3c0c019](https://github.com/dryvist/ansible-secrets-management/commit/3c0c0195d1330db7d72d0ae96f38be7314995379))
* **openbao:** add tofu-state transit paths to the ai-admin policy ([#220](https://github.com/dryvist/ansible-secrets-management/issues/220)) ([8d05b4e](https://github.com/dryvist/ansible-secrets-management/commit/8d05b4edc1f5da3cf8c0d8c2b6a9d8fbf273c4bd))
* **openbao:** add transit paths to the reconcile policy ([#219](https://github.com/dryvist/ansible-secrets-management/issues/219)) ([a98bc52](https://github.com/dryvist/ansible-secrets-management/commit/a98bc529590d62f32b2b38ca348222bb5acee27b))
* **openbao:** admin set and Terrakube identity per GitHub org ([#190](https://github.com/dryvist/ansible-secrets-management/issues/190)) ([76e5263](https://github.com/dryvist/ansible-secrets-management/commit/76e5263e0f59e8233631e8a1d4171518d0e73d74))
* **openbao:** allow a permissions map on github/token write mints ([84ec5f9](https://github.com/dryvist/ansible-secrets-management/commit/84ec5f98ee3b55c9f133974c169247592b70b4dd))
* **openbao:** allow a permissions map on github/token write mints ([4f2a088](https://github.com/dryvist/ansible-secrets-management/commit/4f2a088f082d392c278741aa70c80b23035b7e62))
* **openbao:** allow fan-control write credential publication ([d130c4c](https://github.com/dryvist/ansible-secrets-management/commit/d130c4cbe57ef65c0ce88f1c524d5084ddcc12f5))
* **openbao:** allow terraform-apply to use the tofu-state transit key ([3c0c019](https://github.com/dryvist/ansible-secrets-management/commit/3c0c0195d1330db7d72d0ae96f38be7314995379))
* **openbao:** allow workflow file writes in the work write set ([#176](https://github.com/dryvist/ansible-secrets-management/issues/176)) ([24d78a0](https://github.com/dryvist/ansible-secrets-management/commit/24d78a0bd9adf2d29541e6abb25e9a03ee6060cf))
* **openbao:** attach the ai-apply-all policy set to agent-workstation ([#22](https://github.com/dryvist/ansible-secrets-management/issues/22)) ([b0c948c](https://github.com/dryvist/ansible-secrets-management/commit/b0c948c2c31f1e4a0dd547cb90d4cc34055ae6a1))
* **openbao:** bind the tofu-github role to per-org workspaces ([#202](https://github.com/dryvist/ansible-secrets-management/issues/202)) ([8a7e804](https://github.com/dryvist/ansible-secrets-management/commit/8a7e8046ad96ad395dc45048f27c5b31a70b80c5))
* **openbao:** classify declared AppRoles ([8f46148](https://github.com/dryvist/ansible-secrets-management/commit/8f461481b44346e16e7ef8b20fb16ce77a12d995))
* **openbao:** configure the Azure engine like the AWS engine ([697e64e](https://github.com/dryvist/ansible-secrets-management/commit/697e64e94e7c8e1c409bdc82fa366e05e5359354))
* **openbao:** configure the Azure secrets engine ([#93](https://github.com/dryvist/ansible-secrets-management/issues/93)) ([3eb1f05](https://github.com/dryvist/ansible-secrets-management/commit/3eb1f05abf60cb5564c4bab44df3216d455eb888))
* **openbao:** declare disclosure-denylist secret path and read policy ([#2177](https://github.com/dryvist/ansible-secrets-management/issues/2177)) ([7a975b7](https://github.com/dryvist/ansible-secrets-management/commit/7a975b799aa73b71b35697c9ecfdd872528f7600))
* **openbao:** declare transit mount and tofu-state key ([#216](https://github.com/dryvist/ansible-secrets-management/issues/216)) ([1494f59](https://github.com/dryvist/ansible-secrets-management/commit/1494f59c347368f8d54e6af68fde67da4879da61))
* **openbao:** define the untrusted dispatcher tier ([63ce58b](https://github.com/dryvist/ansible-secrets-management/commit/63ce58b65474cf1349f38f7cd836579e38b79694))
* **openbao:** derive roster agent AppRoles and policies ([#73](https://github.com/dryvist/ansible-secrets-management/issues/73)) ([deaaf89](https://github.com/dryvist/ansible-secrets-management/commit/deaaf898e1d8ecae6a21bc0aaaf7ff487c038699))
* **openbao:** derive the github-work read set and mint write from the App grant ([#289](https://github.com/dryvist/ansible-secrets-management/issues/289)) ([05a5e4a](https://github.com/dryvist/ansible-secrets-management/commit/05a5e4a226f317dffa86bb481cd728da065f6124))
* **openbao:** drop consumer MCP grants once a roster agent owns the system ([96faa17](https://github.com/dryvist/ansible-secrets-management/commit/96faa174a0e9e985c614953d939b7726a7d21d95))
* **openbao:** drop consumer MCP grants once a roster agent owns the system ([#77](https://github.com/dryvist/ansible-secrets-management/issues/77)) ([5322ffb](https://github.com/dryvist/ansible-secrets-management/commit/5322ffb6e4b681c389d173e0d3c918bf61b47c3d))
* **openbao:** drop the github-write repository allowlist ([#2528](https://github.com/dryvist/ansible-secrets-management/issues/2528)) ([3cecb78](https://github.com/dryvist/ansible-secrets-management/commit/3cecb7860325c3c2a18fe2e62f0f7492537444d6))
* **openbao:** extend Hermes rotation and Context7 configuration ([#2332](https://github.com/dryvist/ansible-secrets-management/issues/2332)) ([2137e49](https://github.com/dryvist/ansible-secrets-management/commit/2137e49f61567308ed86db9d7bc6c3ccb6c006d6))
* **openbao:** extend publisher app catalog ([#192](https://github.com/dryvist/ansible-secrets-management/issues/192)) ([d130c4c](https://github.com/dryvist/ansible-secrets-management/commit/d130c4cbe57ef65c0ce88f1c524d5084ddcc12f5))
* **openbao:** generate a litellm-local-workstation router-key secret ([d667131](https://github.com/dryvist/ansible-secrets-management/commit/d667131d6a31586629572c1666ffe35f5ff7003e))
* **openbao:** generate a litellm-local-workstation router-key secret ([#2237](https://github.com/dryvist/ansible-secrets-management/issues/2237)) ([ba42db2](https://github.com/dryvist/ansible-secrets-management/commit/ba42db23b111c0a2b55103e31c4653dd9c750234))
* **openbao:** generate an A2A bearer token for the assistant guest ([eab9d97](https://github.com/dryvist/ansible-secrets-management/commit/eab9d97c8ad795574ae23c8883a7cf44d709bd85))
* **openbao:** generate an A2A bearer token for the assistant guest ([#70](https://github.com/dryvist/ansible-secrets-management/issues/70)) ([1539774](https://github.com/dryvist/ansible-secrets-management/commit/1539774706d7f0fb6cb2edb7ff739ceb761f66df))
* **openbao:** generate hermes_login_password for the vikunja app secret ([7fc49ac](https://github.com/dryvist/ansible-secrets-management/commit/7fc49acce32bd634d623544fd7e7e650b7bc6011))
* **openbao:** generate hermes_login_password for the vikunja app secret ([3c3f64a](https://github.com/dryvist/ansible-secrets-management/commit/3c3f64a0135846c9e849a2b5f3d84c0afa99edec))
* **openbao:** generate hindsight_api_key in apps/hindsight ([#2354](https://github.com/dryvist/ansible-secrets-management/issues/2354)) ([d5db8f9](https://github.com/dryvist/ansible-secrets-management/commit/d5db8f9b0dacdc6d70d6d50472cce61b6b3a0874))
* **openbao:** generate laya and decisions router secrets ([967dccd](https://github.com/dryvist/ansible-secrets-management/commit/967dccd77b099c8e6ef9d76f42fa9b6a2865715b))
* **openbao:** generate the codex-local router key ([#143](https://github.com/dryvist/ansible-secrets-management/issues/143)) ([b1979df](https://github.com/dryvist/ansible-secrets-management/commit/b1979dfbe579ee41f1b62e3030895c48089597e0))
* **openbao:** generate two router application secrets ([#155](https://github.com/dryvist/ansible-secrets-management/issues/155)) ([967dccd](https://github.com/dryvist/ansible-secrets-management/commit/967dccd77b099c8e6ef9d76f42fa9b6a2865715b))
* **openbao:** give the sandbox router key its own leaf ([#242](https://github.com/dryvist/ansible-secrets-management/issues/242)) ([de429e3](https://github.com/dryvist/ansible-secrets-management/commit/de429e32948d91b56c7296a821954a2254d15188))
* **openbao:** grant apps reads for console credentials ([#291](https://github.com/dryvist/ansible-secrets-management/issues/291)) ([a8afda3](https://github.com/dryvist/ansible-secrets-management/commit/a8afda3e558d5cfc3dd1c827703de4fcb1348a59))
* **openbao:** grant observability read on the OpenRouter usage key ([#2357](https://github.com/dryvist/ansible-secrets-management/issues/2357)) ([ecb22df](https://github.com/dryvist/ansible-secrets-management/commit/ecb22df15903d8afadc5c792ac14651b8fd69d23))
* **openbao:** grant read-only Splunk MCP access ([7e5d255](https://github.com/dryvist/ansible-secrets-management/commit/7e5d2558b46ff30d12c137e8d286988ac417a29c))
* **openbao:** grant read-only Splunk MCP access ([573a5cc](https://github.com/dryvist/ansible-secrets-management/commit/573a5cca9897b9e07baf06e6b9fb9bec6a5022b5))
* **openbao:** grant the apps read for the hermes orchestrator leaf ([a679589](https://github.com/dryvist/ansible-secrets-management/commit/a6795893cc95d850d049aaf3d24eb4e06d91ec74))
* **openbao:** grant the pve-exporter token publish path ([#2323](https://github.com/dryvist/ansible-secrets-management/issues/2323)) ([e2d66fb](https://github.com/dryvist/ansible-secrets-management/commit/e2d66fb3413dc353286949a80b0f39d5339722f1))
* **openbao:** isolate owned MCP access in dedicated local-llm policies ([#136](https://github.com/dryvist/ansible-secrets-management/issues/136)) ([ec5b9b2](https://github.com/dryvist/ansible-secrets-management/commit/ec5b9b2d62e386866dc0b85aed6daef4a1f6c617))
* **openbao:** keep plugin staging tasks unchanged ([446d55d](https://github.com/dryvist/ansible-secrets-management/commit/446d55d3461eb12313d47aaa3af9e03542cfe487))
* **openbao:** leave installation_id unpinned in the write policies ([#83](https://github.com/dryvist/ansible-secrets-management/issues/83)) ([91bb0a2](https://github.com/dryvist/ansible-secrets-management/commit/91bb0a25898a9f13f74e4916336bc8b71c5c9b3c))
* **openbao:** leave installation_id unpinned in the write policies ([#83](https://github.com/dryvist/ansible-secrets-management/issues/83)) ([e1f8f0f](https://github.com/dryvist/ansible-secrets-management/commit/e1f8f0fadb2f41b3a934374523b385d1bf858823))
* **openbao:** let the converge identity publish the open-llm bucket ([b751078](https://github.com/dryvist/ansible-secrets-management/commit/b751078e4158b2e43ba941007192ddde84508531))
* **openbao:** let the converge identity publish the open-llm bucket ([d2a956c](https://github.com/dryvist/ansible-secrets-management/commit/d2a956c76c44aebf4c409792409b7b84bf0227ff))
* **openbao:** let the sandbox write role read the sandbox leaf ([#204](https://github.com/dryvist/ansible-secrets-management/issues/204)) ([255b9f4](https://github.com/dryvist/ansible-secrets-management/commit/255b9f4df361a8c83e4a52c8e5057912bf0ceaee))
* **openbao:** let the semaphore role mint the jpe-cribl read token ([#142](https://github.com/dryvist/ansible-secrets-management/issues/142)) ([296a0c7](https://github.com/dryvist/ansible-secrets-management/commit/296a0c786bf86323aa070374f596e012f516172a))
* **openbao:** let the telemetry identity mint the read map ([#188](https://github.com/dryvist/ansible-secrets-management/issues/188)) ([f3c9416](https://github.com/dryvist/ansible-secrets-management/commit/f3c94160d96266e44bfca09f11ffcf471db0ff65))
* **openbao:** mint agents tokens by org name and read two role IDs ([#157](https://github.com/dryvist/ansible-secrets-management/issues/157)) ([b44409e](https://github.com/dryvist/ansible-secrets-management/commit/b44409eb9060e32d39965e4cdd2bf12ecb8acfa6))
* **openbao:** OIDC role for the central AI review workflow ([#191](https://github.com/dryvist/ansible-secrets-management/issues/191)) ([0af4708](https://github.com/dryvist/ansible-secrets-management/commit/0af470829e3fbe7c088f29f1e154d06fe1ff2da4))
* **openbao:** one-approval phone unlock for policy sync ([#223](https://github.com/dryvist/ansible-secrets-management/issues/223)) ([40f5fb1](https://github.com/dryvist/ansible-secrets-management/commit/40f5fb18d44c6f7a69b5c3163d574472bc4d834a))
* **openbao:** pinned read-only token mint in the exporter policy ([#194](https://github.com/dryvist/ansible-secrets-management/issues/194)) ([7f9e347](https://github.com/dryvist/ansible-secrets-management/commit/7f9e347a3bf335e41390dd61505266be6c39a15b))
* **openbao:** pinned reconcile attachments for two human-gated roles ([#269](https://github.com/dryvist/ansible-secrets-management/issues/269)) ([b23e670](https://github.com/dryvist/ansible-secrets-management/commit/b23e67028dfb88c178d8cd07dce60f4fe222aec8))
* **openbao:** port six ansible-proxmox-apps commits ([5ab3a03](https://github.com/dryvist/ansible-secrets-management/commit/5ab3a03dc1936310b89f94b1e4281f6fc36f5cfe))
* **openbao:** preserve owner MCP paths in fetch domains ([#132](https://github.com/dryvist/ansible-secrets-management/issues/132)) ([af5921a](https://github.com/dryvist/ansible-secrets-management/commit/af5921a4acfc56176dae8a77311c4f87ca3f990b))
* **openbao:** provision Qwen Code router key ([#66](https://github.com/dryvist/ansible-secrets-management/issues/66)) ([1d9b9fb](https://github.com/dryvist/ansible-secrets-management/commit/1d9b9fb6c71fec6c5a08b8eefe100ec8c78c93c2))
* **openbao:** report a missing Azure engine root config ([240169b](https://github.com/dryvist/ansible-secrets-management/commit/240169b12407ddc43327001b434c014d5005b1c3))
* **openbao:** rotate the agent-workstation secret_id on the domain schedule ([#41](https://github.com/dryvist/ansible-secrets-management/issues/41)) ([fa5bc47](https://github.com/dryvist/ansible-secrets-management/commit/fa5bc4772f05bb1a33d8abed9de81c8bed57371c))
* **openbao:** rotate the open-llm secret_id on the scheduled cadence ([#2356](https://github.com/dryvist/ansible-secrets-management/issues/2356)) ([b72d162](https://github.com/dryvist/ansible-secrets-management/commit/b72d162c94ada61b2ca0f6289419f95291c931c8))
* **openbao:** scope GitHub org secrets to a Terrakube workspace ([#237](https://github.com/dryvist/ansible-secrets-management/issues/237)) ([c332c91](https://github.com/dryvist/ansible-secrets-management/commit/c332c91f860ab801f4cfdd32905dc0096ddbcb38))
* **openbao:** seed per-agent router and gateway keys outside the apps grant ([#74](https://github.com/dryvist/ansible-secrets-management/issues/74)) ([243deb1](https://github.com/dryvist/ansible-secrets-management/commit/243deb1cdbbf4817a2da90d5d3f4293ac08b9ae0))
* **openbao:** seed sandbox and Claude router keys ([bed9ce4](https://github.com/dryvist/ansible-secrets-management/commit/bed9ce4fbce19f0ef78267d37bd5412e2d2d1c29))
* **openbao:** separate Azure IaC admin AppRole policies ([#135](https://github.com/dryvist/ansible-secrets-management/issues/135)) ([76c8560](https://github.com/dryvist/ansible-secrets-management/commit/76c8560b1ccd3186fc49d89a45c12900c4dc60bb))
* **openbao:** serve extra installations on the everyday GitHub mount ([#65](https://github.com/dryvist/ansible-secrets-management/issues/65)) ([cdc383e](https://github.com/dryvist/ansible-secrets-management/commit/cdc383e3d34cee6cd115253e2ea7eea10d7a136d))
* **openbao:** split dispatcher and sandbox secrets ([3b0308a](https://github.com/dryvist/ansible-secrets-management/commit/3b0308a6010fc4f064edacc4afef7ffb2f26f071))
* **openbao:** split GitHub engine mounts per App ([#2080](https://github.com/dryvist/ansible-secrets-management/issues/2080)) ([70d3891](https://github.com/dryvist/ansible-secrets-management/commit/70d3891b72ab798e29b8b48378731097cde740de))
* **openbao:** split github-work into read and write identities ([#2523](https://github.com/dryvist/ansible-secrets-management/issues/2523)) ([d7933e5](https://github.com/dryvist/ansible-secrets-management/commit/d7933e50ad2e60e91e3aa365a414841fab3e9302))
* **openbao:** use installation scope for general write tokens ([becae0a](https://github.com/dryvist/ansible-secrets-management/commit/becae0a305481104e45eb9b0f797e541e79489f8))
* **openbao:** use installation scope for general write tokens ([d94a45d](https://github.com/dryvist/ansible-secrets-management/commit/d94a45d9c8a94c58926648cafe73d9785c737d11))
* **openbao:** use per-call AppRole credentials ([#2437](https://github.com/dryvist/ansible-secrets-management/issues/2437)) ([152dc90](https://github.com/dryvist/ansible-secrets-management/commit/152dc905d46954f207fcb7e50b3947fd4fe68c37))
* **openbao:** validate GitHub App webhook and installation settings ([#2107](https://github.com/dryvist/ansible-secrets-management/issues/2107)) ([f376a49](https://github.com/dryvist/ansible-secrets-management/commit/f376a49e71b25253271989c2a37b3b0c22268988))
* **postgres:** optional Patroni/etcd HA mode behind postgres_ha_manager ([#2189](https://github.com/dryvist/ansible-secrets-management/issues/2189)) ([d17d540](https://github.com/dryvist/ansible-secrets-management/commit/d17d5402bcb489cf82630ae746abed2945714103))
* scaffold the secrets_management collection ([#1](https://github.com/dryvist/ansible-secrets-management/issues/1)) ([99308cf](https://github.com/dryvist/ansible-secrets-management/commit/99308cf2110d665a995a0cdcf1090a8bc4b92d66))
* schedule reconcile rotation ([ec0e531](https://github.com/dryvist/ansible-secrets-management/commit/ec0e53158f21219d2d17c24653f71f43ddf878b4))
* **scripts:** add a run wrapper for the controller-side playbooks ([#26](https://github.com/dryvist/ansible-secrets-management/issues/26)) ([f638da2](https://github.com/dryvist/ansible-secrets-management/commit/f638da2690b05571331a1c62e23235c1fb75afcb))
* shared ProxMan cluster ingress, DNS ownership, and workstation connection profile ([#2272](https://github.com/dryvist/ansible-secrets-management/issues/2272)) ([6c67a1e](https://github.com/dryvist/ansible-secrets-management/commit/6c67a1ec52e866aa7bdab9e2e5d053d4a0d64de4))
* **unpoller:** native poller + Cribl scrape + OpenBao credential ([#2174](https://github.com/dryvist/ansible-secrets-management/issues/2174)) ([468ada6](https://github.com/dryvist/ansible-secrets-management/commit/468ada6c932dc4aac6c2b23f9d7ff959f9978585))
* **vikunja:** provision the AI Jobs dispatcher token ([cce1b9b](https://github.com/dryvist/ansible-secrets-management/commit/cce1b9b761008cf6976e8a383c5d8b022033eb60))
* **vikunja:** provision the AI Jobs dispatcher token ([2464893](https://github.com/dryvist/ansible-secrets-management/commit/24648938052014cf0fa2d32af95bdc8c810ee09e))
* **wall:** serve the server-room wall ([#2139](https://github.com/dryvist/ansible-secrets-management/issues/2139)) ([4415583](https://github.com/dryvist/ansible-secrets-management/commit/4415583de001ab9aec4ea6c15be186143650be8b))
* **zammad,cribl_edge:** Security IDS group, svc-cribl identity, Edge IDS wiring ([#2257](https://github.com/dryvist/ansible-secrets-management/issues/2257)) ([1eea82d](https://github.com/dryvist/ansible-secrets-management/commit/1eea82d01701986b806296f83862b5167c9e1e9d))


### Bug Fixes

* align the domain catalog ([3b5aa10](https://github.com/dryvist/ansible-secrets-management/commit/3b5aa10965dd41c714bdbf62d4bb37cde0be0a1e))
* assert the single benchmark router key ([#2479](https://github.com/dryvist/ansible-secrets-management/issues/2479)) ([31c5ceb](https://github.com/dryvist/ansible-secrets-management/commit/31c5cebfe3bbb9dcdf11d8b982d7790206fe4d99))
* **authelia:** run controller-side staging under check mode ([#276](https://github.com/dryvist/ansible-secrets-management/issues/276)) ([eee1cce](https://github.com/dryvist/ansible-secrets-management/commit/eee1cce2530b58fe3f8dc39490aa95c79ee48589))
* **authelia:** size the token-endpoint rate limit for device-code polling ([f9e8776](https://github.com/dryvist/ansible-secrets-management/commit/f9e8776b7a28091d18a2ac25fa3e09002b9eb95f))
* **authelia:** size the token-endpoint rate limit for device-code polling ([#210](https://github.com/dryvist/ansible-secrets-management/issues/210)) ([fe1ecc2](https://github.com/dryvist/ansible-secrets-management/commit/fe1ecc2d09c61b192d77c81a1c34c45aca1078c8))
* **authelia:** strip the Digest prefix from service-user hashes ([#2222](https://github.com/dryvist/ansible-secrets-management/issues/2222)) ([81cd257](https://github.com/dryvist/ansible-secrets-management/commit/81cd25793c9299a1178d17ccd86757a2d037c54d))
* **authelia:** use a token-endpoint bucket period Authelia accepts ([#212](https://github.com/dryvist/ansible-secrets-management/issues/212)) ([e1fece7](https://github.com/dryvist/ansible-secrets-management/commit/e1fece7e564ce294e8aff1116544b43d8df80917))
* **auth:** parameterize role defaults ([#2443](https://github.com/dryvist/ansible-secrets-management/issues/2443)) ([1d1649f](https://github.com/dryvist/ansible-secrets-management/commit/1d1649f846ead60e78e9dcdb4050e89057f4e7e7))
* bound scheduled rotation catalog ([#2399](https://github.com/dryvist/ansible-secrets-management/issues/2399)) ([61fb541](https://github.com/dryvist/ansible-secrets-management/commit/61fb54150d94001ea0e303d57e24b6524422b7f1))
* bound scheduled rotation catalog ([#2399](https://github.com/dryvist/ansible-secrets-management/issues/2399)) ([bdfeaeb](https://github.com/dryvist/ansible-secrets-management/commit/bdfeaeb7f6b8d27fbb793d1756332d01ccf6422d))
* build router key paths from the consumer catalog ([7761562](https://github.com/dryvist/ansible-secrets-management/commit/7761562084a5252475d415541ee562eab506c2fe))
* **ci:** hold the workflow Python at 3.14 ([#205](https://github.com/dryvist/ansible-secrets-management/issues/205)) ([c89fbec](https://github.com/dryvist/ansible-secrets-management/commit/c89fbecd9e3cbbdb8118ea08686b5c118380cb52))
* **cribl_stream:** take openbao audit `_time` from the record ([#2516](https://github.com/dryvist/ansible-secrets-management/issues/2516)) ([a748e51](https://github.com/dryvist/ansible-secrets-management/commit/a748e51cd0c0f8dd076e5182f2703a935004f6f1))
* **deps:** require amazon.aws 11.3.0 or newer ([#259](https://github.com/dryvist/ansible-secrets-management/issues/259)) ([b900e5c](https://github.com/dryvist/ansible-secrets-management/commit/b900e5cefec98c29a160e2fd38024f3bf4b7f72b))
* **deps:** require amazon.aws for the published inventory resolver ([39c8fcc](https://github.com/dryvist/ansible-secrets-management/commit/39c8fcc933e2d7f90f12dc99e5d1192384fbd70b))
* **disclosure:** reword sensitive-category terms in comments and docs ([#2182](https://github.com/dryvist/ansible-secrets-management/issues/2182)) ([0ca9bff](https://github.com/dryvist/ansible-secrets-management/commit/0ca9bffe8c42635aeb4db34b443317643762b170))
* generate router keys through shared catalog ([#2474](https://github.com/dryvist/ansible-secrets-management/issues/2474)) ([3a109ab](https://github.com/dryvist/ansible-secrets-management/commit/3a109ab4abbdd3124447d0975002fd8249102c4c))
* **inventory:** preserve tag-selected secret coverage ([90d032c](https://github.com/dryvist/ansible-secrets-management/commit/90d032cca74a2b22b1759b66b810e83d837bb5c8))
* mint flow-lock IDs through approle-issuer ([8efc27d](https://github.com/dryvist/ansible-secrets-management/commit/8efc27d652ee7980e50997a02e3ce996de9fa59b))
* **ntfy:** single-quote the Zammad topic-group JSON in the subscriber env file ([#2486](https://github.com/dryvist/ansible-secrets-management/issues/2486)) ([55b3418](https://github.com/dryvist/ansible-secrets-management/commit/55b34185f3f9ac9161150a704284ee186a8961ce))
* **openbao_secrets:** decide a failed AppRole login without failing the task ([#2301](https://github.com/dryvist/ansible-secrets-management/issues/2301)) ([ba97921](https://github.com/dryvist/ansible-secrets-management/commit/ba979218bb0713e019c514768c53a6c52554dbcf))
* **openbao_secrets:** declare the local-cloud path optional ([#2293](https://github.com/dryvist/ansible-secrets-management/issues/2293)) ([7bf2124](https://github.com/dryvist/ansible-secrets-management/commit/7bf2124432dda1d1f6e9b47d7d8e647b961a05ae))
* **openbao_secrets:** keep an owner's own MCP path in its fetch domain ([41fca41](https://github.com/dryvist/ansible-secrets-management/commit/41fca410f73fce9ee623d0c7e4738852521417f3))
* **openbao_secrets:** run the endpoint probe in check mode ([#64](https://github.com/dryvist/ansible-secrets-management/issues/64)) ([9c40b51](https://github.com/dryvist/ansible-secrets-management/commit/9c40b51b9fbaaef6b0a455639982c0f818b3f22f))
* **openbao_secrets:** skip credential publishing in check mode ([#262](https://github.com/dryvist/ansible-secrets-management/issues/262)) ([5b64b13](https://github.com/dryvist/ansible-secrets-management/commit/5b64b13b47c88dd8448bb7df12772d95c1133840))
* **openbao_secrets:** take the issuer path only where flow-lock runs ([#2503](https://github.com/dryvist/ansible-secrets-management/issues/2503)) ([75f9f6c](https://github.com/dryvist/ansible-secrets-management/commit/75f9f6c4c98a59dd7969e66a29b4d417607e01a2))
* **openbao:** accept spent reconcile secret_id on accessor destroy ([#10](https://github.com/dryvist/ansible-secrets-management/issues/10)) ([e5629ab](https://github.com/dryvist/ansible-secrets-management/commit/e5629ab6110ee72858161ac903da49e4f377de41))
* **openbao:** add Semaphore reads for benchmark and sandbox-agent ([#247](https://github.com/dryvist/ansible-secrets-management/issues/247)) ([5cdaff4](https://github.com/dryvist/ansible-secrets-management/commit/5cdaff4b0367e8a254c33fdcd4ceea8cbcde5daf))
* **openbao:** add the Azure engine path to ai-admin-policy.hcl.j2 ([#101](https://github.com/dryvist/ansible-secrets-management/issues/101)) ([9c839cb](https://github.com/dryvist/ansible-secrets-management/commit/9c839cba7da149b7498b7af6e174179e298952af))
* **openbao:** ai-admin administers login MFA ([3f59c63](https://github.com/dryvist/ansible-secrets-management/commit/3f59c634f1b6f86f8d13c213270fe0abb1f9b9bf))
* **openbao:** ai-admin administers login MFA ([9016915](https://github.com/dryvist/ansible-secrets-management/commit/9016915c54b9d28163b54926a9238391056f300e))
* **openbao:** alert once per rotator failure streak ([#2515](https://github.com/dryvist/ansible-secrets-management/issues/2515)) ([f7a82d0](https://github.com/dryvist/ansible-secrets-management/commit/f7a82d0cdae13f5585d5b8904483995ef32b67ed))
* **openbao:** assert sandbox permission set mapping ([5de28ce](https://github.com/dryvist/ansible-secrets-management/commit/5de28ce3894bf3c974bd1784e3b4c53c423b40ff))
* **openbao:** attach ai-admin-guard to ai-admin-session only ([b5a8694](https://github.com/dryvist/ansible-secrets-management/commit/b5a86946a7b5da118eee8bce1272acd29932d837))
* **openbao:** authenticate the public repository listing on GitHub App mounts ([#169](https://github.com/dryvist/ansible-secrets-management/issues/169)) ([3aa4cd2](https://github.com/dryvist/ansible-secrets-management/commit/3aa4cd23d8475486f6c87520a4c474e29dcb41bc))
* **openbao:** bind the ai-sessions-backup AppRole to the workstation class ([81cef7d](https://github.com/dryvist/ansible-secrets-management/commit/81cef7dbd1a28ffef153d40502a0b882f331c797))
* **openbao:** bind the ai-sessions-backup AppRole to the workstation class ([0912923](https://github.com/dryvist/ansible-secrets-management/commit/091292381a6286b1656f2ee913fd5b4cf2eac9c3))
* **openbao:** bound reconcile policy and AppRole writes ([#221](https://github.com/dryvist/ansible-secrets-management/issues/221)) ([2f01f1e](https://github.com/dryvist/ansible-secrets-management/commit/2f01f1e63f42e163f263fd46c68bde4bc495d50c))
* **openbao:** compare /32 AppRole binds without the prefix length ([#2526](https://github.com/dryvist/ansible-secrets-management/issues/2526)) ([dbf96e2](https://github.com/dryvist/ansible-secrets-management/commit/dbf96e2112e7bb2ed3c12efdc19bbf8cb4142cf9))
* **openbao:** complete taxonomy and permission set fixture ([28dbc9c](https://github.com/dryvist/ansible-secrets-management/commit/28dbc9c6901e973ee652c992daecfbb0e1911981))
* **openbao:** count an empty JSON list as absent in the secret-age audit ([#60](https://github.com/dryvist/ansible-secrets-management/issues/60)) ([8c454be](https://github.com/dryvist/ansible-secrets-management/commit/8c454bedee94672ba097826d7cb29d08327bab7c))
* **openbao:** cover break-glass and reconcile readers in owner-only MCP grants ([e2bbeb5](https://github.com/dryvist/ansible-secrets-management/commit/e2bbeb58c52fa0447b350b468b620b7fa5d13007))
* **openbao:** create the denylist entry metadata with put when absent ([#2273](https://github.com/dryvist/ansible-secrets-management/issues/2273)) ([40e8589](https://github.com/dryvist/ansible-secrets-management/commit/40e85897f2a737dbdf97691fa922df0152271054))
* **openbao:** delegate generated secret writes through the CLI host ([e677200](https://github.com/dryvist/ansible-secrets-management/commit/e677200747bfadb1b771d93fb0ea388e9b96e43b))
* **openbao:** delegate the GitHub App check include to localhost ([#2270](https://github.com/dryvist/ansible-secrets-management/issues/2270)) ([65c0388](https://github.com/dryvist/ansible-secrets-management/commit/65c0388b426db360e677254d239dada38385b208))
* **openbao:** do not declare the Hermes policies without an installation ([#2448](https://github.com/dryvist/ansible-secrets-management/issues/2448)) ([79d7ca8](https://github.com/dryvist/ansible-secrets-management/commit/79d7ca8ad817ef53a728bb0e3bf510977bda799a))
* **openbao:** do not schedule the ci-resolver policy while its repository list is empty ([7152318](https://github.com/dryvist/ansible-secrets-management/commit/7152318a71fe4a20e626a11526674e36a3ce14fd))
* **openbao:** do not schedule the ci-resolver policy while its repository list is empty ([8749cec](https://github.com/dryvist/ansible-secrets-management/commit/8749cec03fe04cad78e65acb04edda3da58944e6))
* **openbao:** do not schedule the ci-resolver policy while its repository list is empty ([#84](https://github.com/dryvist/ansible-secrets-management/issues/84)) ([09de305](https://github.com/dryvist/ansible-secrets-management/commit/09de30587543c5e90357f6f8d016cdbdb4c02fa4))
* **openbao:** drop the Azure credential read from the terraform-apply policy ([bd22110](https://github.com/dryvist/ansible-secrets-management/commit/bd22110267642d492aadeb514132ce5eb592c4af))
* **openbao:** drop the stale scheduled-mode name load in the rotation play ([#2346](https://github.com/dryvist/ansible-secrets-management/issues/2346)) ([4762c6b](https://github.com/dryvist/ansible-secrets-management/commit/4762c6b4cac13730b1df19553cf924b91add6e55))
* **openbao:** end AppRole rotation before credential use in check mode ([9f8eac5](https://github.com/dryvist/ansible-secrets-management/commit/9f8eac56bdc0523ed1950b4a4d3e051296667667))
* **openbao:** end AppRole rotation before credential use in check mode ([#89](https://github.com/dryvist/ansible-secrets-management/issues/89)) ([6a84836](https://github.com/dryvist/ansible-secrets-management/commit/6a848366c67eb2eaf36b5f4b50583cccba903110))
* **openbao:** exclude the plane token's policies from reconcile ([#43](https://github.com/dryvist/ansible-secrets-management/issues/43)) ([164aaff](https://github.com/dryvist/ansible-secrets-management/commit/164aaff0cdddf3fd233ec9d1b71eeabe90ba8468))
* **openbao:** extend reconcile token session TTL ([626d70a](https://github.com/dryvist/ansible-secrets-management/commit/626d70ae12f6c7dfe6628626963bfc720ee67b1d))
* **openbao:** extend reconcile token session TTL ([86310ca](https://github.com/dryvist/ansible-secrets-management/commit/86310cad5b665cbf24c00230c3d6bf4cc1df549d))
* **openbao:** filter per-call env fields ([#257](https://github.com/dryvist/ansible-secrets-management/issues/257)) ([00adbce](https://github.com/dryvist/ansible-secrets-management/commit/00adbce890584a5450255cad91892c12c850831c))
* **openbao:** finish a rotation whose previous secret_id already expired ([#2258](https://github.com/dryvist/ansible-secrets-management/issues/2258)) ([617dfa5](https://github.com/dryvist/ansible-secrets-management/commit/617dfa5449f4a2aec377989b67c6833f4ebbe4a5))
* **openbao:** fold host-cert sign grant into existing signer policies ([#2210](https://github.com/dryvist/ansible-secrets-management/issues/2210)) ([437bbf8](https://github.com/dryvist/ansible-secrets-management/commit/437bbf84d55fe2db396da2066f6795a6b0f742cc))
* **openbao:** gate the rotation roster load on live roster readers ([#87](https://github.com/dryvist/ansible-secrets-management/issues/87)) ([54419b2](https://github.com/dryvist/ansible-secrets-management/commit/54419b24a91831750310f4b3e01922b67fdd0db4))
* **openbao:** generate the assistant guest router key and grant its apps path ([#67](https://github.com/dryvist/ansible-secrets-management/issues/67)) ([ea24f28](https://github.com/dryvist/ansible-secrets-management/commit/ea24f28cbd5ff926b46a4d06e517da2e8b84ea62))
* **openbao:** generate the donna router key and grant its apps path ([ea24f28](https://github.com/dryvist/ansible-secrets-management/commit/ea24f28cbd5ff926b46a4d06e517da2e8b84ea62))
* **openbao:** generate the monitoring GATUS_EXTERNAL_TOKEN ([#2172](https://github.com/dryvist/ansible-secrets-management/issues/2172)) ([546f0aa](https://github.com/dryvist/ansible-secrets-management/commit/546f0aa55f3fcc2fd350cf50e1eb8ed5405c5641))
* **openbao:** give open-llm the rotated-domain secret_id ttl ([#2518](https://github.com/dryvist/ansible-secrets-management/issues/2518)) ([3697109](https://github.com/dryvist/ansible-secrets-management/commit/36971098c32dff31395db6f8ec16af988519bdd3))
* **openbao:** grant apps reader published buckets ([#249](https://github.com/dryvist/ansible-secrets-management/issues/249)) ([674e6be](https://github.com/dryvist/ansible-secrets-management/commit/674e6be6b77a5b1225a7af896666faad77a7a576))
* **openbao:** grant reconcile the GitHub org-secrets Transit key ([#244](https://github.com/dryvist/ansible-secrets-management/issues/244)) ([cdb9c56](https://github.com/dryvist/ansible-secrets-management/commit/cdb9c569d013b70446fc8d73cf52f893f89e5d5a))
* **openbao:** grant Semaphore reads for benchmark and sandbox-agent ([5cdaff4](https://github.com/dryvist/ansible-secrets-management/commit/5cdaff4b0367e8a254c33fdcd4ceea8cbcde5daf))
* **openbao:** grant the admin policy the Azure engine mount ([0ee360c](https://github.com/dryvist/ansible-secrets-management/commit/0ee360c28e8b3f4c638c6e53a69030818b84850d))
* **openbao:** keep finite secret_id bounds on the open-llm AppRole ([7e88bb8](https://github.com/dryvist/ansible-secrets-management/commit/7e88bb81e170050b2f5a5c53811baa454286aa03))
* **openbao:** keep finite secret_id bounds on the open-llm AppRole ([2e9b0de](https://github.com/dryvist/ansible-secrets-management/commit/2e9b0def770e7b8493a37819c46bc8905bc0c915))
* **openbao:** keep finite secret_id bounds on the proxman AppRole ([0822829](https://github.com/dryvist/ansible-secrets-management/commit/082282939702dde6c1fa9ae955f067291cae3ef3))
* **openbao:** keep installation write scope opt-in ([#2336](https://github.com/dryvist/ansible-secrets-management/issues/2336)) ([#2342](https://github.com/dryvist/ansible-secrets-management/issues/2342)) ([c068d9f](https://github.com/dryvist/ansible-secrets-management/commit/c068d9f288dceec4df5183d898b7748a232ed274))
* **openbao:** keep the apps reader's grant on the pve-exporter bucket ([#2328](https://github.com/dryvist/ansible-secrets-management/issues/2328)) ([9eda50e](https://github.com/dryvist/ansible-secrets-management/commit/9eda50ed1922db727a82c0dd26e2cff7114bf358))
* **openbao:** keep the github-runner mount and policy declared without App credentials ([#227](https://github.com/dryvist/ansible-secrets-management/issues/227)) ([f910708](https://github.com/dryvist/ansible-secrets-management/commit/f91070814db2da88ebe6662c7c827444138a3c2b))
* **openbao:** keep the internal Z.ai copy until the external leaf is seeded ([#139](https://github.com/dryvist/ansible-secrets-management/issues/139)) ([d7f28eb](https://github.com/dryvist/ansible-secrets-management/commit/d7f28eb5f6df9179d9f1835b4bb3b43142e7b9d9))
* **openbao:** keep the nodes' seal key id when the environment sets none ([#2244](https://github.com/dryvist/ansible-secrets-management/issues/2244)) ([e8d8d81](https://github.com/dryvist/ansible-secrets-management/commit/e8d8d81ed22501c28812387c7b470276dfddd373))
* **openbao:** leave write installation_id unpinned and skip the empty ci-resolver policy ([#85](https://github.com/dryvist/ansible-secrets-management/issues/85)) ([147b771](https://github.com/dryvist/ansible-secrets-management/commit/147b771e8c7cf3aa3680e087bda693835bf15f82))
* **openbao:** let policy sync derive a mount's read set ([#292](https://github.com/dryvist/ansible-secrets-management/issues/292)) ([3b0941f](https://github.com/dryvist/ansible-secrets-management/commit/3b0941f89fc9e70c8548437a6e6cfbad817cface))
* **openbao:** let semaphore mint read-only tokens by org on the everyday mount ([#173](https://github.com/dryvist/ansible-secrets-management/issues/173)) ([091a7f5](https://github.com/dryvist/ansible-secrets-management/commit/091a7f5e3aed3884e1f023d7f45b37cb09549c68))
* **openbao:** load the agent roster before rotating AppRole secret IDs ([f7259f7](https://github.com/dryvist/ansible-secrets-management/commit/f7259f7aebfd4962a1ce1d34888df7e581b4c341))
* **openbao:** load the agent roster before rotating AppRole secret IDs ([#82](https://github.com/dryvist/ansible-secrets-management/issues/82)) ([48cc113](https://github.com/dryvist/ansible-secrets-management/commit/48cc11363d2f74f4814270319c51c20d7692d4d6))
* **openbao:** load the scheduled identity's name from 05g in the rotation play ([b2add5c](https://github.com/dryvist/ansible-secrets-management/commit/b2add5cefb2b467b3a65d9deae0f51fb3854f652))
* **openbao:** load the scheduled identity's name from 05g in the rotation play ([3e7534c](https://github.com/dryvist/ansible-secrets-management/commit/3e7534c47bdd84fc9d8f0135601715d8e40faffa))
* **openbao:** mask the role_id read in domain rotation ([#2371](https://github.com/dryvist/ansible-secrets-management/issues/2371)) ([d3af608](https://github.com/dryvist/ansible-secrets-management/commit/d3af608a81667febe7dd4e29a1802827ab5c200d))
* **openbao:** mint the claude-ocg router key with the sk- prefix ([#149](https://github.com/dryvist/ansible-secrets-management/issues/149)) ([912be28](https://github.com/dryvist/ansible-secrets-management/commit/912be28d342fe8f1b940a6d68fd3253827fd9656))
* **openbao:** move owned MCP denies to a dedicated local-llm policy ([ad07b7f](https://github.com/dryvist/ansible-secrets-management/commit/ad07b7f2ffb5c587f545b502c1f2e92494fa3e6f))
* **openbao:** non-expiring class-bound secret_ids for standing identities ([#2509](https://github.com/dryvist/ansible-secrets-management/issues/2509)) ([6d4e47a](https://github.com/dryvist/ansible-secrets-management/commit/6d4e47a646c2db98d7bf0073b6c4ea7990587b8f))
* **openbao:** parse the live AppRole list as a bare array ([#2351](https://github.com/dryvist/ansible-secrets-management/issues/2351)) ([15f3246](https://github.com/dryvist/ansible-secrets-management/commit/15f3246f20e1f003b8e3d499d866d2d4b2e77e0d))
* **openbao:** persist the audit imfile read offset ([#2521](https://github.com/dryvist/ansible-secrets-management/issues/2521)) ([a2f5115](https://github.com/dryvist/ansible-secrets-management/commit/a2f5115c7e240703ef4f44dfab898cc1e19f17b8))
* **openbao:** pin reconcile AppRole TTL and use-count parameters ([#222](https://github.com/dryvist/ansible-secrets-management/issues/222)) ([53c861d](https://github.com/dryvist/ansible-secrets-management/commit/53c861d6a0cf77783cd9050821564a198f2c266c))
* **openbao:** preserve finite write realm bounds ([#2339](https://github.com/dryvist/ansible-secrets-management/issues/2339)) ([1e44f41](https://github.com/dryvist/ansible-secrets-management/commit/1e44f41c3da496ed1413992ab1d7ff6a715fa4a4))
* **openbao:** print the working policy-sync command ([#240](https://github.com/dryvist/ansible-secrets-management/issues/240)) ([3356173](https://github.com/dryvist/ansible-secrets-management/commit/335617335c0a5dc03d36971fe6e953c9bb59f939))
* **openbao:** prove workstation-bound rotated pairs by lookup ([#2149](https://github.com/dryvist/ansible-secrets-management/issues/2149)) ([fe78ec8](https://github.com/dryvist/ansible-secrets-management/commit/fe78ec8778fe89ab5d86b022b0e88e19e220f670))
* **openbao:** read only mount paths from the policy-sync capability map ([#286](https://github.com/dryvist/ansible-secrets-management/issues/286)) ([ff12323](https://github.com/dryvist/ansible-secrets-management/commit/ff12323dc29dbec37a56ffc53479c4ab6fa60c75))
* **openbao:** read the App install allowlist from the env document ([#2268](https://github.com/dryvist/ansible-secrets-management/issues/2268)) ([0127aad](https://github.com/dryvist/ansible-secrets-management/commit/0127aad84cda0c438ad435f3a25f9756c3ab6ade))
* **openbao:** reconcile through per-call issuer ([#2446](https://github.com/dryvist/ansible-secrets-management/issues/2446)) ([588ac6b](https://github.com/dryvist/ansible-secrets-management/commit/588ac6b1c1a8a9101fb96da2587bd7aa7b0c4105))
* **openbao:** refresh apt cache before installing prerequisites ([#158](https://github.com/dryvist/ansible-secrets-management/issues/158)) ([986eeeb](https://github.com/dryvist/ansible-secrets-management/commit/986eeebcbb853f7501bac2885749c033b7ab3766))
* **openbao:** refuse preset roster probe results and gate the rotation tests ([6d62b90](https://github.com/dryvist/ansible-secrets-management/commit/6d62b909bd9d85110bf89df9ab5931fbb0766d8b))
* **openbao:** refuse to render the voter-health env file without a HEC token ([#2531](https://github.com/dryvist/ansible-secrets-management/issues/2531)) ([34502b9](https://github.com/dryvist/ansible-secrets-management/commit/34502b9aab8c2cf29fbe84348dda472e46fb1ab6))
* **openbao:** register the telemetry exporter identity ([#265](https://github.com/dryvist/ansible-secrets-management/issues/265)) ([a303737](https://github.com/dryvist/ansible-secrets-management/commit/a303737c5e2714c1b2999de35c7e095f1974d8e7))
* **openbao:** require the snapshot unit and skip the restart in check mode ([e7007ef](https://github.com/dryvist/ansible-secrets-management/commit/e7007efbbc167acd8e65b29f66134211aea9f8dd))
* **openbao:** restart notified voters one at a time ([#2519](https://github.com/dryvist/ansible-secrets-management/issues/2519)) ([684e155](https://github.com/dryvist/ansible-secrets-management/commit/684e15596a77058ea3cc7933e1537662e626cbe5))
* **openbao:** restore Cribl Mac rotation catalog ([e43cc9d](https://github.com/dryvist/ansible-secrets-management/commit/e43cc9d587408c4e7f39b297158d0f0f7eb249e3))
* **openbao:** rotate the ai-donna AppRole secret_id with the other agent identities ([#2465](https://github.com/dryvist/ansible-secrets-management/issues/2465)) ([b8ef9b2](https://github.com/dryvist/ansible-secrets-management/commit/b8ef9b2fd575c0b87fbb764ab2b8f18dbdcfcef6))
* **openbao:** run init store calls on the CLI host ([a305c3b](https://github.com/dryvist/ansible-secrets-management/commit/a305c3b7f9996d918ac50fe063a4d7af38df509f))
* **openbao:** run init store calls on the CLI host ([505ae3e](https://github.com/dryvist/ansible-secrets-management/commit/505ae3e03f351c4a44ca41b54ebba47b9145eb32))
* **openbao:** run policy-sync before reconcile-grant consumers ([#2219](https://github.com/dryvist/ansible-secrets-management/issues/2219)) ([a5b30d9](https://github.com/dryvist/ansible-secrets-management/commit/a5b30d9c297bf6246a1731792adca7bb33fef521))
* **openbao:** run policy-sync capability check and write from the controller ([#2221](https://github.com/dryvist/ansible-secrets-management/issues/2221)) ([a461dd0](https://github.com/dryvist/ansible-secrets-management/commit/a461dd002fb6a1e1a2f19f48c6a3c310cd3810cb))
* **openbao:** run the init path's read-only probes in check mode ([#71](https://github.com/dryvist/ansible-secrets-management/issues/71)) ([5e37787](https://github.com/dryvist/ansible-secrets-management/commit/5e377873d8bb4ec0f6f8678ee562007f0b3fd435))
* **openbao:** run the reconcile credential chain in check mode ([#281](https://github.com/dryvist/ansible-secrets-management/issues/281)) ([30e43e7](https://github.com/dryvist/ansible-secrets-management/commit/30e43e7fcc953338c22d2ef93dfe92ccc433627a))
* **openbao:** run the undeclared-live AppRole calls on the CLI host ([#2450](https://github.com/dryvist/ansible-secrets-management/issues/2450)) ([fecf6af](https://github.com/dryvist/ansible-secrets-management/commit/fecf6af8a903a4eee2d6ad2b06f4dc09a4262ad9))
* **openbao:** scheduled AppRole rotation renews itself first and survives a failed domain ([#2510](https://github.com/dryvist/ansible-secrets-management/issues/2510)) ([19d268f](https://github.com/dryvist/ansible-secrets-management/commit/19d268f230b8ce164260def3abe726540d2e4e15))
* **openbao:** scope Semaphore policy read access ([#255](https://github.com/dryvist/ansible-secrets-management/issues/255)) ([62de769](https://github.com/dryvist/ansible-secrets-management/commit/62de7690ac022582d1fcb9e9d9320090b532c8da))
* **openbao:** scrub environment-specific names from init tasks ([#2259](https://github.com/dryvist/ansible-secrets-management/issues/2259)) ([7b6fa02](https://github.com/dryvist/ansible-secrets-management/commit/7b6fa02e6f7e437a3a027e2798186a6ae54780dc))
* **openbao:** send subscription_id in the Azure engine config ([35d95a3](https://github.com/dryvist/ansible-secrets-management/commit/35d95a315063ef0f619fdc4bb5f33006236ecddd))
* **openbao:** send subscription_id in the Azure engine config ([#114](https://github.com/dryvist/ansible-secrets-management/issues/114)) ([f95dcaf](https://github.com/dryvist/ansible-secrets-management/commit/f95dcafc1918ded4838293c8e802d2fae61d8dbb))
* **openbao:** send the app-secret promote write from the CLI host ([#2452](https://github.com/dryvist/ansible-secrets-management/issues/2452)) ([7709979](https://github.com/dryvist/ansible-secrets-management/commit/770997926a5b48c8cdb0a8692708aa0e19d9783e))
* **openbao:** send the declared AppRole parameters with the existence read ([#229](https://github.com/dryvist/ansible-secrets-management/issues/229)) ([5681784](https://github.com/dryvist/ansible-secrets-management/commit/568178400bbc65307b69226296657c92b5dc752a))
* **openbao:** set ansible_become false on the delegated App check include ([#2271](https://github.com/dryvist/ansible-secrets-management/issues/2271)) ([1bafa69](https://github.com/dryvist/ansible-secrets-management/commit/1bafa69f1fb7fb35e39db939d7723189e4f6d3fb))
* **openbao:** single policy field on the github-exporter role entry ([#195](https://github.com/dryvist/ansible-secrets-management/issues/195)) ([50c0d6c](https://github.com/dryvist/ansible-secrets-management/commit/50c0d6c767d2e9ae2a157b27360369c3d50ef651))
* **openbao:** skip rolling restarts in check mode ([521f6ee](https://github.com/dryvist/ansible-secrets-management/commit/521f6ee2fc0f2bbee212bfe43e763d0bf44e8750))
* **openbao:** skip rolling restarts in check mode ([#181](https://github.com/dryvist/ansible-secrets-management/issues/181)) ([86cf4af](https://github.com/dryvist/ansible-secrets-management/commit/86cf4af5dd9c8b2077d39891e247f8228613b3c8))
* **openbao:** skip the Doppler sync-token read on a seed run ([#2131](https://github.com/dryvist/ansible-secrets-management/issues/2131)) ([e18fa98](https://github.com/dryvist/ansible-secrets-management/commit/e18fa98311d2e36123ad49140dbd489f26426fb2))
* **openbao:** skip the package install task in check mode ([e0ae4a2](https://github.com/dryvist/ansible-secrets-management/commit/e0ae4a20f44826be9a86229daab96ef4fc7ee5ff))
* **openbao:** skip the package install task in check mode ([#180](https://github.com/dryvist/ansible-secrets-management/issues/180)) ([c16b6f6](https://github.com/dryvist/ansible-secrets-management/commit/c16b6f67b3e3416aa3358a8fc9c61a4adc664b9a))
* **openbao:** snapshot and restart on a version upgrade ([57ea8ca](https://github.com/dryvist/ansible-secrets-management/commit/57ea8ca17dd597e842bcc23a183eb93416b4ebba))
* **openbao:** snapshot and restart on a version upgrade ([#90](https://github.com/dryvist/ansible-secrets-management/issues/90)) ([29994ea](https://github.com/dryvist/ansible-secrets-management/commit/29994ea3ae67fe8b220ff170301067e4def66a4c))
* **openbao:** start the observability Splunk grant on its own line ([#147](https://github.com/dryvist/ansible-secrets-management/issues/147)) ([54b4ed7](https://github.com/dryvist/ansible-secrets-management/commit/54b4ed7f128563911a60437e8ce2b5ecbecd5685))
* **openbao:** tag and order the per-App GitHub mount phase ([#2514](https://github.com/dryvist/ansible-secrets-management/issues/2514)) ([f0687fa](https://github.com/dryvist/ansible-secrets-management/commit/f0687fa9ddb51a993281272a09fa9e26255be2e8))
* **openbao:** the exporter AppRole holds only the exporter policy ([50c0d6c](https://github.com/dryvist/ansible-secrets-management/commit/50c0d6c767d2e9ae2a157b27360369c3d50ef651))
* **openbao:** treat an empty Azure engine client_id as missing config ([04f63ec](https://github.com/dryvist/ansible-secrets-management/commit/04f63ecf5291bc3dd8b2f36bba6ef094b9787bd0))
* **openbao:** treat an empty Azure engine client_id as missing config ([#107](https://github.com/dryvist/ansible-secrets-management/issues/107)) ([a85ff41](https://github.com/dryvist/ansible-secrets-management/commit/a85ff412ad5b4cbf86ac36dc76feb925485e273e))
* **openbao:** unlimited secret_id uses for local-llm, hermes and ai-donna ([#2524](https://github.com/dryvist/ansible-secrets-management/issues/2524)) ([7d89ed6](https://github.com/dryvist/ansible-secrets-management/commit/7d89ed6b4a1b47ecc8ead52c5212c2c0063dedd2))
* **openbao:** write KV secret values through the API, never argv ([#2370](https://github.com/dryvist/ansible-secrets-management/issues/2370)) ([a07dced](https://github.com/dryvist/ansible-secrets-management/commit/a07dcedcc1e58b4e7e7a945c7e85b27cb9da7b18))
* **openbao:** write reachable RBAC policies before failing on an ungranted name ([#2213](https://github.com/dryvist/ansible-secrets-management/issues/2213)) ([ad4d62d](https://github.com/dryvist/ansible-secrets-management/commit/ad4d62d488ab96d0fa32a7fd65893679a32f8e87))
* split webhook workspace access by mount ([#275](https://github.com/dryvist/ansible-secrets-management/issues/275)) ([8373dab](https://github.com/dryvist/ansible-secrets-management/commit/8373dab34d31e40471b595f369dca6a621c0131d))
* **unpoller:** read the UniFi controller address from OpenBao via the prefetch ([#2227](https://github.com/dryvist/ansible-secrets-management/issues/2227)) ([0749376](https://github.com/dryvist/ansible-secrets-management/commit/07493764074a302a4f9e6aa11a953ffd783641ff))


### Performance

* **openbao:** add openbao_kv_seed tag and controller-side policy reads ([#2193](https://github.com/dryvist/ansible-secrets-management/issues/2193)) ([bf7386c](https://github.com/dryvist/ansible-secrets-management/commit/bf7386c5326efdb04bdd832d05a5cdeec4017c51))
* **openbao:** resolve the AppRole parameter maps once per run ([#231](https://github.com/dryvist/ansible-secrets-management/issues/231)) ([f7335d4](https://github.com/dryvist/ansible-secrets-management/commit/f7335d40f72565b0cef3a2da895c1fa07a01544e))
* **openbao:** run the AppRole, SSH role and policy writes on openbao_cli_host ([c5f9307](https://github.com/dryvist/ansible-secrets-management/commit/c5f9307dd51c64a517f75361c702f0718659b67d))
* **openbao:** run the AppRole, SSH role and policy writes on openbao_cli_host ([34ef30a](https://github.com/dryvist/ansible-secrets-management/commit/34ef30a79f71b0530aec558b66ee324bc4eb6000))
* **secrets:** scope the OpenBao pre-fetch to domains this run's hosts need ([#2183](https://github.com/dryvist/ansible-secrets-management/issues/2183)) ([bad4da3](https://github.com/dryvist/ansible-secrets-management/commit/bad4da3c46444eab5e117322bd435bd3f1423571))

## [0.36.0](https://github.com/dryvist/ansible-secrets-management/compare/v0.35.0...v0.36.0) (2026-10-21)


### Features

* **openbao:** grant apps reads for console credentials ([#291](https://github.com/dryvist/ansible-secrets-management/issues/291)) ([a8afda3](https://github.com/dryvist/ansible-secrets-management/commit/a8afda3e558d5cfc3dd1c827703de4fcb1348a59))


### Bug Fixes

* **openbao:** let policy sync derive a mount's read set ([#292](https://github.com/dryvist/ansible-secrets-management/issues/292)) ([3b0941f](https://github.com/dryvist/ansible-secrets-management/commit/3b0941f89fc9e70c8548437a6e6cfbad817cface))

## [0.35.0](https://github.com/dryvist/ansible-secrets-management/compare/v0.34.1...v0.35.0) (2026-10-21)


### Features

* **openbao:** derive the github-work read set and mint write from the App grant ([#289](https://github.com/dryvist/ansible-secrets-management/issues/289)) ([05a5e4a](https://github.com/dryvist/ansible-secrets-management/commit/05a5e4a226f317dffa86bb481cd728da065f6124))

## [0.34.1](https://github.com/dryvist/ansible-secrets-management/compare/v0.34.0...v0.34.1) (2026-10-21)


### Bug Fixes

* **openbao:** read only mount paths from the policy-sync capability map ([#286](https://github.com/dryvist/ansible-secrets-management/issues/286)) ([ff12323](https://github.com/dryvist/ansible-secrets-management/commit/ff12323dc29dbec37a56ffc53479c4ab6fa60c75))

## [0.34.0](https://github.com/dryvist/ansible-secrets-management/compare/v0.33.3...v0.34.0) (2026-10-21)


### ⚠ BREAKING CHANGES

* **openbao:** drop the github-write repository allowlist ([#2528](https://github.com/dryvist/ansible-secrets-management/issues/2528))

### Features

* add GitHub agent flow identities ([7d5b714](https://github.com/dryvist/ansible-secrets-management/commit/7d5b714027b3c2602fed00272f6e3db9f0c338b4))
* **agent_sandbox:** host dispatcher with terminal sessions and a login check ([c7def81](https://github.com/dryvist/ansible-secrets-management/commit/c7def81b3fda3a9814b47e1c80568fb46c55a27e))
* **agent_sandbox:** install the pinned host dispatcher with terminal sessions ([01bc2ee](https://github.com/dryvist/ansible-secrets-management/commit/01bc2ee63917eb4e85db7ea61bf5c5f6e62c313b))
* **agent_sandbox:** provide dispatcher alert settings ([#2382](https://github.com/dryvist/ansible-secrets-management/issues/2382)) ([cc5da81](https://github.com/dryvist/ansible-secrets-management/commit/cc5da8120ecb9e3e64bc7c3a3781c86ec92aaff5))
* **authelia,openbao:** seed a UI check service user with TOTP ([bcf07ec](https://github.com/dryvist/ansible-secrets-management/commit/bcf07ec9565c1f85d813f99e770f9484af73b627))
* **authelia:** add OpenBao elevation device-code clients and elevate policy ([#24](https://github.com/dryvist/ansible-secrets-management/issues/24)) ([7fa9ed2](https://github.com/dryvist/ansible-secrets-management/commit/7fa9ed2df1dbe47c65fe3d70109bca3287a2a1c0))
* **authelia:** generate the trusted elevation client secret ([#166](https://github.com/dryvist/ansible-secrets-management/issues/166)) ([50952a9](https://github.com/dryvist/ansible-secrets-management/commit/50952a9b054890fde3e1b4d72b2089da1654b6d7))
* **authelia:** generate the trusted elevation client secret and use client_secret_basic ([5370088](https://github.com/dryvist/ansible-secrets-management/commit/5370088a97db8facfb9e7331162edc9f90a2e410))
* **config:** add exact path entries ([5663df7](https://github.com/dryvist/ansible-secrets-management/commit/5663df74122ea0b08572dba7ad322c1dd0660ff5))
* **config:** add exact path entries ([2eec5d8](https://github.com/dryvist/ansible-secrets-management/commit/2eec5d81551c564b19512cf5beca96d4d70da64f))
* **glance:** add Network + Media page and wall kiosk bypass ([#2212](https://github.com/dryvist/ansible-secrets-management/issues/2212)) ([0471738](https://github.com/dryvist/ansible-secrets-management/commit/04717381b250c60c4bcb3224e1c3661455c8dc51))
* **glance:** enable the deployment-profile tile with a generated router key ([#2449](https://github.com/dryvist/ansible-secrets-management/issues/2449)) ([177c3a5](https://github.com/dryvist/ansible-secrets-management/commit/177c3a54e34b583fbb30e0ac78c057e795fe48c0))
* **homarr:** add the homarr-v2 instance with declarative boards ([#2278](https://github.com/dryvist/ansible-secrets-management/issues/2278)) ([2bc7b39](https://github.com/dryvist/ansible-secrets-management/commit/2bc7b39490c9bda8613ec0d337330c077c5a8519))
* **ntfy:** fan every topic out to one all-alerts Slack channel ([#2276](https://github.com/dryvist/ansible-secrets-management/issues/2276)) ([d7128d5](https://github.com/dryvist/ansible-secrets-management/commit/d7128d5ca0373d68d83590a6d0f843e59aaa86f1))
* **ntfy:** provision a publish-only ai-jobs token ([6890f01](https://github.com/dryvist/ansible-secrets-management/commit/6890f0194f14d6d75e060db1fe8b973c0dd68ae4))
* **ntfy:** provision a publish-only ai-jobs token ([45f1508](https://github.com/dryvist/ansible-secrets-management/commit/45f15083a501a21be83aa3895fdba05e595e5d38))
* **object_storage:** mint scoped per-bucket RustFS IAM credentials ([#2200](https://github.com/dryvist/ansible-secrets-management/issues/2200)) ([0b53919](https://github.com/dryvist/ansible-secrets-management/commit/0b5391969f3ec183f01e78add71b30c0c6741f94))
* **openbao_secrets:** add PostgreSQL backup S3 domain ([#272](https://github.com/dryvist/ansible-secrets-management/issues/272)) ([eb0646a](https://github.com/dryvist/ansible-secrets-management/commit/eb0646a752c2fc6be41ed78273d59cb224358966))
* **openbao_secrets:** drop owned MCP paths from non-owner fetch domains ([6eda816](https://github.com/dryvist/ansible-secrets-management/commit/6eda81668a11e89646ab0dde5e84ac3be6626a70))
* **openbao_secrets:** drop owned MCP paths from non-owner fetch domains ([#78](https://github.com/dryvist/ansible-secrets-management/issues/78)) ([499d28d](https://github.com/dryvist/ansible-secrets-management/commit/499d28dedcc3b6c27a994cb0f24209ca324ca1aa))
* **openbao:** accept a pre-issued rotator token in the rotation play ([#2363](https://github.com/dryvist/ansible-secrets-management/issues/2363)) ([b339e98](https://github.com/dryvist/ansible-secrets-management/commit/b339e9840e6eabba79d687fe67343549d5f3e006))
* **openbao:** add a github-personal App mount with one write set ([#251](https://github.com/dryvist/ansible-secrets-management/issues/251)) ([96bcd1d](https://github.com/dryvist/ansible-secrets-management/commit/96bcd1d1d45fb5ac6ed636afb7cd2e56df2e3aac))
* **openbao:** add a tofu-state transit AppRole ([#234](https://github.com/dryvist/ansible-secrets-management/issues/234)) ([0127a07](https://github.com/dryvist/ansible-secrets-management/commit/0127a0782bc0f7814cd87604fc4bd7608edeaf06))
* **openbao:** add a work-admin permission set ([#183](https://github.com/dryvist/ansible-secrets-management/issues/183)) ([d0a5af4](https://github.com/dryvist/ansible-secrets-management/commit/d0a5af46103fab0b847977d7774fe62e5fbb8ce3))
* **openbao:** add a workstation-bound tofu-state transit AppRole ([0127a07](https://github.com/dryvist/ansible-secrets-management/commit/0127a0782bc0f7814cd87604fc4bd7608edeaf06))
* **openbao:** add agent-ssh-sign AppRole for workstation SSH signing ([#2359](https://github.com/dryvist/ansible-secrets-management/issues/2359)) ([78652e1](https://github.com/dryvist/ansible-secrets-management/commit/78652e17fb99090ff72c927d506a70ab330dd148))
* **openbao:** add azure secrets engine with roles from environment ([#88](https://github.com/dryvist/ansible-secrets-management/issues/88)) ([1242bf2](https://github.com/dryvist/ansible-secrets-management/commit/1242bf2bd980218d54200e6d467d4432c5e1177c))
* **openbao:** add bounded admin session role ([a56d9e6](https://github.com/dryvist/ansible-secrets-management/commit/a56d9e67d14d68aac748a106e6dc25aa3df25a89))
* **openbao:** add Cribl Edge generated fields and readers ([#2386](https://github.com/dryvist/ansible-secrets-management/issues/2386)) ([a6ef6ba](https://github.com/dryvist/ansible-secrets-management/commit/a6ef6bafd87f5825f1d9b9095d6f9dbc7713c6a0))
* **openbao:** add GitHub Enterprise App mounts and inert tiers ([#30](https://github.com/dryvist/ansible-secrets-management/issues/30)) ([278493a](https://github.com/dryvist/ansible-secrets-management/commit/278493a9e3732616fa41d0160465ac37b3830268))
* **openbao:** add github-hermes App mount with visibility-split sets ([#2284](https://github.com/dryvist/ansible-secrets-management/issues/2284)) ([043f741](https://github.com/dryvist/ansible-secrets-management/commit/043f7412588953deb8fd8df8d912ea9344668c5d))
* **openbao:** add github-runner mount for runner registration by org ([#225](https://github.com/dryvist/ansible-secrets-management/issues/225)) ([79b42b8](https://github.com/dryvist/ansible-secrets-management/commit/79b42b89f9e1a82b2f90959549b60d07a3ef5e85))
* **openbao:** add github-work App mount, policy and AppRole ([0601245](https://github.com/dryvist/ansible-secrets-management/commit/0601245dfb0e40c267eaee884d7cda8d7dec4cf8))
* **openbao:** add github-work App mount, policy and AppRole ([09d9251](https://github.com/dryvist/ansible-secrets-management/commit/09d925190958c83e970ecc6b3fac0d6839312579))
* **openbao:** add Hermes configuration ([#2379](https://github.com/dryvist/ansible-secrets-management/issues/2379)) ([5314292](https://github.com/dryvist/ansible-secrets-management/commit/531429297e6b38c5604ba33f35e35430bb48f99d))
* **openbao:** add local-llm-workstation AppRole for workstation reads ([#2352](https://github.com/dryvist/ansible-secrets-management/issues/2352)) ([be55ae3](https://github.com/dryvist/ansible-secrets-management/commit/be55ae32b455ac76295805313a3288eda83b80ca))
* **openbao:** add owner-neutral GitHub token grants ([#163](https://github.com/dryvist/ansible-secrets-management/issues/163)) ([6270354](https://github.com/dryvist/ansible-secrets-management/commit/627035489ce67a6bfeac15c38be6ce3baea3f129))
* **openbao:** add per-engine component tags ([94b12ee](https://github.com/dryvist/ansible-secrets-management/commit/94b12ee10847db896781b8d12af369df99e71e06))
* **openbao:** add per-engine component tags ([#105](https://github.com/dryvist/ansible-secrets-management/issues/105)) ([a883ff2](https://github.com/dryvist/ansible-secrets-management/commit/a883ff2eba591796c68c28ac23bdb4555478acf2))
* **openbao:** add per-organisation repo-create permission sets ([7742019](https://github.com/dryvist/ansible-secrets-management/commit/7742019de807a0ce1fdd7f51f4cf432a2a88b384))
* **openbao:** add per-organisation repo-create permission sets ([#123](https://github.com/dryvist/ansible-secrets-management/issues/123)) ([1ea7e1a](https://github.com/dryvist/ansible-secrets-management/commit/1ea7e1af92f713b8056b88c8187d6dcc4d2043ad))
* **openbao:** add router and gateway reader roles for roster agent keys ([#75](https://github.com/dryvist/ansible-secrets-management/issues/75)) ([39f1a6e](https://github.com/dryvist/ansible-secrets-management/commit/39f1a6ede05ea360d6db6b64684b3242e23a79fd))
* **openbao:** add sandbox agent AppRoles and identity classes ([#128](https://github.com/dryvist/ansible-secrets-management/issues/128)) ([1fbcca7](https://github.com/dryvist/ansible-secrets-management/commit/1fbcca78cf78532177dde2ebe3ed9cbce6fdd99c))
* **openbao:** add sandbox agent roles ([dd51987](https://github.com/dryvist/ansible-secrets-management/commit/dd5198763a084cecabffa8f1f229688270ff0a5c))
* **openbao:** add ssh host-cert signing role ([#2203](https://github.com/dryvist/ansible-secrets-management/issues/2203)) ([3e9cbc4](https://github.com/dryvist/ansible-secrets-management/commit/3e9cbc4f54bf35726518cd206d1db80c41164700))
* **openbao:** add the ai-admin-guard deny overlay ([4b13726](https://github.com/dryvist/ansible-secrets-management/commit/4b137261d56e20bce67011145c75ffeae34aef06))
* **openbao:** add the Authelia JWT elevation roles and a 1h work-identity token ([#25](https://github.com/dryvist/ansible-secrets-management/issues/25)) ([7127d8b](https://github.com/dryvist/ansible-secrets-management/commit/7127d8b0dac6dbe1b7c458fb11569cbcec99c242))
* **openbao:** add the azure-iac-admin AppRole and policy ([6d58f66](https://github.com/dryvist/ansible-secrets-management/commit/6d58f66887276a535d6552ddd13a5066dd1b6824))
* **openbao:** add the azure-iac-admin AppRole and policy ([#119](https://github.com/dryvist/ansible-secrets-management/issues/119)) ([e2e5065](https://github.com/dryvist/ansible-secrets-management/commit/e2e5065a388f861d480ff9a2a0d7a6f499808a32))
* **openbao:** add the ci-resolver GitHub identity ([#53](https://github.com/dryvist/ansible-secrets-management/issues/53)) ([7eca696](https://github.com/dryvist/ansible-secrets-management/commit/7eca69625ada89e662c8de7fe170921e69988ac3))
* **openbao:** add the clickhouse resource domain ([#100](https://github.com/dryvist/ansible-secrets-management/issues/100)) ([2c60338](https://github.com/dryvist/ansible-secrets-management/commit/2c60338b8e222a63e7af6025192289d8b939dc44))
* **openbao:** add the docs router snapshot key, set and OIDC role ([#2505](https://github.com/dryvist/ansible-secrets-management/issues/2505)) ([551e4d9](https://github.com/dryvist/ansible-secrets-management/commit/551e4d922bd93066dc080982300a9996bb6696cf))
* **openbao:** add the github-enterprise-owner mount and the ai-admin-guard overlay ([#48](https://github.com/dryvist/ansible-secrets-management/issues/48)) ([a1b7dc6](https://github.com/dryvist/ansible-secrets-management/commit/a1b7dc66bb398fde7408478b08ebd0be2c0db5e7))
* **openbao:** add the github-enterprise-owner token mount ([e4f413b](https://github.com/dryvist/ansible-secrets-management/commit/e4f413b8c585926c9f8e37a77fb5af7c55ea7832))
* **openbao:** add the herdr-hail workstation AppRole ([#168](https://github.com/dryvist/ansible-secrets-management/issues/168)) ([a19574a](https://github.com/dryvist/ansible-secrets-management/commit/a19574ab5ce61bad9c9690aea662d1fd2f8511b0))
* **openbao:** add the hermes orchestrator generated app secret ([#129](https://github.com/dryvist/ansible-secrets-management/issues/129)) ([dba4b84](https://github.com/dryvist/ansible-secrets-management/commit/dba4b84927d706a3cc32fafaebe764bc4ef97f62))
* **openbao:** add the litellm-local-workstation generated field ([69af118](https://github.com/dryvist/ansible-secrets-management/commit/69af118134aa27b02331c73cb6ad9904febcb615))
* **openbao:** add the work-admin GitHub tier ([d0a5af4](https://github.com/dryvist/ansible-secrets-management/commit/d0a5af46103fab0b847977d7774fe62e5fbb8ce3))
* **openbao:** add tofu-state transit paths to terraform-apply policy ([#218](https://github.com/dryvist/ansible-secrets-management/issues/218)) ([3c0c019](https://github.com/dryvist/ansible-secrets-management/commit/3c0c0195d1330db7d72d0ae96f38be7314995379))
* **openbao:** add tofu-state transit paths to the ai-admin policy ([#220](https://github.com/dryvist/ansible-secrets-management/issues/220)) ([8d05b4e](https://github.com/dryvist/ansible-secrets-management/commit/8d05b4edc1f5da3cf8c0d8c2b6a9d8fbf273c4bd))
* **openbao:** add transit paths to the reconcile policy ([#219](https://github.com/dryvist/ansible-secrets-management/issues/219)) ([a98bc52](https://github.com/dryvist/ansible-secrets-management/commit/a98bc529590d62f32b2b38ca348222bb5acee27b))
* **openbao:** admin set and Terrakube identity per GitHub org ([#190](https://github.com/dryvist/ansible-secrets-management/issues/190)) ([76e5263](https://github.com/dryvist/ansible-secrets-management/commit/76e5263e0f59e8233631e8a1d4171518d0e73d74))
* **openbao:** allow a permissions map on github/token write mints ([84ec5f9](https://github.com/dryvist/ansible-secrets-management/commit/84ec5f98ee3b55c9f133974c169247592b70b4dd))
* **openbao:** allow a permissions map on github/token write mints ([4f2a088](https://github.com/dryvist/ansible-secrets-management/commit/4f2a088f082d392c278741aa70c80b23035b7e62))
* **openbao:** allow fan-control write credential publication ([d130c4c](https://github.com/dryvist/ansible-secrets-management/commit/d130c4cbe57ef65c0ce88f1c524d5084ddcc12f5))
* **openbao:** allow terraform-apply to use the tofu-state transit key ([3c0c019](https://github.com/dryvist/ansible-secrets-management/commit/3c0c0195d1330db7d72d0ae96f38be7314995379))
* **openbao:** allow workflow file writes in the work write set ([#176](https://github.com/dryvist/ansible-secrets-management/issues/176)) ([24d78a0](https://github.com/dryvist/ansible-secrets-management/commit/24d78a0bd9adf2d29541e6abb25e9a03ee6060cf))
* **openbao:** attach the ai-apply-all policy set to agent-workstation ([#22](https://github.com/dryvist/ansible-secrets-management/issues/22)) ([b0c948c](https://github.com/dryvist/ansible-secrets-management/commit/b0c948c2c31f1e4a0dd547cb90d4cc34055ae6a1))
* **openbao:** bind the tofu-github role to per-org workspaces ([#202](https://github.com/dryvist/ansible-secrets-management/issues/202)) ([8a7e804](https://github.com/dryvist/ansible-secrets-management/commit/8a7e8046ad96ad395dc45048f27c5b31a70b80c5))
* **openbao:** classify declared AppRoles ([8f46148](https://github.com/dryvist/ansible-secrets-management/commit/8f461481b44346e16e7ef8b20fb16ce77a12d995))
* **openbao:** configure the Azure engine like the AWS engine ([697e64e](https://github.com/dryvist/ansible-secrets-management/commit/697e64e94e7c8e1c409bdc82fa366e05e5359354))
* **openbao:** configure the Azure secrets engine ([#93](https://github.com/dryvist/ansible-secrets-management/issues/93)) ([3eb1f05](https://github.com/dryvist/ansible-secrets-management/commit/3eb1f05abf60cb5564c4bab44df3216d455eb888))
* **openbao:** declare disclosure-denylist secret path and read policy ([#2177](https://github.com/dryvist/ansible-secrets-management/issues/2177)) ([7a975b7](https://github.com/dryvist/ansible-secrets-management/commit/7a975b799aa73b71b35697c9ecfdd872528f7600))
* **openbao:** declare transit mount and tofu-state key ([#216](https://github.com/dryvist/ansible-secrets-management/issues/216)) ([1494f59](https://github.com/dryvist/ansible-secrets-management/commit/1494f59c347368f8d54e6af68fde67da4879da61))
* **openbao:** define the untrusted dispatcher tier ([63ce58b](https://github.com/dryvist/ansible-secrets-management/commit/63ce58b65474cf1349f38f7cd836579e38b79694))
* **openbao:** derive roster agent AppRoles and policies ([#73](https://github.com/dryvist/ansible-secrets-management/issues/73)) ([deaaf89](https://github.com/dryvist/ansible-secrets-management/commit/deaaf898e1d8ecae6a21bc0aaaf7ff487c038699))
* **openbao:** drop consumer MCP grants once a roster agent owns the system ([96faa17](https://github.com/dryvist/ansible-secrets-management/commit/96faa174a0e9e985c614953d939b7726a7d21d95))
* **openbao:** drop consumer MCP grants once a roster agent owns the system ([#77](https://github.com/dryvist/ansible-secrets-management/issues/77)) ([5322ffb](https://github.com/dryvist/ansible-secrets-management/commit/5322ffb6e4b681c389d173e0d3c918bf61b47c3d))
* **openbao:** drop the github-write repository allowlist ([#2528](https://github.com/dryvist/ansible-secrets-management/issues/2528)) ([3cecb78](https://github.com/dryvist/ansible-secrets-management/commit/3cecb7860325c3c2a18fe2e62f0f7492537444d6))
* **openbao:** extend Hermes rotation and Context7 configuration ([#2332](https://github.com/dryvist/ansible-secrets-management/issues/2332)) ([2137e49](https://github.com/dryvist/ansible-secrets-management/commit/2137e49f61567308ed86db9d7bc6c3ccb6c006d6))
* **openbao:** extend publisher app catalog ([#192](https://github.com/dryvist/ansible-secrets-management/issues/192)) ([d130c4c](https://github.com/dryvist/ansible-secrets-management/commit/d130c4cbe57ef65c0ce88f1c524d5084ddcc12f5))
* **openbao:** generate a litellm-local-workstation router-key secret ([d667131](https://github.com/dryvist/ansible-secrets-management/commit/d667131d6a31586629572c1666ffe35f5ff7003e))
* **openbao:** generate a litellm-local-workstation router-key secret ([#2237](https://github.com/dryvist/ansible-secrets-management/issues/2237)) ([ba42db2](https://github.com/dryvist/ansible-secrets-management/commit/ba42db23b111c0a2b55103e31c4653dd9c750234))
* **openbao:** generate an A2A bearer token for the assistant guest ([eab9d97](https://github.com/dryvist/ansible-secrets-management/commit/eab9d97c8ad795574ae23c8883a7cf44d709bd85))
* **openbao:** generate an A2A bearer token for the assistant guest ([#70](https://github.com/dryvist/ansible-secrets-management/issues/70)) ([1539774](https://github.com/dryvist/ansible-secrets-management/commit/1539774706d7f0fb6cb2edb7ff739ceb761f66df))
* **openbao:** generate hermes_login_password for the vikunja app secret ([7fc49ac](https://github.com/dryvist/ansible-secrets-management/commit/7fc49acce32bd634d623544fd7e7e650b7bc6011))
* **openbao:** generate hermes_login_password for the vikunja app secret ([3c3f64a](https://github.com/dryvist/ansible-secrets-management/commit/3c3f64a0135846c9e849a2b5f3d84c0afa99edec))
* **openbao:** generate hindsight_api_key in apps/hindsight ([#2354](https://github.com/dryvist/ansible-secrets-management/issues/2354)) ([d5db8f9](https://github.com/dryvist/ansible-secrets-management/commit/d5db8f9b0dacdc6d70d6d50472cce61b6b3a0874))
* **openbao:** generate laya and decisions router secrets ([967dccd](https://github.com/dryvist/ansible-secrets-management/commit/967dccd77b099c8e6ef9d76f42fa9b6a2865715b))
* **openbao:** generate the codex-local router key ([#143](https://github.com/dryvist/ansible-secrets-management/issues/143)) ([b1979df](https://github.com/dryvist/ansible-secrets-management/commit/b1979dfbe579ee41f1b62e3030895c48089597e0))
* **openbao:** generate two router application secrets ([#155](https://github.com/dryvist/ansible-secrets-management/issues/155)) ([967dccd](https://github.com/dryvist/ansible-secrets-management/commit/967dccd77b099c8e6ef9d76f42fa9b6a2865715b))
* **openbao:** give the sandbox router key its own leaf ([#242](https://github.com/dryvist/ansible-secrets-management/issues/242)) ([de429e3](https://github.com/dryvist/ansible-secrets-management/commit/de429e32948d91b56c7296a821954a2254d15188))
* **openbao:** grant observability read on the OpenRouter usage key ([#2357](https://github.com/dryvist/ansible-secrets-management/issues/2357)) ([ecb22df](https://github.com/dryvist/ansible-secrets-management/commit/ecb22df15903d8afadc5c792ac14651b8fd69d23))
* **openbao:** grant read-only Splunk MCP access ([7e5d255](https://github.com/dryvist/ansible-secrets-management/commit/7e5d2558b46ff30d12c137e8d286988ac417a29c))
* **openbao:** grant read-only Splunk MCP access ([573a5cc](https://github.com/dryvist/ansible-secrets-management/commit/573a5cca9897b9e07baf06e6b9fb9bec6a5022b5))
* **openbao:** grant the apps read for the hermes orchestrator leaf ([a679589](https://github.com/dryvist/ansible-secrets-management/commit/a6795893cc95d850d049aaf3d24eb4e06d91ec74))
* **openbao:** grant the pve-exporter token publish path ([#2323](https://github.com/dryvist/ansible-secrets-management/issues/2323)) ([e2d66fb](https://github.com/dryvist/ansible-secrets-management/commit/e2d66fb3413dc353286949a80b0f39d5339722f1))
* **openbao:** isolate owned MCP access in dedicated local-llm policies ([#136](https://github.com/dryvist/ansible-secrets-management/issues/136)) ([ec5b9b2](https://github.com/dryvist/ansible-secrets-management/commit/ec5b9b2d62e386866dc0b85aed6daef4a1f6c617))
* **openbao:** keep plugin staging tasks unchanged ([446d55d](https://github.com/dryvist/ansible-secrets-management/commit/446d55d3461eb12313d47aaa3af9e03542cfe487))
* **openbao:** leave installation_id unpinned in the write policies ([#83](https://github.com/dryvist/ansible-secrets-management/issues/83)) ([91bb0a2](https://github.com/dryvist/ansible-secrets-management/commit/91bb0a25898a9f13f74e4916336bc8b71c5c9b3c))
* **openbao:** leave installation_id unpinned in the write policies ([#83](https://github.com/dryvist/ansible-secrets-management/issues/83)) ([e1f8f0f](https://github.com/dryvist/ansible-secrets-management/commit/e1f8f0fadb2f41b3a934374523b385d1bf858823))
* **openbao:** let the converge identity publish the open-llm bucket ([b751078](https://github.com/dryvist/ansible-secrets-management/commit/b751078e4158b2e43ba941007192ddde84508531))
* **openbao:** let the converge identity publish the open-llm bucket ([d2a956c](https://github.com/dryvist/ansible-secrets-management/commit/d2a956c76c44aebf4c409792409b7b84bf0227ff))
* **openbao:** let the sandbox write role read the sandbox leaf ([#204](https://github.com/dryvist/ansible-secrets-management/issues/204)) ([255b9f4](https://github.com/dryvist/ansible-secrets-management/commit/255b9f4df361a8c83e4a52c8e5057912bf0ceaee))
* **openbao:** let the semaphore role mint the jpe-cribl read token ([#142](https://github.com/dryvist/ansible-secrets-management/issues/142)) ([296a0c7](https://github.com/dryvist/ansible-secrets-management/commit/296a0c786bf86323aa070374f596e012f516172a))
* **openbao:** let the telemetry identity mint the read map ([#188](https://github.com/dryvist/ansible-secrets-management/issues/188)) ([f3c9416](https://github.com/dryvist/ansible-secrets-management/commit/f3c94160d96266e44bfca09f11ffcf471db0ff65))
* **openbao:** mint agents tokens by org name and read two role IDs ([#157](https://github.com/dryvist/ansible-secrets-management/issues/157)) ([b44409e](https://github.com/dryvist/ansible-secrets-management/commit/b44409eb9060e32d39965e4cdd2bf12ecb8acfa6))
* **openbao:** OIDC role for the central AI review workflow ([#191](https://github.com/dryvist/ansible-secrets-management/issues/191)) ([0af4708](https://github.com/dryvist/ansible-secrets-management/commit/0af470829e3fbe7c088f29f1e154d06fe1ff2da4))
* **openbao:** one-approval phone unlock for policy sync ([#223](https://github.com/dryvist/ansible-secrets-management/issues/223)) ([40f5fb1](https://github.com/dryvist/ansible-secrets-management/commit/40f5fb18d44c6f7a69b5c3163d574472bc4d834a))
* **openbao:** pinned read-only token mint in the exporter policy ([#194](https://github.com/dryvist/ansible-secrets-management/issues/194)) ([7f9e347](https://github.com/dryvist/ansible-secrets-management/commit/7f9e347a3bf335e41390dd61505266be6c39a15b))
* **openbao:** pinned reconcile attachments for two human-gated roles ([#269](https://github.com/dryvist/ansible-secrets-management/issues/269)) ([b23e670](https://github.com/dryvist/ansible-secrets-management/commit/b23e67028dfb88c178d8cd07dce60f4fe222aec8))
* **openbao:** port six ansible-proxmox-apps commits ([5ab3a03](https://github.com/dryvist/ansible-secrets-management/commit/5ab3a03dc1936310b89f94b1e4281f6fc36f5cfe))
* **openbao:** preserve owner MCP paths in fetch domains ([#132](https://github.com/dryvist/ansible-secrets-management/issues/132)) ([af5921a](https://github.com/dryvist/ansible-secrets-management/commit/af5921a4acfc56176dae8a77311c4f87ca3f990b))
* **openbao:** provision Qwen Code router key ([#66](https://github.com/dryvist/ansible-secrets-management/issues/66)) ([1d9b9fb](https://github.com/dryvist/ansible-secrets-management/commit/1d9b9fb6c71fec6c5a08b8eefe100ec8c78c93c2))
* **openbao:** report a missing Azure engine root config ([240169b](https://github.com/dryvist/ansible-secrets-management/commit/240169b12407ddc43327001b434c014d5005b1c3))
* **openbao:** rotate the agent-workstation secret_id on the domain schedule ([#41](https://github.com/dryvist/ansible-secrets-management/issues/41)) ([fa5bc47](https://github.com/dryvist/ansible-secrets-management/commit/fa5bc4772f05bb1a33d8abed9de81c8bed57371c))
* **openbao:** rotate the open-llm secret_id on the scheduled cadence ([#2356](https://github.com/dryvist/ansible-secrets-management/issues/2356)) ([b72d162](https://github.com/dryvist/ansible-secrets-management/commit/b72d162c94ada61b2ca0f6289419f95291c931c8))
* **openbao:** scope GitHub org secrets to a Terrakube workspace ([#237](https://github.com/dryvist/ansible-secrets-management/issues/237)) ([c332c91](https://github.com/dryvist/ansible-secrets-management/commit/c332c91f860ab801f4cfdd32905dc0096ddbcb38))
* **openbao:** seed per-agent router and gateway keys outside the apps grant ([#74](https://github.com/dryvist/ansible-secrets-management/issues/74)) ([243deb1](https://github.com/dryvist/ansible-secrets-management/commit/243deb1cdbbf4817a2da90d5d3f4293ac08b9ae0))
* **openbao:** seed sandbox and Claude router keys ([bed9ce4](https://github.com/dryvist/ansible-secrets-management/commit/bed9ce4fbce19f0ef78267d37bd5412e2d2d1c29))
* **openbao:** separate Azure IaC admin AppRole policies ([#135](https://github.com/dryvist/ansible-secrets-management/issues/135)) ([76c8560](https://github.com/dryvist/ansible-secrets-management/commit/76c8560b1ccd3186fc49d89a45c12900c4dc60bb))
* **openbao:** serve extra installations on the everyday GitHub mount ([#65](https://github.com/dryvist/ansible-secrets-management/issues/65)) ([cdc383e](https://github.com/dryvist/ansible-secrets-management/commit/cdc383e3d34cee6cd115253e2ea7eea10d7a136d))
* **openbao:** split dispatcher and sandbox secrets ([3b0308a](https://github.com/dryvist/ansible-secrets-management/commit/3b0308a6010fc4f064edacc4afef7ffb2f26f071))
* **openbao:** split GitHub engine mounts per App ([#2080](https://github.com/dryvist/ansible-secrets-management/issues/2080)) ([70d3891](https://github.com/dryvist/ansible-secrets-management/commit/70d3891b72ab798e29b8b48378731097cde740de))
* **openbao:** split github-work into read and write identities ([#2523](https://github.com/dryvist/ansible-secrets-management/issues/2523)) ([d7933e5](https://github.com/dryvist/ansible-secrets-management/commit/d7933e50ad2e60e91e3aa365a414841fab3e9302))
* **openbao:** use installation scope for general write tokens ([becae0a](https://github.com/dryvist/ansible-secrets-management/commit/becae0a305481104e45eb9b0f797e541e79489f8))
* **openbao:** use installation scope for general write tokens ([d94a45d](https://github.com/dryvist/ansible-secrets-management/commit/d94a45d9c8a94c58926648cafe73d9785c737d11))
* **openbao:** use per-call AppRole credentials ([#2437](https://github.com/dryvist/ansible-secrets-management/issues/2437)) ([152dc90](https://github.com/dryvist/ansible-secrets-management/commit/152dc905d46954f207fcb7e50b3947fd4fe68c37))
* **openbao:** validate GitHub App webhook and installation settings ([#2107](https://github.com/dryvist/ansible-secrets-management/issues/2107)) ([f376a49](https://github.com/dryvist/ansible-secrets-management/commit/f376a49e71b25253271989c2a37b3b0c22268988))
* **postgres:** optional Patroni/etcd HA mode behind postgres_ha_manager ([#2189](https://github.com/dryvist/ansible-secrets-management/issues/2189)) ([d17d540](https://github.com/dryvist/ansible-secrets-management/commit/d17d5402bcb489cf82630ae746abed2945714103))
* scaffold the secrets_management collection ([#1](https://github.com/dryvist/ansible-secrets-management/issues/1)) ([99308cf](https://github.com/dryvist/ansible-secrets-management/commit/99308cf2110d665a995a0cdcf1090a8bc4b92d66))
* schedule reconcile rotation ([ec0e531](https://github.com/dryvist/ansible-secrets-management/commit/ec0e53158f21219d2d17c24653f71f43ddf878b4))
* **scripts:** add a run wrapper for the controller-side playbooks ([#26](https://github.com/dryvist/ansible-secrets-management/issues/26)) ([f638da2](https://github.com/dryvist/ansible-secrets-management/commit/f638da2690b05571331a1c62e23235c1fb75afcb))
* shared ProxMan cluster ingress, DNS ownership, and workstation connection profile ([#2272](https://github.com/dryvist/ansible-secrets-management/issues/2272)) ([6c67a1e](https://github.com/dryvist/ansible-secrets-management/commit/6c67a1ec52e866aa7bdab9e2e5d053d4a0d64de4))
* **unpoller:** native poller + Cribl scrape + OpenBao credential ([#2174](https://github.com/dryvist/ansible-secrets-management/issues/2174)) ([468ada6](https://github.com/dryvist/ansible-secrets-management/commit/468ada6c932dc4aac6c2b23f9d7ff959f9978585))
* **vikunja:** provision the AI Jobs dispatcher token ([cce1b9b](https://github.com/dryvist/ansible-secrets-management/commit/cce1b9b761008cf6976e8a383c5d8b022033eb60))
* **vikunja:** provision the AI Jobs dispatcher token ([2464893](https://github.com/dryvist/ansible-secrets-management/commit/24648938052014cf0fa2d32af95bdc8c810ee09e))
* **wall:** serve the server-room wall ([#2139](https://github.com/dryvist/ansible-secrets-management/issues/2139)) ([4415583](https://github.com/dryvist/ansible-secrets-management/commit/4415583de001ab9aec4ea6c15be186143650be8b))
* **zammad,cribl_edge:** Security IDS group, svc-cribl identity, Edge IDS wiring ([#2257](https://github.com/dryvist/ansible-secrets-management/issues/2257)) ([1eea82d](https://github.com/dryvist/ansible-secrets-management/commit/1eea82d01701986b806296f83862b5167c9e1e9d))


### Bug Fixes

* align the domain catalog ([3b5aa10](https://github.com/dryvist/ansible-secrets-management/commit/3b5aa10965dd41c714bdbf62d4bb37cde0be0a1e))
* assert the single benchmark router key ([#2479](https://github.com/dryvist/ansible-secrets-management/issues/2479)) ([31c5ceb](https://github.com/dryvist/ansible-secrets-management/commit/31c5cebfe3bbb9dcdf11d8b982d7790206fe4d99))
* **authelia:** run controller-side staging under check mode ([#276](https://github.com/dryvist/ansible-secrets-management/issues/276)) ([eee1cce](https://github.com/dryvist/ansible-secrets-management/commit/eee1cce2530b58fe3f8dc39490aa95c79ee48589))
* **authelia:** size the token-endpoint rate limit for device-code polling ([f9e8776](https://github.com/dryvist/ansible-secrets-management/commit/f9e8776b7a28091d18a2ac25fa3e09002b9eb95f))
* **authelia:** size the token-endpoint rate limit for device-code polling ([#210](https://github.com/dryvist/ansible-secrets-management/issues/210)) ([fe1ecc2](https://github.com/dryvist/ansible-secrets-management/commit/fe1ecc2d09c61b192d77c81a1c34c45aca1078c8))
* **authelia:** strip the Digest prefix from service-user hashes ([#2222](https://github.com/dryvist/ansible-secrets-management/issues/2222)) ([81cd257](https://github.com/dryvist/ansible-secrets-management/commit/81cd25793c9299a1178d17ccd86757a2d037c54d))
* **authelia:** use a token-endpoint bucket period Authelia accepts ([#212](https://github.com/dryvist/ansible-secrets-management/issues/212)) ([e1fece7](https://github.com/dryvist/ansible-secrets-management/commit/e1fece7e564ce294e8aff1116544b43d8df80917))
* **auth:** parameterize role defaults ([#2443](https://github.com/dryvist/ansible-secrets-management/issues/2443)) ([1d1649f](https://github.com/dryvist/ansible-secrets-management/commit/1d1649f846ead60e78e9dcdb4050e89057f4e7e7))
* bound scheduled rotation catalog ([#2399](https://github.com/dryvist/ansible-secrets-management/issues/2399)) ([61fb541](https://github.com/dryvist/ansible-secrets-management/commit/61fb54150d94001ea0e303d57e24b6524422b7f1))
* bound scheduled rotation catalog ([#2399](https://github.com/dryvist/ansible-secrets-management/issues/2399)) ([bdfeaeb](https://github.com/dryvist/ansible-secrets-management/commit/bdfeaeb7f6b8d27fbb793d1756332d01ccf6422d))
* build router key paths from the consumer catalog ([7761562](https://github.com/dryvist/ansible-secrets-management/commit/7761562084a5252475d415541ee562eab506c2fe))
* **ci:** hold the workflow Python at 3.14 ([#205](https://github.com/dryvist/ansible-secrets-management/issues/205)) ([c89fbec](https://github.com/dryvist/ansible-secrets-management/commit/c89fbecd9e3cbbdb8118ea08686b5c118380cb52))
* **cribl_stream:** take openbao audit `_time` from the record ([#2516](https://github.com/dryvist/ansible-secrets-management/issues/2516)) ([a748e51](https://github.com/dryvist/ansible-secrets-management/commit/a748e51cd0c0f8dd076e5182f2703a935004f6f1))
* **deps:** require amazon.aws 11.3.0 or newer ([#259](https://github.com/dryvist/ansible-secrets-management/issues/259)) ([b900e5c](https://github.com/dryvist/ansible-secrets-management/commit/b900e5cefec98c29a160e2fd38024f3bf4b7f72b))
* **deps:** require amazon.aws for the published inventory resolver ([39c8fcc](https://github.com/dryvist/ansible-secrets-management/commit/39c8fcc933e2d7f90f12dc99e5d1192384fbd70b))
* **disclosure:** reword sensitive-category terms in comments and docs ([#2182](https://github.com/dryvist/ansible-secrets-management/issues/2182)) ([0ca9bff](https://github.com/dryvist/ansible-secrets-management/commit/0ca9bffe8c42635aeb4db34b443317643762b170))
* generate router keys through shared catalog ([#2474](https://github.com/dryvist/ansible-secrets-management/issues/2474)) ([3a109ab](https://github.com/dryvist/ansible-secrets-management/commit/3a109ab4abbdd3124447d0975002fd8249102c4c))
* **inventory:** preserve tag-selected secret coverage ([90d032c](https://github.com/dryvist/ansible-secrets-management/commit/90d032cca74a2b22b1759b66b810e83d837bb5c8))
* mint flow-lock IDs through approle-issuer ([8efc27d](https://github.com/dryvist/ansible-secrets-management/commit/8efc27d652ee7980e50997a02e3ce996de9fa59b))
* **ntfy:** single-quote the Zammad topic-group JSON in the subscriber env file ([#2486](https://github.com/dryvist/ansible-secrets-management/issues/2486)) ([55b3418](https://github.com/dryvist/ansible-secrets-management/commit/55b34185f3f9ac9161150a704284ee186a8961ce))
* **openbao_secrets:** decide a failed AppRole login without failing the task ([#2301](https://github.com/dryvist/ansible-secrets-management/issues/2301)) ([ba97921](https://github.com/dryvist/ansible-secrets-management/commit/ba979218bb0713e019c514768c53a6c52554dbcf))
* **openbao_secrets:** declare the local-cloud path optional ([#2293](https://github.com/dryvist/ansible-secrets-management/issues/2293)) ([7bf2124](https://github.com/dryvist/ansible-secrets-management/commit/7bf2124432dda1d1f6e9b47d7d8e647b961a05ae))
* **openbao_secrets:** keep an owner's own MCP path in its fetch domain ([41fca41](https://github.com/dryvist/ansible-secrets-management/commit/41fca410f73fce9ee623d0c7e4738852521417f3))
* **openbao_secrets:** run the endpoint probe in check mode ([#64](https://github.com/dryvist/ansible-secrets-management/issues/64)) ([9c40b51](https://github.com/dryvist/ansible-secrets-management/commit/9c40b51b9fbaaef6b0a455639982c0f818b3f22f))
* **openbao_secrets:** skip credential publishing in check mode ([#262](https://github.com/dryvist/ansible-secrets-management/issues/262)) ([5b64b13](https://github.com/dryvist/ansible-secrets-management/commit/5b64b13b47c88dd8448bb7df12772d95c1133840))
* **openbao_secrets:** take the issuer path only where flow-lock runs ([#2503](https://github.com/dryvist/ansible-secrets-management/issues/2503)) ([75f9f6c](https://github.com/dryvist/ansible-secrets-management/commit/75f9f6c4c98a59dd7969e66a29b4d417607e01a2))
* **openbao:** accept spent reconcile secret_id on accessor destroy ([#10](https://github.com/dryvist/ansible-secrets-management/issues/10)) ([e5629ab](https://github.com/dryvist/ansible-secrets-management/commit/e5629ab6110ee72858161ac903da49e4f377de41))
* **openbao:** add Semaphore reads for benchmark and sandbox-agent ([#247](https://github.com/dryvist/ansible-secrets-management/issues/247)) ([5cdaff4](https://github.com/dryvist/ansible-secrets-management/commit/5cdaff4b0367e8a254c33fdcd4ceea8cbcde5daf))
* **openbao:** add the Azure engine path to ai-admin-policy.hcl.j2 ([#101](https://github.com/dryvist/ansible-secrets-management/issues/101)) ([9c839cb](https://github.com/dryvist/ansible-secrets-management/commit/9c839cba7da149b7498b7af6e174179e298952af))
* **openbao:** ai-admin administers login MFA ([3f59c63](https://github.com/dryvist/ansible-secrets-management/commit/3f59c634f1b6f86f8d13c213270fe0abb1f9b9bf))
* **openbao:** ai-admin administers login MFA ([9016915](https://github.com/dryvist/ansible-secrets-management/commit/9016915c54b9d28163b54926a9238391056f300e))
* **openbao:** alert once per rotator failure streak ([#2515](https://github.com/dryvist/ansible-secrets-management/issues/2515)) ([f7a82d0](https://github.com/dryvist/ansible-secrets-management/commit/f7a82d0cdae13f5585d5b8904483995ef32b67ed))
* **openbao:** assert sandbox permission set mapping ([5de28ce](https://github.com/dryvist/ansible-secrets-management/commit/5de28ce3894bf3c974bd1784e3b4c53c423b40ff))
* **openbao:** attach ai-admin-guard to ai-admin-session only ([b5a8694](https://github.com/dryvist/ansible-secrets-management/commit/b5a86946a7b5da118eee8bce1272acd29932d837))
* **openbao:** authenticate the public repository listing on GitHub App mounts ([#169](https://github.com/dryvist/ansible-secrets-management/issues/169)) ([3aa4cd2](https://github.com/dryvist/ansible-secrets-management/commit/3aa4cd23d8475486f6c87520a4c474e29dcb41bc))
* **openbao:** bind the ai-sessions-backup AppRole to the workstation class ([81cef7d](https://github.com/dryvist/ansible-secrets-management/commit/81cef7dbd1a28ffef153d40502a0b882f331c797))
* **openbao:** bind the ai-sessions-backup AppRole to the workstation class ([0912923](https://github.com/dryvist/ansible-secrets-management/commit/091292381a6286b1656f2ee913fd5b4cf2eac9c3))
* **openbao:** bound reconcile policy and AppRole writes ([#221](https://github.com/dryvist/ansible-secrets-management/issues/221)) ([2f01f1e](https://github.com/dryvist/ansible-secrets-management/commit/2f01f1e63f42e163f263fd46c68bde4bc495d50c))
* **openbao:** compare /32 AppRole binds without the prefix length ([#2526](https://github.com/dryvist/ansible-secrets-management/issues/2526)) ([dbf96e2](https://github.com/dryvist/ansible-secrets-management/commit/dbf96e2112e7bb2ed3c12efdc19bbf8cb4142cf9))
* **openbao:** complete taxonomy and permission set fixture ([28dbc9c](https://github.com/dryvist/ansible-secrets-management/commit/28dbc9c6901e973ee652c992daecfbb0e1911981))
* **openbao:** count an empty JSON list as absent in the secret-age audit ([#60](https://github.com/dryvist/ansible-secrets-management/issues/60)) ([8c454be](https://github.com/dryvist/ansible-secrets-management/commit/8c454bedee94672ba097826d7cb29d08327bab7c))
* **openbao:** cover break-glass and reconcile readers in owner-only MCP grants ([e2bbeb5](https://github.com/dryvist/ansible-secrets-management/commit/e2bbeb58c52fa0447b350b468b620b7fa5d13007))
* **openbao:** create the denylist entry metadata with put when absent ([#2273](https://github.com/dryvist/ansible-secrets-management/issues/2273)) ([40e8589](https://github.com/dryvist/ansible-secrets-management/commit/40e85897f2a737dbdf97691fa922df0152271054))
* **openbao:** delegate generated secret writes through the CLI host ([e677200](https://github.com/dryvist/ansible-secrets-management/commit/e677200747bfadb1b771d93fb0ea388e9b96e43b))
* **openbao:** delegate the GitHub App check include to localhost ([#2270](https://github.com/dryvist/ansible-secrets-management/issues/2270)) ([65c0388](https://github.com/dryvist/ansible-secrets-management/commit/65c0388b426db360e677254d239dada38385b208))
* **openbao:** do not declare the Hermes policies without an installation ([#2448](https://github.com/dryvist/ansible-secrets-management/issues/2448)) ([79d7ca8](https://github.com/dryvist/ansible-secrets-management/commit/79d7ca8ad817ef53a728bb0e3bf510977bda799a))
* **openbao:** do not schedule the ci-resolver policy while its repository list is empty ([7152318](https://github.com/dryvist/ansible-secrets-management/commit/7152318a71fe4a20e626a11526674e36a3ce14fd))
* **openbao:** do not schedule the ci-resolver policy while its repository list is empty ([8749cec](https://github.com/dryvist/ansible-secrets-management/commit/8749cec03fe04cad78e65acb04edda3da58944e6))
* **openbao:** do not schedule the ci-resolver policy while its repository list is empty ([#84](https://github.com/dryvist/ansible-secrets-management/issues/84)) ([09de305](https://github.com/dryvist/ansible-secrets-management/commit/09de30587543c5e90357f6f8d016cdbdb4c02fa4))
* **openbao:** drop the Azure credential read from the terraform-apply policy ([bd22110](https://github.com/dryvist/ansible-secrets-management/commit/bd22110267642d492aadeb514132ce5eb592c4af))
* **openbao:** drop the stale scheduled-mode name load in the rotation play ([#2346](https://github.com/dryvist/ansible-secrets-management/issues/2346)) ([4762c6b](https://github.com/dryvist/ansible-secrets-management/commit/4762c6b4cac13730b1df19553cf924b91add6e55))
* **openbao:** end AppRole rotation before credential use in check mode ([9f8eac5](https://github.com/dryvist/ansible-secrets-management/commit/9f8eac56bdc0523ed1950b4a4d3e051296667667))
* **openbao:** end AppRole rotation before credential use in check mode ([#89](https://github.com/dryvist/ansible-secrets-management/issues/89)) ([6a84836](https://github.com/dryvist/ansible-secrets-management/commit/6a848366c67eb2eaf36b5f4b50583cccba903110))
* **openbao:** exclude the plane token's policies from reconcile ([#43](https://github.com/dryvist/ansible-secrets-management/issues/43)) ([164aaff](https://github.com/dryvist/ansible-secrets-management/commit/164aaff0cdddf3fd233ec9d1b71eeabe90ba8468))
* **openbao:** extend reconcile token session TTL ([626d70a](https://github.com/dryvist/ansible-secrets-management/commit/626d70ae12f6c7dfe6628626963bfc720ee67b1d))
* **openbao:** extend reconcile token session TTL ([86310ca](https://github.com/dryvist/ansible-secrets-management/commit/86310cad5b665cbf24c00230c3d6bf4cc1df549d))
* **openbao:** filter per-call env fields ([#257](https://github.com/dryvist/ansible-secrets-management/issues/257)) ([00adbce](https://github.com/dryvist/ansible-secrets-management/commit/00adbce890584a5450255cad91892c12c850831c))
* **openbao:** finish a rotation whose previous secret_id already expired ([#2258](https://github.com/dryvist/ansible-secrets-management/issues/2258)) ([617dfa5](https://github.com/dryvist/ansible-secrets-management/commit/617dfa5449f4a2aec377989b67c6833f4ebbe4a5))
* **openbao:** fold host-cert sign grant into existing signer policies ([#2210](https://github.com/dryvist/ansible-secrets-management/issues/2210)) ([437bbf8](https://github.com/dryvist/ansible-secrets-management/commit/437bbf84d55fe2db396da2066f6795a6b0f742cc))
* **openbao:** gate the rotation roster load on live roster readers ([#87](https://github.com/dryvist/ansible-secrets-management/issues/87)) ([54419b2](https://github.com/dryvist/ansible-secrets-management/commit/54419b24a91831750310f4b3e01922b67fdd0db4))
* **openbao:** generate the assistant guest router key and grant its apps path ([#67](https://github.com/dryvist/ansible-secrets-management/issues/67)) ([ea24f28](https://github.com/dryvist/ansible-secrets-management/commit/ea24f28cbd5ff926b46a4d06e517da2e8b84ea62))
* **openbao:** generate the donna router key and grant its apps path ([ea24f28](https://github.com/dryvist/ansible-secrets-management/commit/ea24f28cbd5ff926b46a4d06e517da2e8b84ea62))
* **openbao:** generate the monitoring GATUS_EXTERNAL_TOKEN ([#2172](https://github.com/dryvist/ansible-secrets-management/issues/2172)) ([546f0aa](https://github.com/dryvist/ansible-secrets-management/commit/546f0aa55f3fcc2fd350cf50e1eb8ed5405c5641))
* **openbao:** give open-llm the rotated-domain secret_id ttl ([#2518](https://github.com/dryvist/ansible-secrets-management/issues/2518)) ([3697109](https://github.com/dryvist/ansible-secrets-management/commit/36971098c32dff31395db6f8ec16af988519bdd3))
* **openbao:** grant apps reader published buckets ([#249](https://github.com/dryvist/ansible-secrets-management/issues/249)) ([674e6be](https://github.com/dryvist/ansible-secrets-management/commit/674e6be6b77a5b1225a7af896666faad77a7a576))
* **openbao:** grant reconcile the GitHub org-secrets Transit key ([#244](https://github.com/dryvist/ansible-secrets-management/issues/244)) ([cdb9c56](https://github.com/dryvist/ansible-secrets-management/commit/cdb9c569d013b70446fc8d73cf52f893f89e5d5a))
* **openbao:** grant Semaphore reads for benchmark and sandbox-agent ([5cdaff4](https://github.com/dryvist/ansible-secrets-management/commit/5cdaff4b0367e8a254c33fdcd4ceea8cbcde5daf))
* **openbao:** grant the admin policy the Azure engine mount ([0ee360c](https://github.com/dryvist/ansible-secrets-management/commit/0ee360c28e8b3f4c638c6e53a69030818b84850d))
* **openbao:** keep finite secret_id bounds on the open-llm AppRole ([7e88bb8](https://github.com/dryvist/ansible-secrets-management/commit/7e88bb81e170050b2f5a5c53811baa454286aa03))
* **openbao:** keep finite secret_id bounds on the open-llm AppRole ([2e9b0de](https://github.com/dryvist/ansible-secrets-management/commit/2e9b0def770e7b8493a37819c46bc8905bc0c915))
* **openbao:** keep finite secret_id bounds on the proxman AppRole ([0822829](https://github.com/dryvist/ansible-secrets-management/commit/082282939702dde6c1fa9ae955f067291cae3ef3))
* **openbao:** keep installation write scope opt-in ([#2336](https://github.com/dryvist/ansible-secrets-management/issues/2336)) ([#2342](https://github.com/dryvist/ansible-secrets-management/issues/2342)) ([c068d9f](https://github.com/dryvist/ansible-secrets-management/commit/c068d9f288dceec4df5183d898b7748a232ed274))
* **openbao:** keep the apps reader's grant on the pve-exporter bucket ([#2328](https://github.com/dryvist/ansible-secrets-management/issues/2328)) ([9eda50e](https://github.com/dryvist/ansible-secrets-management/commit/9eda50ed1922db727a82c0dd26e2cff7114bf358))
* **openbao:** keep the github-runner mount and policy declared without App credentials ([#227](https://github.com/dryvist/ansible-secrets-management/issues/227)) ([f910708](https://github.com/dryvist/ansible-secrets-management/commit/f91070814db2da88ebe6662c7c827444138a3c2b))
* **openbao:** keep the internal Z.ai copy until the external leaf is seeded ([#139](https://github.com/dryvist/ansible-secrets-management/issues/139)) ([d7f28eb](https://github.com/dryvist/ansible-secrets-management/commit/d7f28eb5f6df9179d9f1835b4bb3b43142e7b9d9))
* **openbao:** keep the nodes' seal key id when the environment sets none ([#2244](https://github.com/dryvist/ansible-secrets-management/issues/2244)) ([e8d8d81](https://github.com/dryvist/ansible-secrets-management/commit/e8d8d81ed22501c28812387c7b470276dfddd373))
* **openbao:** leave write installation_id unpinned and skip the empty ci-resolver policy ([#85](https://github.com/dryvist/ansible-secrets-management/issues/85)) ([147b771](https://github.com/dryvist/ansible-secrets-management/commit/147b771e8c7cf3aa3680e087bda693835bf15f82))
* **openbao:** let semaphore mint read-only tokens by org on the everyday mount ([#173](https://github.com/dryvist/ansible-secrets-management/issues/173)) ([091a7f5](https://github.com/dryvist/ansible-secrets-management/commit/091a7f5e3aed3884e1f023d7f45b37cb09549c68))
* **openbao:** load the agent roster before rotating AppRole secret IDs ([f7259f7](https://github.com/dryvist/ansible-secrets-management/commit/f7259f7aebfd4962a1ce1d34888df7e581b4c341))
* **openbao:** load the agent roster before rotating AppRole secret IDs ([#82](https://github.com/dryvist/ansible-secrets-management/issues/82)) ([48cc113](https://github.com/dryvist/ansible-secrets-management/commit/48cc11363d2f74f4814270319c51c20d7692d4d6))
* **openbao:** load the scheduled identity's name from 05g in the rotation play ([b2add5c](https://github.com/dryvist/ansible-secrets-management/commit/b2add5cefb2b467b3a65d9deae0f51fb3854f652))
* **openbao:** load the scheduled identity's name from 05g in the rotation play ([3e7534c](https://github.com/dryvist/ansible-secrets-management/commit/3e7534c47bdd84fc9d8f0135601715d8e40faffa))
* **openbao:** mask the role_id read in domain rotation ([#2371](https://github.com/dryvist/ansible-secrets-management/issues/2371)) ([d3af608](https://github.com/dryvist/ansible-secrets-management/commit/d3af608a81667febe7dd4e29a1802827ab5c200d))
* **openbao:** mint the claude-ocg router key with the sk- prefix ([#149](https://github.com/dryvist/ansible-secrets-management/issues/149)) ([912be28](https://github.com/dryvist/ansible-secrets-management/commit/912be28d342fe8f1b940a6d68fd3253827fd9656))
* **openbao:** move owned MCP denies to a dedicated local-llm policy ([ad07b7f](https://github.com/dryvist/ansible-secrets-management/commit/ad07b7f2ffb5c587f545b502c1f2e92494fa3e6f))
* **openbao:** non-expiring class-bound secret_ids for standing identities ([#2509](https://github.com/dryvist/ansible-secrets-management/issues/2509)) ([6d4e47a](https://github.com/dryvist/ansible-secrets-management/commit/6d4e47a646c2db98d7bf0073b6c4ea7990587b8f))
* **openbao:** parse the live AppRole list as a bare array ([#2351](https://github.com/dryvist/ansible-secrets-management/issues/2351)) ([15f3246](https://github.com/dryvist/ansible-secrets-management/commit/15f3246f20e1f003b8e3d499d866d2d4b2e77e0d))
* **openbao:** persist the audit imfile read offset ([#2521](https://github.com/dryvist/ansible-secrets-management/issues/2521)) ([a2f5115](https://github.com/dryvist/ansible-secrets-management/commit/a2f5115c7e240703ef4f44dfab898cc1e19f17b8))
* **openbao:** pin reconcile AppRole TTL and use-count parameters ([#222](https://github.com/dryvist/ansible-secrets-management/issues/222)) ([53c861d](https://github.com/dryvist/ansible-secrets-management/commit/53c861d6a0cf77783cd9050821564a198f2c266c))
* **openbao:** preserve finite write realm bounds ([#2339](https://github.com/dryvist/ansible-secrets-management/issues/2339)) ([1e44f41](https://github.com/dryvist/ansible-secrets-management/commit/1e44f41c3da496ed1413992ab1d7ff6a715fa4a4))
* **openbao:** print the working policy-sync command ([#240](https://github.com/dryvist/ansible-secrets-management/issues/240)) ([3356173](https://github.com/dryvist/ansible-secrets-management/commit/335617335c0a5dc03d36971fe6e953c9bb59f939))
* **openbao:** prove workstation-bound rotated pairs by lookup ([#2149](https://github.com/dryvist/ansible-secrets-management/issues/2149)) ([fe78ec8](https://github.com/dryvist/ansible-secrets-management/commit/fe78ec8778fe89ab5d86b022b0e88e19e220f670))
* **openbao:** read the App install allowlist from the env document ([#2268](https://github.com/dryvist/ansible-secrets-management/issues/2268)) ([0127aad](https://github.com/dryvist/ansible-secrets-management/commit/0127aad84cda0c438ad435f3a25f9756c3ab6ade))
* **openbao:** read the rotator's Doppler target from the platform env doc ([#2127](https://github.com/dryvist/ansible-secrets-management/issues/2127)) ([99c77fd](https://github.com/dryvist/ansible-secrets-management/commit/99c77fd87b0cd79ee1dece1c2ae917f3fdf87830))
* **openbao:** reconcile through per-call issuer ([#2446](https://github.com/dryvist/ansible-secrets-management/issues/2446)) ([588ac6b](https://github.com/dryvist/ansible-secrets-management/commit/588ac6b1c1a8a9101fb96da2587bd7aa7b0c4105))
* **openbao:** refresh apt cache before installing prerequisites ([#158](https://github.com/dryvist/ansible-secrets-management/issues/158)) ([986eeeb](https://github.com/dryvist/ansible-secrets-management/commit/986eeebcbb853f7501bac2885749c033b7ab3766))
* **openbao:** refuse preset roster probe results and gate the rotation tests ([6d62b90](https://github.com/dryvist/ansible-secrets-management/commit/6d62b909bd9d85110bf89df9ab5931fbb0766d8b))
* **openbao:** refuse to render the voter-health env file without a HEC token ([#2531](https://github.com/dryvist/ansible-secrets-management/issues/2531)) ([34502b9](https://github.com/dryvist/ansible-secrets-management/commit/34502b9aab8c2cf29fbe84348dda472e46fb1ab6))
* **openbao:** register the telemetry exporter identity ([#265](https://github.com/dryvist/ansible-secrets-management/issues/265)) ([a303737](https://github.com/dryvist/ansible-secrets-management/commit/a303737c5e2714c1b2999de35c7e095f1974d8e7))
* **openbao:** republish rotated workstation AppRole pairs into Doppler ([#2120](https://github.com/dryvist/ansible-secrets-management/issues/2120)) ([15cf20d](https://github.com/dryvist/ansible-secrets-management/commit/15cf20dec40a31f3c72b7737d4ed2c43b58da164))
* **openbao:** require the snapshot unit and skip the restart in check mode ([e7007ef](https://github.com/dryvist/ansible-secrets-management/commit/e7007efbbc167acd8e65b29f66134211aea9f8dd))
* **openbao:** restart notified voters one at a time ([#2519](https://github.com/dryvist/ansible-secrets-management/issues/2519)) ([684e155](https://github.com/dryvist/ansible-secrets-management/commit/684e15596a77058ea3cc7933e1537662e626cbe5))
* **openbao:** restore Cribl Mac rotation catalog ([e43cc9d](https://github.com/dryvist/ansible-secrets-management/commit/e43cc9d587408c4e7f39b297158d0f0f7eb249e3))
* **openbao:** rotate the ai-donna AppRole secret_id with the other agent identities ([#2465](https://github.com/dryvist/ansible-secrets-management/issues/2465)) ([b8ef9b2](https://github.com/dryvist/ansible-secrets-management/commit/b8ef9b2fd575c0b87fbb764ab2b8f18dbdcfcef6))
* **openbao:** run init store calls on the CLI host ([a305c3b](https://github.com/dryvist/ansible-secrets-management/commit/a305c3b7f9996d918ac50fe063a4d7af38df509f))
* **openbao:** run init store calls on the CLI host ([505ae3e](https://github.com/dryvist/ansible-secrets-management/commit/505ae3e03f351c4a44ca41b54ebba47b9145eb32))
* **openbao:** run policy-sync before reconcile-grant consumers ([#2219](https://github.com/dryvist/ansible-secrets-management/issues/2219)) ([a5b30d9](https://github.com/dryvist/ansible-secrets-management/commit/a5b30d9c297bf6246a1731792adca7bb33fef521))
* **openbao:** run policy-sync capability check and write from the controller ([#2221](https://github.com/dryvist/ansible-secrets-management/issues/2221)) ([a461dd0](https://github.com/dryvist/ansible-secrets-management/commit/a461dd002fb6a1e1a2f19f48c6a3c310cd3810cb))
* **openbao:** run the init path's read-only probes in check mode ([#71](https://github.com/dryvist/ansible-secrets-management/issues/71)) ([5e37787](https://github.com/dryvist/ansible-secrets-management/commit/5e377873d8bb4ec0f6f8678ee562007f0b3fd435))
* **openbao:** run the reconcile credential chain in check mode ([#281](https://github.com/dryvist/ansible-secrets-management/issues/281)) ([30e43e7](https://github.com/dryvist/ansible-secrets-management/commit/30e43e7fcc953338c22d2ef93dfe92ccc433627a))
* **openbao:** run the undeclared-live AppRole calls on the CLI host ([#2450](https://github.com/dryvist/ansible-secrets-management/issues/2450)) ([fecf6af](https://github.com/dryvist/ansible-secrets-management/commit/fecf6af8a903a4eee2d6ad2b06f4dc09a4262ad9))
* **openbao:** scheduled AppRole rotation renews itself first and survives a failed domain ([#2510](https://github.com/dryvist/ansible-secrets-management/issues/2510)) ([19d268f](https://github.com/dryvist/ansible-secrets-management/commit/19d268f230b8ce164260def3abe726540d2e4e15))
* **openbao:** scope Semaphore policy read access ([#255](https://github.com/dryvist/ansible-secrets-management/issues/255)) ([62de769](https://github.com/dryvist/ansible-secrets-management/commit/62de7690ac022582d1fcb9e9d9320090b532c8da))
* **openbao:** scrub environment-specific names from init tasks ([#2259](https://github.com/dryvist/ansible-secrets-management/issues/2259)) ([7b6fa02](https://github.com/dryvist/ansible-secrets-management/commit/7b6fa02e6f7e437a3a027e2798186a6ae54780dc))
* **openbao:** send subscription_id in the Azure engine config ([35d95a3](https://github.com/dryvist/ansible-secrets-management/commit/35d95a315063ef0f619fdc4bb5f33006236ecddd))
* **openbao:** send subscription_id in the Azure engine config ([#114](https://github.com/dryvist/ansible-secrets-management/issues/114)) ([f95dcaf](https://github.com/dryvist/ansible-secrets-management/commit/f95dcafc1918ded4838293c8e802d2fae61d8dbb))
* **openbao:** send the app-secret promote write from the CLI host ([#2452](https://github.com/dryvist/ansible-secrets-management/issues/2452)) ([7709979](https://github.com/dryvist/ansible-secrets-management/commit/770997926a5b48c8cdb0a8692708aa0e19d9783e))
* **openbao:** send the declared AppRole parameters with the existence read ([#229](https://github.com/dryvist/ansible-secrets-management/issues/229)) ([5681784](https://github.com/dryvist/ansible-secrets-management/commit/568178400bbc65307b69226296657c92b5dc752a))
* **openbao:** set ansible_become false on the delegated App check include ([#2271](https://github.com/dryvist/ansible-secrets-management/issues/2271)) ([1bafa69](https://github.com/dryvist/ansible-secrets-management/commit/1bafa69f1fb7fb35e39db939d7723189e4f6d3fb))
* **openbao:** single policy field on the github-exporter role entry ([#195](https://github.com/dryvist/ansible-secrets-management/issues/195)) ([50c0d6c](https://github.com/dryvist/ansible-secrets-management/commit/50c0d6c767d2e9ae2a157b27360369c3d50ef651))
* **openbao:** skip rolling restarts in check mode ([521f6ee](https://github.com/dryvist/ansible-secrets-management/commit/521f6ee2fc0f2bbee212bfe43e763d0bf44e8750))
* **openbao:** skip rolling restarts in check mode ([#181](https://github.com/dryvist/ansible-secrets-management/issues/181)) ([86cf4af](https://github.com/dryvist/ansible-secrets-management/commit/86cf4af5dd9c8b2077d39891e247f8228613b3c8))
* **openbao:** skip the Doppler sync-token read on a seed run ([#2131](https://github.com/dryvist/ansible-secrets-management/issues/2131)) ([e18fa98](https://github.com/dryvist/ansible-secrets-management/commit/e18fa98311d2e36123ad49140dbd489f26426fb2))
* **openbao:** skip the package install task in check mode ([e0ae4a2](https://github.com/dryvist/ansible-secrets-management/commit/e0ae4a20f44826be9a86229daab96ef4fc7ee5ff))
* **openbao:** skip the package install task in check mode ([#180](https://github.com/dryvist/ansible-secrets-management/issues/180)) ([c16b6f6](https://github.com/dryvist/ansible-secrets-management/commit/c16b6f67b3e3416aa3358a8fc9c61a4adc664b9a))
* **openbao:** snapshot and restart on a version upgrade ([57ea8ca](https://github.com/dryvist/ansible-secrets-management/commit/57ea8ca17dd597e842bcc23a183eb93416b4ebba))
* **openbao:** snapshot and restart on a version upgrade ([#90](https://github.com/dryvist/ansible-secrets-management/issues/90)) ([29994ea](https://github.com/dryvist/ansible-secrets-management/commit/29994ea3ae67fe8b220ff170301067e4def66a4c))
* **openbao:** start the observability Splunk grant on its own line ([#147](https://github.com/dryvist/ansible-secrets-management/issues/147)) ([54b4ed7](https://github.com/dryvist/ansible-secrets-management/commit/54b4ed7f128563911a60437e8ce2b5ecbecd5685))
* **openbao:** tag and order the per-App GitHub mount phase ([#2514](https://github.com/dryvist/ansible-secrets-management/issues/2514)) ([f0687fa](https://github.com/dryvist/ansible-secrets-management/commit/f0687fa9ddb51a993281272a09fa9e26255be2e8))
* **openbao:** the exporter AppRole holds only the exporter policy ([50c0d6c](https://github.com/dryvist/ansible-secrets-management/commit/50c0d6c767d2e9ae2a157b27360369c3d50ef651))
* **openbao:** treat an empty Azure engine client_id as missing config ([04f63ec](https://github.com/dryvist/ansible-secrets-management/commit/04f63ecf5291bc3dd8b2f36bba6ef094b9787bd0))
* **openbao:** treat an empty Azure engine client_id as missing config ([#107](https://github.com/dryvist/ansible-secrets-management/issues/107)) ([a85ff41](https://github.com/dryvist/ansible-secrets-management/commit/a85ff412ad5b4cbf86ac36dc76feb925485e273e))
* **openbao:** unlimited secret_id uses for local-llm, hermes and ai-donna ([#2524](https://github.com/dryvist/ansible-secrets-management/issues/2524)) ([7d89ed6](https://github.com/dryvist/ansible-secrets-management/commit/7d89ed6b4a1b47ecc8ead52c5212c2c0063dedd2))
* **openbao:** write KV secret values through the API, never argv ([#2370](https://github.com/dryvist/ansible-secrets-management/issues/2370)) ([a07dced](https://github.com/dryvist/ansible-secrets-management/commit/a07dcedcc1e58b4e7e7a945c7e85b27cb9da7b18))
* **openbao:** write reachable RBAC policies before failing on an ungranted name ([#2213](https://github.com/dryvist/ansible-secrets-management/issues/2213)) ([ad4d62d](https://github.com/dryvist/ansible-secrets-management/commit/ad4d62d488ab96d0fa32a7fd65893679a32f8e87))
* split webhook workspace access by mount ([#275](https://github.com/dryvist/ansible-secrets-management/issues/275)) ([8373dab](https://github.com/dryvist/ansible-secrets-management/commit/8373dab34d31e40471b595f369dca6a621c0131d))
* **unpoller:** read the UniFi controller address from OpenBao via the prefetch ([#2227](https://github.com/dryvist/ansible-secrets-management/issues/2227)) ([0749376](https://github.com/dryvist/ansible-secrets-management/commit/07493764074a302a4f9e6aa11a953ffd783641ff))


### Performance

* **openbao:** add openbao_kv_seed tag and controller-side policy reads ([#2193](https://github.com/dryvist/ansible-secrets-management/issues/2193)) ([bf7386c](https://github.com/dryvist/ansible-secrets-management/commit/bf7386c5326efdb04bdd832d05a5cdeec4017c51))
* **openbao:** resolve the AppRole parameter maps once per run ([#231](https://github.com/dryvist/ansible-secrets-management/issues/231)) ([f7335d4](https://github.com/dryvist/ansible-secrets-management/commit/f7335d40f72565b0cef3a2da895c1fa07a01544e))
* **openbao:** run the AppRole, SSH role and policy writes on openbao_cli_host ([c5f9307](https://github.com/dryvist/ansible-secrets-management/commit/c5f9307dd51c64a517f75361c702f0718659b67d))
* **openbao:** run the AppRole, SSH role and policy writes on openbao_cli_host ([34ef30a](https://github.com/dryvist/ansible-secrets-management/commit/34ef30a79f71b0530aec558b66ee324bc4eb6000))
* **secrets:** scope the OpenBao pre-fetch to domains this run's hosts need ([#2183](https://github.com/dryvist/ansible-secrets-management/issues/2183)) ([bad4da3](https://github.com/dryvist/ansible-secrets-management/commit/bad4da3c46444eab5e117322bd435bd3f1423571))

## [0.33.3](https://github.com/dryvist/ansible-secrets-management/compare/v0.33.2...v0.33.3) (2026-10-21)


### Bug Fixes

* **openbao:** run the reconcile credential chain in check mode ([#281](https://github.com/dryvist/ansible-secrets-management/issues/281)) ([30e43e7](https://github.com/dryvist/ansible-secrets-management/commit/30e43e7fcc953338c22d2ef93dfe92ccc433627a))

## [0.33.2](https://github.com/dryvist/ansible-secrets-management/compare/v0.33.1...v0.33.2) (2026-10-21)


### Bug Fixes

* split webhook workspace access by mount ([#275](https://github.com/dryvist/ansible-secrets-management/issues/275)) ([8373dab](https://github.com/dryvist/ansible-secrets-management/commit/8373dab34d31e40471b595f369dca6a621c0131d))

## [0.33.1](https://github.com/dryvist/ansible-secrets-management/compare/v0.33.0...v0.33.1) (2026-10-21)


### Bug Fixes

* **authelia:** run controller-side staging under check mode ([#276](https://github.com/dryvist/ansible-secrets-management/issues/276)) ([eee1cce](https://github.com/dryvist/ansible-secrets-management/commit/eee1cce2530b58fe3f8dc39490aa95c79ee48589))

## [0.33.0](https://github.com/dryvist/ansible-secrets-management/compare/v0.32.0...v0.33.0) (2026-10-20)


### Features

* **openbao_secrets:** add PostgreSQL backup S3 domain ([#272](https://github.com/dryvist/ansible-secrets-management/issues/272)) ([eb0646a](https://github.com/dryvist/ansible-secrets-management/commit/eb0646a752c2fc6be41ed78273d59cb224358966))

## [0.32.0](https://github.com/dryvist/ansible-secrets-management/compare/v0.31.4...v0.32.0) (2026-10-20)


### Features

* **openbao:** pinned reconcile attachments for two human-gated roles ([#269](https://github.com/dryvist/ansible-secrets-management/issues/269)) ([b23e670](https://github.com/dryvist/ansible-secrets-management/commit/b23e67028dfb88c178d8cd07dce60f4fe222aec8))

## [0.31.4](https://github.com/dryvist/ansible-secrets-management/compare/v0.31.3...v0.31.4) (2026-10-20)


### Bug Fixes

* **openbao:** register the telemetry exporter identity ([#265](https://github.com/dryvist/ansible-secrets-management/issues/265)) ([a303737](https://github.com/dryvist/ansible-secrets-management/commit/a303737c5e2714c1b2999de35c7e095f1974d8e7))

## [0.31.3](https://github.com/dryvist/ansible-secrets-management/compare/v0.31.2...v0.31.3) (2026-10-20)


### Bug Fixes

* **openbao_secrets:** skip credential publishing in check mode ([#262](https://github.com/dryvist/ansible-secrets-management/issues/262)) ([5b64b13](https://github.com/dryvist/ansible-secrets-management/commit/5b64b13b47c88dd8448bb7df12772d95c1133840))

## [0.31.2](https://github.com/dryvist/ansible-secrets-management/compare/v0.31.1...v0.31.2) (2026-10-20)


### Bug Fixes

* **deps:** require amazon.aws 11.3.0 or newer ([#259](https://github.com/dryvist/ansible-secrets-management/issues/259)) ([b900e5c](https://github.com/dryvist/ansible-secrets-management/commit/b900e5cefec98c29a160e2fd38024f3bf4b7f72b))
* **openbao:** filter per-call env fields ([#257](https://github.com/dryvist/ansible-secrets-management/issues/257)) ([00adbce](https://github.com/dryvist/ansible-secrets-management/commit/00adbce890584a5450255cad91892c12c850831c))

## [0.31.1](https://github.com/dryvist/ansible-secrets-management/compare/v0.31.0...v0.31.1) (2026-10-20)


### Bug Fixes

* **openbao:** scope Semaphore policy read access ([#255](https://github.com/dryvist/ansible-secrets-management/issues/255)) ([62de769](https://github.com/dryvist/ansible-secrets-management/commit/62de7690ac022582d1fcb9e9d9320090b532c8da))

## [0.31.0](https://github.com/dryvist/ansible-secrets-management/compare/v0.30.1...v0.31.0) (2026-10-20)


### Features

* **openbao:** add a github-personal App mount with one write set ([#251](https://github.com/dryvist/ansible-secrets-management/issues/251)) ([96bcd1d](https://github.com/dryvist/ansible-secrets-management/commit/96bcd1d1d45fb5ac6ed636afb7cd2e56df2e3aac))


### Bug Fixes

* **openbao:** grant apps reader published buckets ([#249](https://github.com/dryvist/ansible-secrets-management/issues/249)) ([674e6be](https://github.com/dryvist/ansible-secrets-management/commit/674e6be6b77a5b1225a7af896666faad77a7a576))

## [0.30.1](https://github.com/dryvist/ansible-secrets-management/compare/v0.30.0...v0.30.1) (2026-10-19)


### Bug Fixes

* **openbao:** add Semaphore reads for benchmark and sandbox-agent ([#247](https://github.com/dryvist/ansible-secrets-management/issues/247)) ([5cdaff4](https://github.com/dryvist/ansible-secrets-management/commit/5cdaff4b0367e8a254c33fdcd4ceea8cbcde5daf))
* **openbao:** grant Semaphore reads for benchmark and sandbox-agent ([5cdaff4](https://github.com/dryvist/ansible-secrets-management/commit/5cdaff4b0367e8a254c33fdcd4ceea8cbcde5daf))

## [0.30.0](https://github.com/dryvist/ansible-secrets-management/compare/v0.29.1...v0.30.0) (2026-10-19)


### Features

* **openbao:** give the sandbox router key its own leaf ([#242](https://github.com/dryvist/ansible-secrets-management/issues/242)) ([de429e3](https://github.com/dryvist/ansible-secrets-management/commit/de429e32948d91b56c7296a821954a2254d15188))


### Bug Fixes

* **openbao:** grant reconcile the GitHub org-secrets Transit key ([#244](https://github.com/dryvist/ansible-secrets-management/issues/244)) ([cdb9c56](https://github.com/dryvist/ansible-secrets-management/commit/cdb9c569d013b70446fc8d73cf52f893f89e5d5a))

## [0.29.1](https://github.com/dryvist/ansible-secrets-management/compare/v0.29.0...v0.29.1) (2026-10-18)


### Bug Fixes

* **openbao:** print the working policy-sync command ([#240](https://github.com/dryvist/ansible-secrets-management/issues/240)) ([3356173](https://github.com/dryvist/ansible-secrets-management/commit/335617335c0a5dc03d36971fe6e953c9bb59f939))

## [0.29.0](https://github.com/dryvist/ansible-secrets-management/compare/v0.28.0...v0.29.0) (2026-10-18)


### Features

* **openbao:** scope GitHub org secrets to a Terrakube workspace ([#237](https://github.com/dryvist/ansible-secrets-management/issues/237)) ([c332c91](https://github.com/dryvist/ansible-secrets-management/commit/c332c91f860ab801f4cfdd32905dc0096ddbcb38))

## [0.28.0](https://github.com/dryvist/ansible-secrets-management/compare/v0.27.1...v0.28.0) (2026-10-18)


### Features

* **openbao:** add a tofu-state transit AppRole ([#234](https://github.com/dryvist/ansible-secrets-management/issues/234)) ([0127a07](https://github.com/dryvist/ansible-secrets-management/commit/0127a0782bc0f7814cd87604fc4bd7608edeaf06))
* **openbao:** add a workstation-bound tofu-state transit AppRole ([0127a07](https://github.com/dryvist/ansible-secrets-management/commit/0127a0782bc0f7814cd87604fc4bd7608edeaf06))

## [0.27.1](https://github.com/dryvist/ansible-secrets-management/compare/v0.27.0...v0.27.1) (2026-10-18)


### Bug Fixes

* **openbao:** keep the github-runner mount and policy declared without App credentials ([#227](https://github.com/dryvist/ansible-secrets-management/issues/227)) ([f910708](https://github.com/dryvist/ansible-secrets-management/commit/f91070814db2da88ebe6662c7c827444138a3c2b))
* **openbao:** send the declared AppRole parameters with the existence read ([#229](https://github.com/dryvist/ansible-secrets-management/issues/229)) ([5681784](https://github.com/dryvist/ansible-secrets-management/commit/568178400bbc65307b69226296657c92b5dc752a))


### Performance

* **openbao:** resolve the AppRole parameter maps once per run ([#231](https://github.com/dryvist/ansible-secrets-management/issues/231)) ([f7335d4](https://github.com/dryvist/ansible-secrets-management/commit/f7335d40f72565b0cef3a2da895c1fa07a01544e))

## [0.27.0](https://github.com/dryvist/ansible-secrets-management/compare/v0.26.0...v0.27.0) (2026-10-17)


### Features

* **openbao:** add github-runner mount for runner registration by org ([#225](https://github.com/dryvist/ansible-secrets-management/issues/225)) ([79b42b8](https://github.com/dryvist/ansible-secrets-management/commit/79b42b89f9e1a82b2f90959549b60d07a3ef5e85))
* **openbao:** add tofu-state transit paths to terraform-apply policy ([#218](https://github.com/dryvist/ansible-secrets-management/issues/218)) ([3c0c019](https://github.com/dryvist/ansible-secrets-management/commit/3c0c0195d1330db7d72d0ae96f38be7314995379))
* **openbao:** add tofu-state transit paths to the ai-admin policy ([#220](https://github.com/dryvist/ansible-secrets-management/issues/220)) ([8d05b4e](https://github.com/dryvist/ansible-secrets-management/commit/8d05b4edc1f5da3cf8c0d8c2b6a9d8fbf273c4bd))
* **openbao:** add transit paths to the reconcile policy ([#219](https://github.com/dryvist/ansible-secrets-management/issues/219)) ([a98bc52](https://github.com/dryvist/ansible-secrets-management/commit/a98bc529590d62f32b2b38ca348222bb5acee27b))
* **openbao:** allow terraform-apply to use the tofu-state transit key ([3c0c019](https://github.com/dryvist/ansible-secrets-management/commit/3c0c0195d1330db7d72d0ae96f38be7314995379))
* **openbao:** one-approval phone unlock for policy sync ([#223](https://github.com/dryvist/ansible-secrets-management/issues/223)) ([40f5fb1](https://github.com/dryvist/ansible-secrets-management/commit/40f5fb18d44c6f7a69b5c3163d574472bc4d834a))


### Bug Fixes

* **openbao:** bound reconcile policy and AppRole writes ([#221](https://github.com/dryvist/ansible-secrets-management/issues/221)) ([2f01f1e](https://github.com/dryvist/ansible-secrets-management/commit/2f01f1e63f42e163f263fd46c68bde4bc495d50c))
* **openbao:** pin reconcile AppRole TTL and use-count parameters ([#222](https://github.com/dryvist/ansible-secrets-management/issues/222)) ([53c861d](https://github.com/dryvist/ansible-secrets-management/commit/53c861d6a0cf77783cd9050821564a198f2c266c))

## [0.26.0](https://github.com/dryvist/ansible-secrets-management/compare/v0.25.1...v0.26.0) (2026-10-17)


### Features

* **openbao:** declare transit mount and tofu-state key ([#216](https://github.com/dryvist/ansible-secrets-management/issues/216)) ([1494f59](https://github.com/dryvist/ansible-secrets-management/commit/1494f59c347368f8d54e6af68fde67da4879da61))


### Bug Fixes

* **authelia:** use a token-endpoint bucket period Authelia accepts ([#212](https://github.com/dryvist/ansible-secrets-management/issues/212)) ([e1fece7](https://github.com/dryvist/ansible-secrets-management/commit/e1fece7e564ce294e8aff1116544b43d8df80917))

## [0.25.1](https://github.com/dryvist/ansible-secrets-management/compare/v0.25.0...v0.25.1) (2026-10-17)


### Bug Fixes

* **authelia:** size the token-endpoint rate limit for device-code polling ([f9e8776](https://github.com/dryvist/ansible-secrets-management/commit/f9e8776b7a28091d18a2ac25fa3e09002b9eb95f))
* **authelia:** size the token-endpoint rate limit for device-code polling ([#210](https://github.com/dryvist/ansible-secrets-management/issues/210)) ([fe1ecc2](https://github.com/dryvist/ansible-secrets-management/commit/fe1ecc2d09c61b192d77c81a1c34c45aca1078c8))

## [0.25.0](https://github.com/dryvist/ansible-secrets-management/compare/v0.24.0...v0.25.0) (2026-10-17)


### Features

* **openbao:** let the sandbox write role read the sandbox leaf ([#204](https://github.com/dryvist/ansible-secrets-management/issues/204)) ([255b9f4](https://github.com/dryvist/ansible-secrets-management/commit/255b9f4df361a8c83e4a52c8e5057912bf0ceaee))

## [0.24.0](https://github.com/dryvist/ansible-secrets-management/compare/v0.23.0...v0.24.0) (2026-10-17)


### Features

* **openbao:** admin set and Terrakube identity per GitHub org ([#190](https://github.com/dryvist/ansible-secrets-management/issues/190)) ([76e5263](https://github.com/dryvist/ansible-secrets-management/commit/76e5263e0f59e8233631e8a1d4171518d0e73d74))
* **openbao:** allow fan-control write credential publication ([d130c4c](https://github.com/dryvist/ansible-secrets-management/commit/d130c4cbe57ef65c0ce88f1c524d5084ddcc12f5))
* **openbao:** bind the tofu-github role to per-org workspaces ([#202](https://github.com/dryvist/ansible-secrets-management/issues/202)) ([8a7e804](https://github.com/dryvist/ansible-secrets-management/commit/8a7e8046ad96ad395dc45048f27c5b31a70b80c5))
* **openbao:** extend publisher app catalog ([#192](https://github.com/dryvist/ansible-secrets-management/issues/192)) ([d130c4c](https://github.com/dryvist/ansible-secrets-management/commit/d130c4cbe57ef65c0ce88f1c524d5084ddcc12f5))
* **openbao:** OIDC role for the central AI review workflow ([#191](https://github.com/dryvist/ansible-secrets-management/issues/191)) ([0af4708](https://github.com/dryvist/ansible-secrets-management/commit/0af470829e3fbe7c088f29f1e154d06fe1ff2da4))
* **openbao:** pinned read-only token mint in the exporter policy ([#194](https://github.com/dryvist/ansible-secrets-management/issues/194)) ([7f9e347](https://github.com/dryvist/ansible-secrets-management/commit/7f9e347a3bf335e41390dd61505266be6c39a15b))


### Bug Fixes

* **ci:** hold the workflow Python at 3.14 ([#205](https://github.com/dryvist/ansible-secrets-management/issues/205)) ([c89fbec](https://github.com/dryvist/ansible-secrets-management/commit/c89fbecd9e3cbbdb8118ea08686b5c118380cb52))
* **openbao:** single policy field on the github-exporter role entry ([#195](https://github.com/dryvist/ansible-secrets-management/issues/195)) ([50c0d6c](https://github.com/dryvist/ansible-secrets-management/commit/50c0d6c767d2e9ae2a157b27360369c3d50ef651))
* **openbao:** the exporter AppRole holds only the exporter policy ([50c0d6c](https://github.com/dryvist/ansible-secrets-management/commit/50c0d6c767d2e9ae2a157b27360369c3d50ef651))

## [0.23.0](https://github.com/dryvist/ansible-secrets-management/compare/v0.22.0...v0.23.0) (2026-10-17)


### Features

* **openbao:** let the telemetry identity mint the read map ([#188](https://github.com/dryvist/ansible-secrets-management/issues/188)) ([f3c9416](https://github.com/dryvist/ansible-secrets-management/commit/f3c94160d96266e44bfca09f11ffcf471db0ff65))

## [0.22.0](https://github.com/dryvist/ansible-secrets-management/compare/v0.21.0...v0.22.0) (2026-10-16)


### Features

* **openbao:** add a work-admin permission set ([#183](https://github.com/dryvist/ansible-secrets-management/issues/183)) ([d0a5af4](https://github.com/dryvist/ansible-secrets-management/commit/d0a5af46103fab0b847977d7774fe62e5fbb8ce3))
* **openbao:** add the work-admin GitHub tier ([d0a5af4](https://github.com/dryvist/ansible-secrets-management/commit/d0a5af46103fab0b847977d7774fe62e5fbb8ce3))


### Bug Fixes

* **openbao:** skip rolling restarts in check mode ([#181](https://github.com/dryvist/ansible-secrets-management/issues/181)) ([86cf4af](https://github.com/dryvist/ansible-secrets-management/commit/86cf4af5dd9c8b2077d39891e247f8228613b3c8))
* **openbao:** skip the package install task in check mode ([#180](https://github.com/dryvist/ansible-secrets-management/issues/180)) ([c16b6f6](https://github.com/dryvist/ansible-secrets-management/commit/c16b6f67b3e3416aa3358a8fc9c61a4adc664b9a))

## [0.21.0](https://github.com/dryvist/ansible-secrets-management/compare/v0.20.1...v0.21.0) (2026-10-15)


### Features

* **openbao:** allow workflow file writes in the work write set ([#176](https://github.com/dryvist/ansible-secrets-management/issues/176)) ([24d78a0](https://github.com/dryvist/ansible-secrets-management/commit/24d78a0bd9adf2d29541e6abb25e9a03ee6060cf))

## [0.20.1](https://github.com/dryvist/ansible-secrets-management/compare/v0.20.0...v0.20.1) (2026-10-15)


### Bug Fixes

* **openbao:** let semaphore mint read-only tokens by org on the everyday mount ([#173](https://github.com/dryvist/ansible-secrets-management/issues/173)) ([091a7f5](https://github.com/dryvist/ansible-secrets-management/commit/091a7f5e3aed3884e1f023d7f45b37cb09549c68))

## [0.20.0](https://github.com/dryvist/ansible-secrets-management/compare/v0.19.0...v0.20.0) (2026-10-14)


### Features

* **openbao:** add the herdr-hail workstation AppRole ([#168](https://github.com/dryvist/ansible-secrets-management/issues/168)) ([a19574a](https://github.com/dryvist/ansible-secrets-management/commit/a19574ab5ce61bad9c9690aea662d1fd2f8511b0))


### Bug Fixes

* **openbao:** authenticate the public repository listing on GitHub App mounts ([#169](https://github.com/dryvist/ansible-secrets-management/issues/169)) ([3aa4cd2](https://github.com/dryvist/ansible-secrets-management/commit/3aa4cd23d8475486f6c87520a4c474e29dcb41bc))

## [0.19.0](https://github.com/dryvist/ansible-secrets-management/compare/v0.18.0...v0.19.0) (2026-10-14)


### Features

* **authelia:** generate the trusted elevation client secret ([#166](https://github.com/dryvist/ansible-secrets-management/issues/166)) ([50952a9](https://github.com/dryvist/ansible-secrets-management/commit/50952a9b054890fde3e1b4d72b2089da1654b6d7))
* **authelia:** generate the trusted elevation client secret and use client_secret_basic ([5370088](https://github.com/dryvist/ansible-secrets-management/commit/5370088a97db8facfb9e7331162edc9f90a2e410))

## [0.18.0](https://github.com/dryvist/ansible-secrets-management/compare/v0.17.1...v0.18.0) (2026-10-14)


### Features

* **openbao:** add owner-neutral GitHub token grants ([#163](https://github.com/dryvist/ansible-secrets-management/issues/163)) ([6270354](https://github.com/dryvist/ansible-secrets-management/commit/627035489ce67a6bfeac15c38be6ce3baea3f129))
* **openbao:** mint agents tokens by org name and read two role IDs ([#157](https://github.com/dryvist/ansible-secrets-management/issues/157)) ([b44409e](https://github.com/dryvist/ansible-secrets-management/commit/b44409eb9060e32d39965e4cdd2bf12ecb8acfa6))

## [0.17.1](https://github.com/dryvist/ansible-secrets-management/compare/v0.17.0...v0.17.1) (2026-10-14)


### Bug Fixes

* **openbao:** refresh apt cache before installing prerequisites ([#158](https://github.com/dryvist/ansible-secrets-management/issues/158)) ([986eeeb](https://github.com/dryvist/ansible-secrets-management/commit/986eeebcbb853f7501bac2885749c033b7ab3766))

## [0.17.0](https://github.com/dryvist/ansible-secrets-management/compare/v0.16.1...v0.17.0) (2026-10-14)


### Features

* **openbao:** generate laya and decisions router secrets ([967dccd](https://github.com/dryvist/ansible-secrets-management/commit/967dccd77b099c8e6ef9d76f42fa9b6a2865715b))
* **openbao:** generate two router application secrets ([#155](https://github.com/dryvist/ansible-secrets-management/issues/155)) ([967dccd](https://github.com/dryvist/ansible-secrets-management/commit/967dccd77b099c8e6ef9d76f42fa9b6a2865715b))

## [0.16.1](https://github.com/dryvist/ansible-secrets-management/compare/v0.16.0...v0.16.1) (2026-10-13)


### Bug Fixes

* **openbao:** mint the claude-ocg router key with the sk- prefix ([#149](https://github.com/dryvist/ansible-secrets-management/issues/149)) ([912be28](https://github.com/dryvist/ansible-secrets-management/commit/912be28d342fe8f1b940a6d68fd3253827fd9656))

## [0.16.0](https://github.com/dryvist/ansible-secrets-management/compare/v0.15.0...v0.16.0) (2026-10-13)


### Features

* **openbao:** generate the codex-local router key ([#143](https://github.com/dryvist/ansible-secrets-management/issues/143)) ([b1979df](https://github.com/dryvist/ansible-secrets-management/commit/b1979dfbe579ee41f1b62e3030895c48089597e0))
* **openbao:** isolate owned MCP access in dedicated local-llm policies ([#136](https://github.com/dryvist/ansible-secrets-management/issues/136)) ([ec5b9b2](https://github.com/dryvist/ansible-secrets-management/commit/ec5b9b2d62e386866dc0b85aed6daef4a1f6c617))
* **openbao:** preserve owner MCP paths in fetch domains ([#132](https://github.com/dryvist/ansible-secrets-management/issues/132)) ([af5921a](https://github.com/dryvist/ansible-secrets-management/commit/af5921a4acfc56176dae8a77311c4f87ca3f990b))
* **openbao:** separate Azure IaC admin AppRole policies ([#135](https://github.com/dryvist/ansible-secrets-management/issues/135)) ([76c8560](https://github.com/dryvist/ansible-secrets-management/commit/76c8560b1ccd3186fc49d89a45c12900c4dc60bb))


### Bug Fixes

* **openbao:** start the observability Splunk grant on its own line ([#147](https://github.com/dryvist/ansible-secrets-management/issues/147)) ([54b4ed7](https://github.com/dryvist/ansible-secrets-management/commit/54b4ed7f128563911a60437e8ce2b5ecbecd5685))

## [0.15.0](https://github.com/dryvist/ansible-secrets-management/compare/v0.14.0...v0.15.0) (2026-10-13)


### Features

* **openbao:** let the semaphore role mint the jpe-cribl read token ([#142](https://github.com/dryvist/ansible-secrets-management/issues/142)) ([296a0c7](https://github.com/dryvist/ansible-secrets-management/commit/296a0c786bf86323aa070374f596e012f516172a))

## [0.14.0](https://github.com/dryvist/ansible-secrets-management/compare/v0.13.0...v0.14.0) (2026-10-13)


### Features

* **openbao:** add sandbox agent AppRoles and identity classes ([#128](https://github.com/dryvist/ansible-secrets-management/issues/128)) ([1fbcca7](https://github.com/dryvist/ansible-secrets-management/commit/1fbcca78cf78532177dde2ebe3ed9cbce6fdd99c))


### Bug Fixes

* **openbao:** keep the internal Z.ai copy until the external leaf is seeded ([#139](https://github.com/dryvist/ansible-secrets-management/issues/139)) ([d7f28eb](https://github.com/dryvist/ansible-secrets-management/commit/d7f28eb5f6df9179d9f1835b4bb3b43142e7b9d9))

## [0.13.0](https://github.com/dryvist/ansible-secrets-management/compare/v0.12.0...v0.13.0) (2026-10-13)


### Features

* **openbao:** add the hermes orchestrator generated app secret ([#129](https://github.com/dryvist/ansible-secrets-management/issues/129)) ([dba4b84](https://github.com/dryvist/ansible-secrets-management/commit/dba4b84927d706a3cc32fafaebe764bc4ef97f62))
* **openbao:** grant the apps read for the hermes orchestrator leaf ([a679589](https://github.com/dryvist/ansible-secrets-management/commit/a6795893cc95d850d049aaf3d24eb4e06d91ec74))

## [0.12.0](https://github.com/dryvist/ansible-secrets-management/compare/v0.11.0...v0.12.0) (2026-10-12)


### Features

* **openbao:** add per-organisation repo-create permission sets ([7742019](https://github.com/dryvist/ansible-secrets-management/commit/7742019de807a0ce1fdd7f51f4cf432a2a88b384))
* **openbao:** add per-organisation repo-create permission sets ([#123](https://github.com/dryvist/ansible-secrets-management/issues/123)) ([1ea7e1a](https://github.com/dryvist/ansible-secrets-management/commit/1ea7e1af92f713b8056b88c8187d6dcc4d2043ad))

## [0.11.0](https://github.com/dryvist/ansible-secrets-management/compare/v0.10.1...v0.11.0) (2026-10-12)


### Features

* **openbao:** add the azure-iac-admin AppRole and policy ([#119](https://github.com/dryvist/ansible-secrets-management/issues/119)) ([e2e5065](https://github.com/dryvist/ansible-secrets-management/commit/e2e5065a388f861d480ff9a2a0d7a6f499808a32))

## [0.10.1](https://github.com/dryvist/ansible-secrets-management/compare/v0.10.0...v0.10.1) (2026-10-12)


### Bug Fixes

* **openbao:** send subscription_id in the Azure engine config ([35d95a3](https://github.com/dryvist/ansible-secrets-management/commit/35d95a315063ef0f619fdc4bb5f33006236ecddd))
* **openbao:** send subscription_id in the Azure engine config ([#114](https://github.com/dryvist/ansible-secrets-management/issues/114)) ([f95dcaf](https://github.com/dryvist/ansible-secrets-management/commit/f95dcafc1918ded4838293c8e802d2fae61d8dbb))

## [0.10.0](https://github.com/dryvist/ansible-secrets-management/compare/v0.9.1...v0.10.0) (2026-10-12)


### Features

* **openbao:** add per-engine component tags ([#105](https://github.com/dryvist/ansible-secrets-management/issues/105)) ([a883ff2](https://github.com/dryvist/ansible-secrets-management/commit/a883ff2eba591796c68c28ac23bdb4555478acf2))
* **openbao:** keep plugin staging tasks unchanged ([446d55d](https://github.com/dryvist/ansible-secrets-management/commit/446d55d3461eb12313d47aaa3af9e03542cfe487))


### Bug Fixes

* **openbao:** treat an empty Azure engine client_id as missing config ([04f63ec](https://github.com/dryvist/ansible-secrets-management/commit/04f63ecf5291bc3dd8b2f36bba6ef094b9787bd0))
* **openbao:** treat an empty Azure engine client_id as missing config ([#107](https://github.com/dryvist/ansible-secrets-management/issues/107)) ([a85ff41](https://github.com/dryvist/ansible-secrets-management/commit/a85ff412ad5b4cbf86ac36dc76feb925485e273e))

## [0.9.1](https://github.com/dryvist/ansible-secrets-management/compare/v0.9.0...v0.9.1) (2026-10-12)


### Bug Fixes

* **openbao:** add the Azure engine path to ai-admin-policy.hcl.j2 ([#101](https://github.com/dryvist/ansible-secrets-management/issues/101)) ([9c839cb](https://github.com/dryvist/ansible-secrets-management/commit/9c839cba7da149b7498b7af6e174179e298952af))
* **openbao:** grant the admin policy the Azure engine mount ([0ee360c](https://github.com/dryvist/ansible-secrets-management/commit/0ee360c28e8b3f4c638c6e53a69030818b84850d))

## [0.9.0](https://github.com/dryvist/ansible-secrets-management/compare/v0.8.0...v0.9.0) (2026-10-12)


### Features

* **openbao:** configure the Azure secrets engine ([#93](https://github.com/dryvist/ansible-secrets-management/issues/93)) ([3eb1f05](https://github.com/dryvist/ansible-secrets-management/commit/3eb1f05abf60cb5564c4bab44df3216d455eb888))


### Bug Fixes

* **openbao:** end AppRole rotation before credential use in check mode ([#89](https://github.com/dryvist/ansible-secrets-management/issues/89)) ([6a84836](https://github.com/dryvist/ansible-secrets-management/commit/6a848366c67eb2eaf36b5f4b50583cccba903110))

## [0.8.0](https://github.com/dryvist/ansible-secrets-management/compare/v0.7.1...v0.8.0) (2026-10-12)


### Features

* **openbao_secrets:** drop owned MCP paths from non-owner fetch domains ([#78](https://github.com/dryvist/ansible-secrets-management/issues/78)) ([499d28d](https://github.com/dryvist/ansible-secrets-management/commit/499d28dedcc3b6c27a994cb0f24209ca324ca1aa))
* **openbao:** add azure secrets engine with roles from environment ([#88](https://github.com/dryvist/ansible-secrets-management/issues/88)) ([1242bf2](https://github.com/dryvist/ansible-secrets-management/commit/1242bf2bd980218d54200e6d467d4432c5e1177c))
* **openbao:** add router and gateway reader roles for roster agent keys ([#75](https://github.com/dryvist/ansible-secrets-management/issues/75)) ([39f1a6e](https://github.com/dryvist/ansible-secrets-management/commit/39f1a6ede05ea360d6db6b64684b3242e23a79fd))
* **openbao:** derive roster agent AppRoles and policies ([#73](https://github.com/dryvist/ansible-secrets-management/issues/73)) ([deaaf89](https://github.com/dryvist/ansible-secrets-management/commit/deaaf898e1d8ecae6a21bc0aaaf7ff487c038699))
* **openbao:** drop consumer MCP grants once a roster agent owns the system ([#77](https://github.com/dryvist/ansible-secrets-management/issues/77)) ([5322ffb](https://github.com/dryvist/ansible-secrets-management/commit/5322ffb6e4b681c389d173e0d3c918bf61b47c3d))
* **openbao:** generate an A2A bearer token for the assistant guest ([eab9d97](https://github.com/dryvist/ansible-secrets-management/commit/eab9d97c8ad795574ae23c8883a7cf44d709bd85))
* **openbao:** generate an A2A bearer token for the assistant guest ([#70](https://github.com/dryvist/ansible-secrets-management/issues/70)) ([1539774](https://github.com/dryvist/ansible-secrets-management/commit/1539774706d7f0fb6cb2edb7ff739ceb761f66df))
* **openbao:** leave installation_id unpinned in the write policies ([#83](https://github.com/dryvist/ansible-secrets-management/issues/83)) ([91bb0a2](https://github.com/dryvist/ansible-secrets-management/commit/91bb0a25898a9f13f74e4916336bc8b71c5c9b3c))
* **openbao:** leave installation_id unpinned in the write policies ([#83](https://github.com/dryvist/ansible-secrets-management/issues/83)) ([e1f8f0f](https://github.com/dryvist/ansible-secrets-management/commit/e1f8f0fadb2f41b3a934374523b385d1bf858823))
* **openbao:** provision Qwen Code router key ([#66](https://github.com/dryvist/ansible-secrets-management/issues/66)) ([1d9b9fb](https://github.com/dryvist/ansible-secrets-management/commit/1d9b9fb6c71fec6c5a08b8eefe100ec8c78c93c2))
* **openbao:** seed per-agent router and gateway keys outside the apps grant ([#74](https://github.com/dryvist/ansible-secrets-management/issues/74)) ([243deb1](https://github.com/dryvist/ansible-secrets-management/commit/243deb1cdbbf4817a2da90d5d3f4293ac08b9ae0))
* **openbao:** serve extra installations on the everyday GitHub mount ([#65](https://github.com/dryvist/ansible-secrets-management/issues/65)) ([cdc383e](https://github.com/dryvist/ansible-secrets-management/commit/cdc383e3d34cee6cd115253e2ea7eea10d7a136d))


### Bug Fixes

* **openbao_secrets:** run the endpoint probe in check mode ([#64](https://github.com/dryvist/ansible-secrets-management/issues/64)) ([9c40b51](https://github.com/dryvist/ansible-secrets-management/commit/9c40b51b9fbaaef6b0a455639982c0f818b3f22f))
* **openbao:** do not schedule the ci-resolver policy while its repository list is empty ([7152318](https://github.com/dryvist/ansible-secrets-management/commit/7152318a71fe4a20e626a11526674e36a3ce14fd))
* **openbao:** do not schedule the ci-resolver policy while its repository list is empty ([8749cec](https://github.com/dryvist/ansible-secrets-management/commit/8749cec03fe04cad78e65acb04edda3da58944e6))
* **openbao:** do not schedule the ci-resolver policy while its repository list is empty ([#84](https://github.com/dryvist/ansible-secrets-management/issues/84)) ([09de305](https://github.com/dryvist/ansible-secrets-management/commit/09de30587543c5e90357f6f8d016cdbdb4c02fa4))
* **openbao:** gate the rotation roster load on live roster readers ([#87](https://github.com/dryvist/ansible-secrets-management/issues/87)) ([54419b2](https://github.com/dryvist/ansible-secrets-management/commit/54419b24a91831750310f4b3e01922b67fdd0db4))
* **openbao:** generate the assistant guest router key and grant its apps path ([#67](https://github.com/dryvist/ansible-secrets-management/issues/67)) ([ea24f28](https://github.com/dryvist/ansible-secrets-management/commit/ea24f28cbd5ff926b46a4d06e517da2e8b84ea62))
* **openbao:** generate the donna router key and grant its apps path ([ea24f28](https://github.com/dryvist/ansible-secrets-management/commit/ea24f28cbd5ff926b46a4d06e517da2e8b84ea62))
* **openbao:** leave write installation_id unpinned and skip the empty ci-resolver policy ([#85](https://github.com/dryvist/ansible-secrets-management/issues/85)) ([147b771](https://github.com/dryvist/ansible-secrets-management/commit/147b771e8c7cf3aa3680e087bda693835bf15f82))
* **openbao:** load the agent roster before rotating AppRole secret IDs ([f7259f7](https://github.com/dryvist/ansible-secrets-management/commit/f7259f7aebfd4962a1ce1d34888df7e581b4c341))
* **openbao:** load the agent roster before rotating AppRole secret IDs ([#82](https://github.com/dryvist/ansible-secrets-management/issues/82)) ([48cc113](https://github.com/dryvist/ansible-secrets-management/commit/48cc11363d2f74f4814270319c51c20d7692d4d6))
* **openbao:** require the snapshot unit and skip the restart in check mode ([e7007ef](https://github.com/dryvist/ansible-secrets-management/commit/e7007efbbc167acd8e65b29f66134211aea9f8dd))
* **openbao:** run the init path's read-only probes in check mode ([#71](https://github.com/dryvist/ansible-secrets-management/issues/71)) ([5e37787](https://github.com/dryvist/ansible-secrets-management/commit/5e377873d8bb4ec0f6f8678ee562007f0b3fd435))
* **openbao:** snapshot and restart on a version upgrade ([57ea8ca](https://github.com/dryvist/ansible-secrets-management/commit/57ea8ca17dd597e842bcc23a183eb93416b4ebba))
* **openbao:** snapshot and restart on a version upgrade ([#90](https://github.com/dryvist/ansible-secrets-management/issues/90)) ([29994ea](https://github.com/dryvist/ansible-secrets-management/commit/29994ea3ae67fe8b220ff170301067e4def66a4c))

## [0.7.1](https://github.com/dryvist/ansible-secrets-management/compare/v0.7.0...v0.7.1) (2026-10-11)


### Bug Fixes

* **openbao:** count an empty JSON list as absent in the secret-age audit ([#60](https://github.com/dryvist/ansible-secrets-management/issues/60)) ([8c454be](https://github.com/dryvist/ansible-secrets-management/commit/8c454bedee94672ba097826d7cb29d08327bab7c))

## [0.7.0](https://github.com/dryvist/ansible-secrets-management/compare/v0.6.0...v0.7.0) (2026-10-11)


### Features

* **openbao:** add the ci-resolver GitHub identity ([#53](https://github.com/dryvist/ansible-secrets-management/issues/53)) ([7eca696](https://github.com/dryvist/ansible-secrets-management/commit/7eca69625ada89e662c8de7fe170921e69988ac3))

## [0.6.0](https://github.com/dryvist/ansible-secrets-management/compare/v0.5.0...v0.6.0) (2026-10-11)


### Features

* **openbao:** add the ai-admin-guard deny overlay ([4b13726](https://github.com/dryvist/ansible-secrets-management/commit/4b137261d56e20bce67011145c75ffeae34aef06))
* **openbao:** add the github-enterprise-owner mount and the ai-admin-guard overlay ([#48](https://github.com/dryvist/ansible-secrets-management/issues/48)) ([a1b7dc6](https://github.com/dryvist/ansible-secrets-management/commit/a1b7dc66bb398fde7408478b08ebd0be2c0db5e7))
* **openbao:** add the github-enterprise-owner token mount ([e4f413b](https://github.com/dryvist/ansible-secrets-management/commit/e4f413b8c585926c9f8e37a77fb5af7c55ea7832))


### Bug Fixes

* **openbao:** attach ai-admin-guard to ai-admin-session only ([b5a8694](https://github.com/dryvist/ansible-secrets-management/commit/b5a86946a7b5da118eee8bce1272acd29932d837))

## [0.5.0](https://github.com/dryvist/ansible-secrets-management/compare/v0.4.0...v0.5.0) (2026-10-11)


### Features

* **openbao:** add GitHub Enterprise App mounts and inert tiers ([#30](https://github.com/dryvist/ansible-secrets-management/issues/30)) ([278493a](https://github.com/dryvist/ansible-secrets-management/commit/278493a9e3732616fa41d0160465ac37b3830268))
* **openbao:** rotate the agent-workstation secret_id on the domain schedule ([#41](https://github.com/dryvist/ansible-secrets-management/issues/41)) ([fa5bc47](https://github.com/dryvist/ansible-secrets-management/commit/fa5bc4772f05bb1a33d8abed9de81c8bed57371c))


### Bug Fixes

* **openbao:** exclude the plane token's policies from reconcile ([#43](https://github.com/dryvist/ansible-secrets-management/issues/43)) ([164aaff](https://github.com/dryvist/ansible-secrets-management/commit/164aaff0cdddf3fd233ec9d1b71eeabe90ba8468))

## [0.4.0](https://github.com/dryvist/ansible-secrets-management/compare/v0.3.1...v0.4.0) (2026-10-11)


### Features

* **authelia:** add OpenBao elevation device-code clients and elevate policy ([#24](https://github.com/dryvist/ansible-secrets-management/issues/24)) ([7fa9ed2](https://github.com/dryvist/ansible-secrets-management/commit/7fa9ed2df1dbe47c65fe3d70109bca3287a2a1c0))
* **openbao:** add the Authelia JWT elevation roles and a 1h work-identity token ([#25](https://github.com/dryvist/ansible-secrets-management/issues/25)) ([7127d8b](https://github.com/dryvist/ansible-secrets-management/commit/7127d8b0dac6dbe1b7c458fb11569cbcec99c242))
* **openbao:** attach the ai-apply-all policy set to agent-workstation ([#22](https://github.com/dryvist/ansible-secrets-management/issues/22)) ([b0c948c](https://github.com/dryvist/ansible-secrets-management/commit/b0c948c2c31f1e4a0dd547cb90d4cc34055ae6a1))
* **scripts:** add a run wrapper for the controller-side playbooks ([#26](https://github.com/dryvist/ansible-secrets-management/issues/26)) ([f638da2](https://github.com/dryvist/ansible-secrets-management/commit/f638da2690b05571331a1c62e23235c1fb75afcb))

## [0.3.1](https://github.com/dryvist/ansible-secrets-management/compare/v0.3.0...v0.3.1) (2026-10-10)


### Bug Fixes

* **openbao:** accept spent reconcile secret_id on accessor destroy ([#10](https://github.com/dryvist/ansible-secrets-management/issues/10)) ([e5629ab](https://github.com/dryvist/ansible-secrets-management/commit/e5629ab6110ee72858161ac903da49e4f377de41))

## [0.3.0](https://github.com/dryvist/ansible-secrets-management/compare/v0.2.0...v0.3.0) (2026-10-10)


### ⚠ BREAKING CHANGES

* **openbao:** drop the github-write repository allowlist ([#2528](https://github.com/dryvist/ansible-secrets-management/issues/2528))

### Features

* **openbao:** drop the github-write repository allowlist ([#2528](https://github.com/dryvist/ansible-secrets-management/issues/2528)) ([3cecb78](https://github.com/dryvist/ansible-secrets-management/commit/3cecb7860325c3c2a18fe2e62f0f7492537444d6))
* **openbao:** port six ansible-proxmox-apps commits ([5ab3a03](https://github.com/dryvist/ansible-secrets-management/commit/5ab3a03dc1936310b89f94b1e4281f6fc36f5cfe))
* **openbao:** split github-work into read and write identities ([#2523](https://github.com/dryvist/ansible-secrets-management/issues/2523)) ([d7933e5](https://github.com/dryvist/ansible-secrets-management/commit/d7933e50ad2e60e91e3aa365a414841fab3e9302))


### Bug Fixes

* **openbao:** compare /32 AppRole binds without the prefix length ([#2526](https://github.com/dryvist/ansible-secrets-management/issues/2526)) ([dbf96e2](https://github.com/dryvist/ansible-secrets-management/commit/dbf96e2112e7bb2ed3c12efdc19bbf8cb4142cf9))
* **openbao:** refuse to render the voter-health env file without a HEC token ([#2531](https://github.com/dryvist/ansible-secrets-management/issues/2531)) ([34502b9](https://github.com/dryvist/ansible-secrets-management/commit/34502b9aab8c2cf29fbe84348dda472e46fb1ab6))
* **openbao:** unlimited secret_id uses for local-llm, hermes and ai-donna ([#2524](https://github.com/dryvist/ansible-secrets-management/issues/2524)) ([7d89ed6](https://github.com/dryvist/ansible-secrets-management/commit/7d89ed6b4a1b47ecc8ead52c5212c2c0063dedd2))

## [0.2.0](https://github.com/dryvist/ansible-secrets-management/compare/v0.1.0...v0.2.0) (2026-10-10)


### Features

* add GitHub agent flow identities ([7d5b714](https://github.com/dryvist/ansible-secrets-management/commit/7d5b714027b3c2602fed00272f6e3db9f0c338b4))
* **agent_sandbox:** host dispatcher with terminal sessions and a login check ([c7def81](https://github.com/dryvist/ansible-secrets-management/commit/c7def81b3fda3a9814b47e1c80568fb46c55a27e))
* **agent_sandbox:** install the pinned host dispatcher with terminal sessions ([01bc2ee](https://github.com/dryvist/ansible-secrets-management/commit/01bc2ee63917eb4e85db7ea61bf5c5f6e62c313b))
* **agent_sandbox:** provide dispatcher alert settings ([#2382](https://github.com/dryvist/ansible-secrets-management/issues/2382)) ([cc5da81](https://github.com/dryvist/ansible-secrets-management/commit/cc5da8120ecb9e3e64bc7c3a3781c86ec92aaff5))
* **authelia,dashboards:** LiteLLM OIDC client + ingress url_path on board links ([3cc1d67](https://github.com/dryvist/ansible-secrets-management/commit/3cc1d67eb0146b622863b82deaf9871d69fc7e53))
* **authelia,openbao:** seed a UI check service user with TOTP ([bcf07ec](https://github.com/dryvist/ansible-secrets-management/commit/bcf07ec9565c1f85d813f99e770f9484af73b627))
* **authelia,syslog:** narrow Semaphore API bypass, ship iac-platform logs ([#1680](https://github.com/dryvist/ansible-secrets-management/issues/1680)) ([f9a1d09](https://github.com/dryvist/ansible-secrets-management/commit/f9a1d09095a5827ae2a0f91ed2ea80ff52d6851e))
* **authelia:** add run-UI and federated OIDC clients, reconcile operator groups ([#1651](https://github.com/dryvist/ansible-secrets-management/issues/1651)) ([2f43961](https://github.com/dryvist/ansible-secrets-management/commit/2f439614b3e77a4ca20c48edd377fc511165e782))
* **authelia:** declare litellm OIDC client ([d455875](https://github.com/dryvist/ansible-secrets-management/commit/d45587544980d9004d69c8a072a7b0fcd12c5a30))
* **authelia:** exempt the metrics store ingest paths from the forward-auth gate ([#1899](https://github.com/dryvist/ansible-secrets-management/issues/1899)) ([f37e548](https://github.com/dryvist/ansible-secrets-management/commit/f37e548b28f90a90f36573fdbf226f061caa61da))
* **authelia:** register Homarr and Langfuse OIDC clients ([#1554](https://github.com/dryvist/ansible-secrets-management/issues/1554)) ([fad0a41](https://github.com/dryvist/ansible-secrets-management/commit/fad0a419df80c0630142ad90c5ea9da84e32fcd6))
* **authelia:** render litellm confidential client ([a46d68e](https://github.com/dryvist/ansible-secrets-management/commit/a46d68e6fb91a99f3326fe226ca40685a3083b87))
* **ci:** route the runner hosts and Molecule containers through the build caches ([9fe56e9](https://github.com/dryvist/ansible-secrets-management/commit/9fe56e9c13fadf572e58b68ce1a52b03b539c3bb))
* **ci:** route the runner hosts and Molecule containers through the build caches ([1ebc5f5](https://github.com/dryvist/ansible-secrets-management/commit/1ebc5f5182c83681020aa5d5388112caf1927ea7))
* **config:** add exact path entries ([5663df7](https://github.com/dryvist/ansible-secrets-management/commit/5663df74122ea0b08572dba7ad322c1dd0660ff5))
* **config:** add exact path entries ([2eec5d8](https://github.com/dryvist/ansible-secrets-management/commit/2eec5d81551c564b19512cf5beca96d4d70da64f))
* **cribl:** fan OTLP traces out to Arize Phoenix and register its OIDC client ([#1701](https://github.com/dryvist/ansible-secrets-management/issues/1701)) ([12a2c60](https://github.com/dryvist/ansible-secrets-management/commit/12a2c60f1ed13b4b216890d86d47a13417d8a798))
* **deadman:** report to Gatus external endpoints and Healthchecks by slug ([#1856](https://github.com/dryvist/ansible-secrets-management/issues/1856)) ([99b72fc](https://github.com/dryvist/ansible-secrets-management/commit/99b72fc4a2c23d52a4c2a1144edcc43c989b9a29))
* **defaults:** read estate-wide defaults from the secret store ([#1486](https://github.com/dryvist/ansible-secrets-management/issues/1486)) ([be03666](https://github.com/dryvist/ansible-secrets-management/commit/be0366608b2c8b8f388ea6fe97a2520c16601acb))
* **github_runner:** build the Molecule base image once per host and hand it to every scenario ([#1987](https://github.com/dryvist/ansible-secrets-management/issues/1987)) ([04d4b37](https://github.com/dryvist/ansible-secrets-management/commit/04d4b379956a9a59a6dca0bdc7e4d01b4f436188))
* **github_runner:** mint registration tokens from OpenBao, not a static PAT ([#1722](https://github.com/dryvist/ansible-secrets-management/issues/1722)) ([5360cf9](https://github.com/dryvist/ansible-secrets-management/commit/5360cf9057be305aa1b471c3bb5838e7ec57e8cb))
* **github_runner:** run Molecule on the upstream image, drop the custom build ([#2005](https://github.com/dryvist/ansible-secrets-management/issues/2005)) ([d5ad9d7](https://github.com/dryvist/ansible-secrets-management/commit/d5ad9d7a7418ae3ec354d59a24fbe9012fbe5555))
* **github-runner-arc:** add ARC pilot role (k3s + gha-runner-scale-set) ([21846ca](https://github.com/dryvist/ansible-secrets-management/commit/21846caff743a9d2058a73cf8eeb334b4b9bb5db))
* **github-runner-arc:** add ARC pilot role (k3s + gha-runner-scale-set) ([2ef8b6d](https://github.com/dryvist/ansible-secrets-management/commit/2ef8b6d44ca440d0eeb32a51f7e9a53da90823b6))
* **glance:** add Network + Media page and wall kiosk bypass ([#2212](https://github.com/dryvist/ansible-secrets-management/issues/2212)) ([0471738](https://github.com/dryvist/ansible-secrets-management/commit/04717381b250c60c4bcb3224e1c3661455c8dc51))
* **glance:** enable the deployment-profile tile with a generated router key ([#2449](https://github.com/dryvist/ansible-secrets-management/issues/2449)) ([177c3a5](https://github.com/dryvist/ansible-secrets-management/commit/177c3a54e34b583fbb30e0ac78c057e795fe48c0))
* **grafana:** sign in through Authelia SSO ([#1655](https://github.com/dryvist/ansible-secrets-management/issues/1655)) ([a89453e](https://github.com/dryvist/ansible-secrets-management/commit/a89453e1c79e87b823b55b82fb7b2d6c28b633de))
* **healthchecks_docker:** replace the dead email channel with native ntfy ([#1849](https://github.com/dryvist/ansible-secrets-management/issues/1849)) ([e4ae1ac](https://github.com/dryvist/ansible-secrets-management/commit/e4ae1acd88204ab94889575d668d0f3d76017707))
* **homarr:** add the homarr-v2 instance with declarative boards ([#2278](https://github.com/dryvist/ansible-secrets-management/issues/2278)) ([2bc7b39](https://github.com/dryvist/ansible-secrets-management/commit/2bc7b39490c9bda8613ec0d337330c077c5a8519))
* **homarr:** configure integrations from OpenBao over the Homarr API ([#1539](https://github.com/dryvist/ansible-secrets-management/issues/1539)) ([35a60df](https://github.com/dryvist/ansible-secrets-management/commit/35a60df9cfcc71d3bbd6cc5d5f19d8a16c1fb9a0))
* **mcp_gateway:** add MCP gateway role and OpenBao secret wiring ([b72592d](https://github.com/dryvist/ansible-secrets-management/commit/b72592dbf08d20da53c164ad7492364a747f857d))
* **mcp_gateway:** add MCP gateway role and OpenBao secret wiring ([6537d1f](https://github.com/dryvist/ansible-secrets-management/commit/6537d1f9d70e8c29eb8b8ec7517c76f9177f4eff))
* **metrics:** guest-level node_exporter, cAdvisor, PVE API exporter ([#1859](https://github.com/dryvist/ansible-secrets-management/issues/1859)) ([f63da4b](https://github.com/dryvist/ansible-secrets-management/commit/f63da4badd82dc2f1be876c37edf5c720634bd53))
* **ntfy:** alert hub with Slack fan-out and Zammad subscriber ([#1842](https://github.com/dryvist/ansible-secrets-management/issues/1842)) ([a62b13d](https://github.com/dryvist/ansible-secrets-management/commit/a62b13d38bb75e8d0886ee38541ceda66bcd6183))
* **ntfy:** fan every topic out to one all-alerts Slack channel ([#2276](https://github.com/dryvist/ansible-secrets-management/issues/2276)) ([d7128d5](https://github.com/dryvist/ansible-secrets-management/commit/d7128d5ca0373d68d83590a6d0f843e59aaa86f1))
* **ntfy:** provision a publish-only ai-jobs token ([6890f01](https://github.com/dryvist/ansible-secrets-management/commit/6890f0194f14d6d75e060db1fe8b973c0dd68ae4))
* **ntfy:** provision a publish-only ai-jobs token ([45f1508](https://github.com/dryvist/ansible-secrets-management/commit/45f15083a501a21be83aa3895fdba05e595e5d38))
* **object_storage:** mint scoped per-bucket RustFS IAM credentials ([#2200](https://github.com/dryvist/ansible-secrets-management/issues/2200)) ([0b53919](https://github.com/dryvist/ansible-secrets-management/commit/0b5391969f3ec183f01e78add71b30c0c6741f94))
* **openbao_secrets:** accept an operator AppRole pair as the last fallback ([#2101](https://github.com/dryvist/ansible-secrets-management/issues/2101)) ([96e7de7](https://github.com/dryvist/ansible-secrets-management/commit/96e7de70970373ac8347b86f21bbccd73cbf47b5))
* **openbao:** accept a pre-issued rotator token in the rotation play ([#2363](https://github.com/dryvist/ansible-secrets-management/issues/2363)) ([b339e98](https://github.com/dryvist/ansible-secrets-management/commit/b339e9840e6eabba79d687fe67343549d5f3e006))
* **openbao:** accept a pre-issued token as the reconcile identity ([#1783](https://github.com/dryvist/ansible-secrets-management/issues/1783)) ([5d846e3](https://github.com/dryvist/ansible-secrets-management/commit/5d846e36c0ea072b1084cdece79bde92d5112bda))
* **openbao:** add a read-only github-exporter GitHub App tier ([8f80147](https://github.com/dryvist/ansible-secrets-management/commit/8f8014736b8d625f23b20d913309aec659d198ca))
* **openbao:** add a seed-only entry point runnable in either auth mode ([#2118](https://github.com/dryvist/ansible-secrets-management/issues/2118)) ([086c809](https://github.com/dryvist/ansible-secrets-management/commit/086c8091d89dad68eab57c7a41bfee64b2f0846f))
* **openbao:** add a seed-only mode to the AppRole rotation playbook ([#2112](https://github.com/dryvist/ansible-secrets-management/issues/2112)) ([9d3b211](https://github.com/dryvist/ansible-secrets-management/commit/9d3b211b53928a2af7c269a0543d16163e96cddb))
* **openbao:** add a workstation-only converge identity for the OpenBao-node play ([#1862](https://github.com/dryvist/ansible-secrets-management/issues/1862)) ([70e90f1](https://github.com/dryvist/ansible-secrets-management/commit/70e90f10e51bcd2f71ee3b3a19bb08a894c8df70))
* **openbao:** add agent-ssh-sign AppRole for workstation SSH signing ([#2359](https://github.com/dryvist/ansible-secrets-management/issues/2359)) ([78652e1](https://github.com/dryvist/ansible-secrets-management/commit/78652e17fb99090ff72c927d506a70ab330dd148))
* **openbao:** add an agent workstation AppRole ([#2106](https://github.com/dryvist/ansible-secrets-management/issues/2106)) ([bedd914](https://github.com/dryvist/ansible-secrets-management/commit/bedd914e8f1b310ee3ced66559c72ca0b0e4b106))
* **openbao:** add an operator workstation AppRole ([#2097](https://github.com/dryvist/ansible-secrets-management/issues/2097)) ([4ca7225](https://github.com/dryvist/ansible-secrets-management/commit/4ca722505fd2af23100b179fe643c27cde1fac08))
* **openbao:** add approle-audit read-only policy for auth/approle/role ([3a8446f](https://github.com/dryvist/ansible-secrets-management/commit/3a8446f515e070da9bab5a7eee52eea1f4fe2330))
* **openbao:** add bounded admin session role ([a56d9e6](https://github.com/dryvist/ansible-secrets-management/commit/a56d9e67d14d68aac748a106e6dc25aa3df25a89))
* **openbao:** add Cribl Edge generated fields and readers ([#2386](https://github.com/dryvist/ansible-secrets-management/issues/2386)) ([a6ef6ba](https://github.com/dryvist/ansible-secrets-management/commit/a6ef6bafd87f5825f1d9b9095d6f9dbc7713c6a0))
* **openbao:** add daily secret-age auditor timer ([#1821](https://github.com/dryvist/ansible-secrets-management/issues/1821)) ([3db0f9a](https://github.com/dryvist/ansible-secrets-management/commit/3db0f9afc7ec593207f0b9bf4142db7333f1f9c3))
* **openbao:** add github-hermes App mount with visibility-split sets ([#2284](https://github.com/dryvist/ansible-secrets-management/issues/2284)) ([043f741](https://github.com/dryvist/ansible-secrets-management/commit/043f7412588953deb8fd8df8d912ea9344668c5d))
* **openbao:** add github-repo-create tier ([8fdca75](https://github.com/dryvist/ansible-secrets-management/commit/8fdca7558b189f166e0add3185f22b4e42e3a2ac))
* **openbao:** add github-repo-create tier ([1fc7028](https://github.com/dryvist/ansible-secrets-management/commit/1fc7028865506fde66d12539166f0f368bfcd5dd))
* **openbao:** add github-work App mount, policy and AppRole ([0601245](https://github.com/dryvist/ansible-secrets-management/commit/0601245dfb0e40c267eaee884d7cda8d7dec4cf8))
* **openbao:** add github-work App mount, policy and AppRole ([09d9251](https://github.com/dryvist/ansible-secrets-management/commit/09d925190958c83e970ecc6b3fac0d6839312579))
* **openbao:** add Hermes configuration ([#2379](https://github.com/dryvist/ansible-secrets-management/issues/2379)) ([5314292](https://github.com/dryvist/ansible-secrets-management/commit/531429297e6b38c5604ba33f35e35430bb48f99d))
* **openbao:** add inert github-admin-claude repo-create AppRole ([#2055](https://github.com/dryvist/ansible-secrets-management/issues/2055)) ([3636112](https://github.com/dryvist/ansible-secrets-management/commit/36361129a16cfddcdbb492be0c2d6b906f812c86))
* **openbao:** add llm-router-write single-secret writer identity ([#1577](https://github.com/dryvist/ansible-secrets-management/issues/1577)) ([8577d18](https://github.com/dryvist/ansible-secrets-management/commit/8577d18120eb9e1b59b7f6d39d567755ef68ca3b))
* **openbao:** add local-llm-workstation AppRole for workstation reads ([#2352](https://github.com/dryvist/ansible-secrets-management/issues/2352)) ([be55ae3](https://github.com/dryvist/ansible-secrets-management/commit/be55ae32b455ac76295805313a3288eda83b80ca))
* **openbao:** add open-llm's public-repo write permission set ([bc61634](https://github.com/dryvist/ansible-secrets-management/commit/bc61634639b35b10b7c3caebba2ef850e010f0ea))
* **openbao:** add opencode to the ai-api-key provider set ([#1828](https://github.com/dryvist/ansible-secrets-management/issues/1828)) ([3593cfa](https://github.com/dryvist/ansible-secrets-management/commit/3593cfaef85a9205f9401435b21659ba835e0f17))
* **openbao:** add Prometheus telemetry and scrape target ([#2051](https://github.com/dryvist/ansible-secrets-management/issues/2051)) ([84863f8](https://github.com/dryvist/ansible-secrets-management/commit/84863f8b2b769912baaa5b60ec41423e0f7f6c4e))
* **openbao:** add read-only approle-audit policy ([a79e9fd](https://github.com/dryvist/ansible-secrets-management/commit/a79e9fdba4d2cda96583f6748b203da54fa27871))
* **openbao:** add read-only open-llm AppRole ([7242bb9](https://github.com/dryvist/ansible-secrets-management/commit/7242bb976c89520047cf564895c652bf66833721))
* **openbao:** add read-only open-llm AppRole for the successor harness ([9e0b650](https://github.com/dryvist/ansible-secrets-management/commit/9e0b6501b1baf2abc3a4bad66dec0425eddcc381))
* **openbao:** add ssh host-cert signing role ([#2203](https://github.com/dryvist/ansible-secrets-management/issues/2203)) ([3e9cbc4](https://github.com/dryvist/ansible-secrets-management/commit/3e9cbc4f54bf35726518cd206d1db80c41164700))
* **openbao:** add standing operator master-admin AppRole ([12e11d7](https://github.com/dryvist/ansible-secrets-management/commit/12e11d750889da17d223d7ee093b9f86255c7ee7))
* **openbao:** add standing operator master-admin AppRole ([3cfa2d6](https://github.com/dryvist/ansible-secrets-management/commit/3cfa2d6a96eab48df69fc399be26784ed41049a1))
* **openbao:** add the docs router snapshot key, set and OIDC role ([#2505](https://github.com/dryvist/ansible-secrets-management/issues/2505)) ([551e4d9](https://github.com/dryvist/ansible-secrets-management/commit/551e4d922bd93066dc080982300a9996bb6696cf))
* **openbao:** add the iac-platform-semaphore workspace identity ([#1681](https://github.com/dryvist/ansible-secrets-management/issues/1681)) ([4fa7c4a](https://github.com/dryvist/ansible-secrets-management/commit/4fa7c4ac6b0d7dcfa5e438e1d8166bc6c7e00dee))
* **openbao:** add the litellm-local-workstation generated field ([69af118](https://github.com/dryvist/ansible-secrets-management/commit/69af118134aa27b02331c73cb6ad9904febcb615))
* **openbao:** allow a permissions map on github/token write mints ([84ec5f9](https://github.com/dryvist/ansible-secrets-management/commit/84ec5f98ee3b55c9f133974c169247592b70b4dd))
* **openbao:** allow a permissions map on github/token write mints ([4f2a088](https://github.com/dryvist/ansible-secrets-management/commit/4f2a088f082d392c278741aa70c80b23035b7e62))
* **openbao:** attach GitHub and AI read tiers to the workstation identities ([#2111](https://github.com/dryvist/ansible-secrets-management/issues/2111)) ([fabaa99](https://github.com/dryvist/ansible-secrets-management/commit/fabaa99f81182e9c44540e0b8c4f9427c57df748))
* **openbao:** declare a read-only AppRole for the IaC platform deploy ([2abd852](https://github.com/dryvist/ansible-secrets-management/commit/2abd852b0899130afd2f345ffa611483343d8cbc))
* **openbao:** declare a read-only AppRole for the IaC platform deploy ([#1657](https://github.com/dryvist/ansible-secrets-management/issues/1657)) ([d81e3cb](https://github.com/dryvist/ansible-secrets-management/commit/d81e3cbeb01c5c104a32605df96c56f65790f0b8))
* **openbao:** declare disclosure-denylist secret path and read policy ([#2177](https://github.com/dryvist/ansible-secrets-management/issues/2177)) ([7a975b7](https://github.com/dryvist/ansible-secrets-management/commit/7a975b799aa73b71b35697c9ecfdd872528f7600))
* **openbao:** declare the four identities that existed only in the store ([#1788](https://github.com/dryvist/ansible-secrets-management/issues/1788)) ([ace0051](https://github.com/dryvist/ansible-secrets-management/commit/ace005139d56a219886433ec5b23d842e4ba3583))
* **openbao:** define the untrusted dispatcher tier ([63ce58b](https://github.com/dryvist/ansible-secrets-management/commit/63ce58b65474cf1349f38f7cd836579e38b79694))
* **openbao:** docs publisher policy reads one app bucket ([#2073](https://github.com/dryvist/ansible-secrets-management/issues/2073)) ([c43630b](https://github.com/dryvist/ansible-secrets-management/commit/c43630b96fe4a9526f1be36b25a5c5a021a463ae))
* **openbao:** extend Hermes rotation and Context7 configuration ([#2332](https://github.com/dryvist/ansible-secrets-management/issues/2332)) ([2137e49](https://github.com/dryvist/ansible-secrets-management/commit/2137e49f61567308ed86db9d7bc6c3ccb6c006d6))
* **openbao:** fail the converge on an AppRole live but declared nowhere ([#1750](https://github.com/dryvist/ansible-secrets-management/issues/1750)) ([3c4389b](https://github.com/dryvist/ansible-secrets-management/commit/3c4389b7154a49fa83c1af9006ee0dabae229b23))
* **openbao:** fail the converge on an AppRole with no source-address class ([#1747](https://github.com/dryvist/ansible-secrets-management/issues/1747)) ([4843937](https://github.com/dryvist/ansible-secrets-management/commit/48439371250ec1b69edb3db4e1502360bc89dea5))
* **openbao:** fail when the store's provisioning host is absent from a run ([#1766](https://github.com/dryvist/ansible-secrets-management/issues/1766)) ([cd61168](https://github.com/dryvist/ansible-secrets-management/commit/cd61168ceb95350099638a1ea6b7735faf321c5a))
* **openbao:** finite secret_id TTLs, CIDR binding, scoped admin policy, issuer split, human unlock ([#1692](https://github.com/dryvist/ansible-secrets-management/issues/1692)) ([0900005](https://github.com/dryvist/ansible-secrets-management/commit/090000598f0a35f43c3aba86eedad7822c3c8f59))
* **openbao:** generalize slack rotator into an openbao_rotators table, add splunk-mcp ([#1820](https://github.com/dryvist/ansible-secrets-management/issues/1820)) ([8087676](https://github.com/dryvist/ansible-secrets-management/commit/80876765871ca8bb789dea764f599a5563ad701d))
* **openbao:** generate a github-actions router key ([#1825](https://github.com/dryvist/ansible-secrets-management/issues/1825)) ([2f2ac06](https://github.com/dryvist/ansible-secrets-management/commit/2f2ac0664343f24f21d7efd3278acfe4fee53270))
* **openbao:** generate a litellm-local router-key secret ([#2046](https://github.com/dryvist/ansible-secrets-management/issues/2046)) ([170d5a2](https://github.com/dryvist/ansible-secrets-management/commit/170d5a257632e17d3158edb37e4dc31bbfeed3c5))
* **openbao:** generate a litellm-local-workstation router-key secret ([d667131](https://github.com/dryvist/ansible-secrets-management/commit/d667131d6a31586629572c1666ffe35f5ff7003e))
* **openbao:** generate a litellm-local-workstation router-key secret ([#2237](https://github.com/dryvist/ansible-secrets-management/issues/2237)) ([ba42db2](https://github.com/dryvist/ansible-secrets-management/commit/ba42db23b111c0a2b55103e31c4653dd9c750234))
* **openbao:** generate a per-consumer router key for Open WebUI and LangGraph ([#1709](https://github.com/dryvist/ansible-secrets-management/issues/1709)) ([9bb417c](https://github.com/dryvist/ansible-secrets-management/commit/9bb417c70890b309e85e602d2aea7a7552ab96ce))
* **openbao:** generate a scoped router key for langfuse ([#2105](https://github.com/dryvist/ansible-secrets-management/issues/2105)) ([4c3011b](https://github.com/dryvist/ansible-secrets-management/commit/4c3011b28bfa3d952fea957c1b1b3434dd9af635))
* **openbao:** generate a shared Semaphore runner registration token ([#2069](https://github.com/dryvist/ansible-secrets-management/issues/2069)) ([ae5a39a](https://github.com/dryvist/ansible-secrets-management/commit/ae5a39a61fc53fa867adef7ae09301fec2825ee4))
* **openbao:** generate hermes_login_password for the vikunja app secret ([7fc49ac](https://github.com/dryvist/ansible-secrets-management/commit/7fc49acce32bd634d623544fd7e7e650b7bc6011))
* **openbao:** generate hermes_login_password for the vikunja app secret ([3c3f64a](https://github.com/dryvist/ansible-secrets-management/commit/3c3f64a0135846c9e849a2b5f3d84c0afa99edec))
* **openbao:** generate hindsight_api_key in apps/hindsight ([#2354](https://github.com/dryvist/ansible-secrets-management/issues/2354)) ([d5db8f9](https://github.com/dryvist/ansible-secrets-management/commit/d5db8f9b0dacdc6d70d6d50472cce61b6b3a0874))
* **openbao:** generate litellm OIDC client secret ([5d4abb0](https://github.com/dryvist/ansible-secrets-management/commit/5d4abb0bf72a79198d73918ea82b91dff84b9f49))
* **openbao:** generate router keys for eight new apps ([#1867](https://github.com/dryvist/ansible-secrets-management/issues/1867)) ([34646ad](https://github.com/dryvist/ansible-secrets-management/commit/34646ad07a0b5e8139d45f09c6634e34699ebbef))
* **openbao:** generate scoped router keys for agentgateway, dify, llamaindex ([#2104](https://github.com/dryvist/ansible-secrets-management/issues/2104)) ([6e00ac2](https://github.com/dryvist/ansible-secrets-management/commit/6e00ac29847b5cb3cff9af949f2ca63136ecfad3))
* **openbao:** generate the github-actions-oss router key under apps ([d023949](https://github.com/dryvist/ansible-secrets-management/commit/d0239499a1d5c3c6669b5779d95972b52b0ad623))
* **openbao:** generate the github-actions-public router key under apps ([e54d663](https://github.com/dryvist/ansible-secrets-management/commit/e54d663f2991f6238ad411ea1b12f3eb6bbefa46))
* **openbao:** give the unattended execution plane its own identity ([#1724](https://github.com/dryvist/ansible-secrets-management/issues/1724)) ([5b2615a](https://github.com/dryvist/ansible-secrets-management/commit/5b2615a1ddbc985b76c135da59ead7af759a55cb))
* **openbao:** grant LiteLLM provider credential leaves ([d71427a](https://github.com/dryvist/ansible-secrets-management/commit/d71427aa28b0164455958340c6a673ac49b73b8c))
* **openbao:** grant LiteLLM provider credential leaves ([40dadc5](https://github.com/dryvist/ansible-secrets-management/commit/40dadc5400bdb162a6385211c91b614953113c39))
* **openbao:** grant observability read on the OpenRouter usage key ([#2357](https://github.com/dryvist/ansible-secrets-management/issues/2357)) ([ecb22df](https://github.com/dryvist/ansible-secrets-management/commit/ecb22df15903d8afadc5c792ac14651b8fd69d23))
* **openbao:** grant read-only Splunk MCP access ([7e5d255](https://github.com/dryvist/ansible-secrets-management/commit/7e5d2558b46ff30d12c137e8d286988ac417a29c))
* **openbao:** grant read-only Splunk MCP access ([573a5cc](https://github.com/dryvist/ansible-secrets-management/commit/573a5cca9897b9e07baf06e6b9fb9bec6a5022b5))
* **openbao:** grant the agent workstation AppRole the vikunja MCP read policy ([#2108](https://github.com/dryvist/ansible-secrets-management/issues/2108)) ([d0b848d](https://github.com/dryvist/ansible-secrets-management/commit/d0b848d4beb560c969f8a11d9357a27b5586600c))
* **openbao:** grant the converge AppRole a read on the NAS account secret ([#1572](https://github.com/dryvist/ansible-secrets-management/issues/1572)) ([750336a](https://github.com/dryvist/ansible-secrets-management/commit/750336aaca5b6c6d011043cda7e40c7f23135855))
* **openbao:** grant the converge identity its run-environment documents ([#1737](https://github.com/dryvist/ansible-secrets-management/issues/1737)) ([07e1546](https://github.com/dryvist/ansible-secrets-management/commit/07e15464cccb756beeea6255294e1a3ae6540b87))
* **openbao:** grant the pve-exporter token publish path ([#2323](https://github.com/dryvist/ansible-secrets-management/issues/2323)) ([e2d66fb](https://github.com/dryvist/ansible-secrets-management/commit/e2d66fb3413dc353286949a80b0f39d5339722f1))
* **openbao:** grant tofu-proxmox read on ssh-client-ca config ([#2043](https://github.com/dryvist/ansible-secrets-management/issues/2043)) ([9413b48](https://github.com/dryvist/ansible-secrets-management/commit/9413b48fb7fe0930ff2d99945e15f8ad11f39dba))
* **openbao:** let claude-identity rotate its own secret_id ([#2074](https://github.com/dryvist/ansible-secrets-management/issues/2074)) ([26c9cb4](https://github.com/dryvist/ansible-secrets-management/commit/26c9cb497f25f73e93d26c0717561c8039e2ba3b))
* **openbao:** let the agent workstation identity run converges ([#2115](https://github.com/dryvist/ansible-secrets-management/issues/2115)) ([fa87d0f](https://github.com/dryvist/ansible-secrets-management/commit/fa87d0fb69366d2c05628755066fb352da6a704c))
* **openbao:** let the converge identity publish the open-llm bucket ([b751078](https://github.com/dryvist/ansible-secrets-management/commit/b751078e4158b2e43ba941007192ddde84508531))
* **openbao:** let the converge identity publish the open-llm bucket ([d2a956c](https://github.com/dryvist/ansible-secrets-management/commit/d2a956c76c44aebf4c409792409b7b84bf0227ff))
* **openbao:** let the execution plane be the reconcile identity ([#1785](https://github.com/dryvist/ansible-secrets-management/issues/1785)) ([73d1d1c](https://github.com/dryvist/ansible-secrets-management/commit/73d1d1cfcef71a0be20ece74384a57e3e1e6d8c6))
* **openbao:** let the semaphore identity mint read-tier GitHub tokens ([#1742](https://github.com/dryvist/ansible-secrets-management/issues/1742)) ([7700a13](https://github.com/dryvist/ansible-secrets-management/commit/7700a133e69699a0ded699c42c412b0391096e11))
* **openbao:** mint a dedicated router key for Hindsight ([33485b5](https://github.com/dryvist/ansible-secrets-management/commit/33485b5918d7308f0fef0a50f0f56c45cd64a10a))
* **openbao:** mint a dedicated router key for Hindsight ([5a9724d](https://github.com/dryvist/ansible-secrets-management/commit/5a9724dd3712ca37701ff7b3f31a34040527874e))
* **openbao:** mint a repository-scoped docs publisher token from GitHub Actions OIDC ([#1729](https://github.com/dryvist/ansible-secrets-management/issues/1729)) ([1d79191](https://github.com/dryvist/ansible-secrets-management/commit/1d79191498884963073db8a25a4dc01045cd5136))
* **openbao:** mint dedicated router key for n8n ([#2011](https://github.com/dryvist/ansible-secrets-management/issues/2011)) ([6f01c9a](https://github.com/dryvist/ansible-secrets-management/commit/6f01c9a59d871369bf4d8f7cb79fa33463c55350))
* **openbao:** mint the tofu-github token instead of storing it ([#1726](https://github.com/dryvist/ansible-secrets-management/issues/1726)) ([d01c823](https://github.com/dryvist/ansible-secrets-management/commit/d01c823f128017ada6ee42d9cc028a8895617093))
* **openbao:** move policy-sync to an inert openbao-policy-sync AppRole ([#2079](https://github.com/dryvist/ansible-secrets-management/issues/2079)) ([3fb1f4f](https://github.com/dryvist/ansible-secrets-management/commit/3fb1f4f57ef07f0e39b0ea45160693101dcb4d43))
* **openbao:** policy-sync keeps the reconcile policy in step on plane converges ([#2068](https://github.com/dryvist/ansible-secrets-management/issues/2068)) ([8fe4434](https://github.com/dryvist/ansible-secrets-management/commit/8fe4434fda15ad4a1bf6676f0f02cc184181b907))
* **openbao:** promote open-llm's KV bucket, fix policy path ([2bbb6ef](https://github.com/dryvist/ansible-secrets-management/commit/2bbb6efc5909c3d721bb686877a0d26c9072667e))
* **openbao:** promote the task-tracker operator account into its app bucket ([#1794](https://github.com/dryvist/ansible-secrets-management/issues/1794)) ([a70e441](https://github.com/dryvist/ansible-secrets-management/commit/a70e441f59a58d1e326b9a369c8d93cf45a2547a))
* **openbao:** read machine-identity AppRole pairs from the env document in a prefetch play ([#2113](https://github.com/dryvist/ansible-secrets-management/issues/2113)) ([157e80e](https://github.com/dryvist/ansible-secrets-management/commit/157e80edef7c8fb48e3218e4cbcbe98a79eebf2a))
* **openbao:** rotate domain AppRole secret_ids under a dedicated identity ([#2040](https://github.com/dryvist/ansible-secrets-management/issues/2040)) ([335d5cc](https://github.com/dryvist/ansible-secrets-management/commit/335d5cc7a97c47b774c9152f4389983159f5a577))
* **openbao:** rotate the open-llm secret_id on the scheduled cadence ([#2356](https://github.com/dryvist/ansible-secrets-management/issues/2356)) ([b72d162](https://github.com/dryvist/ansible-secrets-management/commit/b72d162c94ada61b2ca0f6289419f95291c931c8))
* **openbao:** say so when provisioning is skipped for want of a token ([#1576](https://github.com/dryvist/ansible-secrets-management/issues/1576)) ([f260451](https://github.com/dryvist/ansible-secrets-management/commit/f260451576eb41d40301dbe9988bf59e1dc31d59))
* **openbao:** seed and grant the hermes-ui app secrets ([#1415](https://github.com/dryvist/ansible-secrets-management/issues/1415)) ([7d6561e](https://github.com/dryvist/ansible-secrets-management/commit/7d6561e88d1e7379502d5ac4dcf3112c0150dc88))
* **openbao:** seed open-llm's vikunja/zammad MCP URLs from OpenBao ([afc29a2](https://github.com/dryvist/ansible-secrets-management/commit/afc29a2ec24b40383e1e55fcac663cec09653239))
* **openbao:** seed open-llm's vikunja/zammad MCP URLs from OpenBao ([88a0803](https://github.com/dryvist/ansible-secrets-management/commit/88a0803ba027c116afb4997e2e0c52f9a6dbcd11))
* **openbao:** self-bootstrapping github-admin-claude with an org-admin set ([#2067](https://github.com/dryvist/ansible-secrets-management/issues/2067)) ([7767306](https://github.com/dryvist/ansible-secrets-management/commit/7767306259d518c7ad37f40f7593e7b6da2588d5))
* **openbao:** set ai-public cidr class and secret_id bounds ([#1886](https://github.com/dryvist/ansible-secrets-management/issues/1886)) ([a5952f7](https://github.com/dryvist/ansible-secrets-management/commit/a5952f762be2bba7326888a6cae3f29878f9ac69))
* **openbao:** set approle-audit CIDR class to machine_or_workstation ([4f169d0](https://github.com/dryvist/ansible-secrets-management/commit/4f169d0c401bdb0635d1807b5b1781d21c2d1432))
* **openbao:** split GitHub engine mounts per App ([#2080](https://github.com/dryvist/ansible-secrets-management/issues/2080)) ([70d3891](https://github.com/dryvist/ansible-secrets-management/commit/70d3891b72ab798e29b8b48378731097cde740de))
* **openbao:** standing secret_id for the vikunja-mcp AppRole ([4e1e2c2](https://github.com/dryvist/ansible-secrets-management/commit/4e1e2c2e001b042ef679f7172554eb1b8e6250a0))
* **openbao:** trust ingress X-Forwarded-For and reconcile bound-CIDR drift ([#1735](https://github.com/dryvist/ansible-secrets-management/issues/1735)) ([eca0975](https://github.com/dryvist/ansible-secrets-management/commit/eca097511dcba1a56f32ceb13caa942770089152))
* **openbao:** update vikunja-mcp AppRole declaration ([019dfb6](https://github.com/dryvist/ansible-secrets-management/commit/019dfb6cd0f5543af2d0c0f73f3aa5aab373977d))
* **openbao:** use installation scope for general write tokens ([becae0a](https://github.com/dryvist/ansible-secrets-management/commit/becae0a305481104e45eb9b0f797e541e79489f8))
* **openbao:** use installation scope for general write tokens ([d94a45d](https://github.com/dryvist/ansible-secrets-management/commit/d94a45d9c8a94c58926648cafe73d9785c737d11))
* **openbao:** use per-call AppRole credentials ([#2437](https://github.com/dryvist/ansible-secrets-management/issues/2437)) ([152dc90](https://github.com/dryvist/ansible-secrets-management/commit/152dc905d46954f207fcb7e50b3947fd4fe68c37))
* **openbao:** validate GitHub App webhook and installation settings ([#2107](https://github.com/dryvist/ansible-secrets-management/issues/2107)) ([f376a49](https://github.com/dryvist/ansible-secrets-management/commit/f376a49e71b25253271989c2a37b3b0c22268988))
* **postgres:** add the litellm database to the ai-VLAN cluster ([#1570](https://github.com/dryvist/ansible-secrets-management/issues/1570)) ([7ed79fe](https://github.com/dryvist/ansible-secrets-management/commit/7ed79fe5575e55ab6b46d748dd8af81e658c2d65))
* **postgres:** optional Patroni/etcd HA mode behind postgres_ha_manager ([#2189](https://github.com/dryvist/ansible-secrets-management/issues/2189)) ([d17d540](https://github.com/dryvist/ansible-secrets-management/commit/d17d5402bcb489cf82630ae746abed2945714103))
* **prometheus_stack:** scrape the LLM router's metrics with a generated per-scraper key ([#1823](https://github.com/dryvist/ansible-secrets-management/issues/1823)) ([934c3d2](https://github.com/dryvist/ansible-secrets-management/commit/934c3d2d5c532f59f9a4d2c73fc2103955ce5893))
* **rotate-key:** add canonical on-demand secret rotation playbook ([#1819](https://github.com/dryvist/ansible-secrets-management/issues/1819)) ([88d7294](https://github.com/dryvist/ansible-secrets-management/commit/88d7294cc8a1c24b4863bb29b226fe2b43292e88))
* **runner:** fall back when the semaphore AppRole login is refused ([#1846](https://github.com/dryvist/ansible-secrets-management/issues/1846)) ([49bd600](https://github.com/dryvist/ansible-secrets-management/commit/49bd600ebc60a0b61340ee6556682c8e361f89eb))
* scaffold the secrets_management collection ([#1](https://github.com/dryvist/ansible-secrets-management/issues/1)) ([99308cf](https://github.com/dryvist/ansible-secrets-management/commit/99308cf2110d665a995a0cdcf1090a8bc4b92d66))
* schedule reconcile rotation ([ec0e531](https://github.com/dryvist/ansible-secrets-management/commit/ec0e53158f21219d2d17c24653f71f43ddf878b4))
* **service_deadman:** add an off-site free-tier deadman + ntfy liveness check ([#1866](https://github.com/dryvist/ansible-secrets-management/issues/1866)) ([c313a63](https://github.com/dryvist/ansible-secrets-management/commit/c313a63c41259d9709787b2a8b0c4cb60f054aa4))
* shared ProxMan cluster ingress, DNS ownership, and workstation connection profile ([#2272](https://github.com/dryvist/ansible-secrets-management/issues/2272)) ([6c67a1e](https://github.com/dryvist/ansible-secrets-management/commit/6c67a1ec52e866aa7bdab9e2e5d053d4a0d64de4))
* **unpoller:** native poller + Cribl scrape + OpenBao credential ([#2174](https://github.com/dryvist/ansible-secrets-management/issues/2174)) ([468ada6](https://github.com/dryvist/ansible-secrets-management/commit/468ada6c932dc4aac6c2b23f9d7ff959f9978585))
* **vikunja:** add data-driven Hermes bridge identity mechanism ([#2062](https://github.com/dryvist/ansible-secrets-management/issues/2062)) ([3ac7d90](https://github.com/dryvist/ansible-secrets-management/commit/3ac7d906d256e0c1dc220447bcb4eeafb0146549))
* **vikunja:** mint a narrow dispatch-queue token and publish it to its own path ([#2109](https://github.com/dryvist/ansible-secrets-management/issues/2109)) ([03b9724](https://github.com/dryvist/ansible-secrets-management/commit/03b9724577d81bb9356b1f379bb87b38831dbd7a))
* **vikunja:** provision the AI Jobs dispatcher token ([cce1b9b](https://github.com/dryvist/ansible-secrets-management/commit/cce1b9b761008cf6976e8a383c5d8b022033eb60))
* **vikunja:** provision the AI Jobs dispatcher token ([2464893](https://github.com/dryvist/ansible-secrets-management/commit/24648938052014cf0fa2d32af95bdc8c810ee09e))
* **vikunja:** publish MCP token to OpenBao with a scoped reader AppRole ([#2054](https://github.com/dryvist/ansible-secrets-management/issues/2054)) ([ae584ee](https://github.com/dryvist/ansible-secrets-management/commit/ae584eec7a280a19912f6f19252b8f2cf5ebb8d2))
* **wall:** serve the server-room wall ([#2139](https://github.com/dryvist/ansible-secrets-management/issues/2139)) ([4415583](https://github.com/dryvist/ansible-secrets-management/commit/4415583de001ab9aec4ea6c15be186143650be8b))
* **zammad,cribl_edge:** Security IDS group, svc-cribl identity, Edge IDS wiring ([#2257](https://github.com/dryvist/ansible-secrets-management/issues/2257)) ([1eea82d](https://github.com/dryvist/ansible-secrets-management/commit/1eea82d01701986b806296f83862b5167c9e1e9d))
* **zammad:** add svc-splunk service account and its own API token ([#1579](https://github.com/dryvist/ansible-secrets-management/issues/1579)) ([a170112](https://github.com/dryvist/ansible-secrets-management/commit/a1701126d5b29df187ffb776d8715f0e9ae9f8b3))


### Bug Fixes

* align the domain catalog ([3b5aa10](https://github.com/dryvist/ansible-secrets-management/commit/3b5aa10965dd41c714bdbf62d4bb37cde0be0a1e))
* assert the single benchmark router key ([#2479](https://github.com/dryvist/ansible-secrets-management/issues/2479)) ([31c5ceb](https://github.com/dryvist/ansible-secrets-management/commit/31c5cebfe3bbb9dcdf11d8b982d7790206fe4d99))
* **authelia:** strip the Digest prefix from service-user hashes ([#2222](https://github.com/dryvist/ansible-secrets-management/issues/2222)) ([81cd257](https://github.com/dryvist/ansible-secrets-management/commit/81cd25793c9299a1178d17ccd86757a2d037c54d))
* **authelia:** strip the Digest prefix so OIDC client secrets are hashes, not plaintext ([#1660](https://github.com/dryvist/ansible-secrets-management/issues/1660)) ([afd21ce](https://github.com/dryvist/ansible-secrets-management/commit/afd21ce61093c24285d84725b3f548757bd70360))
* **authelia:** verify release checksum from signed manifest, drop stale pin ([8f59137](https://github.com/dryvist/ansible-secrets-management/commit/8f5913763fcefabad661619f2e2e2b77b138b1b5))
* **auth:** parameterize role defaults ([#2443](https://github.com/dryvist/ansible-secrets-management/issues/2443)) ([1d1649f](https://github.com/dryvist/ansible-secrets-management/commit/1d1649f846ead60e78e9dcdb4050e89057f4e7e7))
* bound scheduled rotation catalog ([#2399](https://github.com/dryvist/ansible-secrets-management/issues/2399)) ([61fb541](https://github.com/dryvist/ansible-secrets-management/commit/61fb54150d94001ea0e303d57e24b6524422b7f1))
* bound scheduled rotation catalog ([#2399](https://github.com/dryvist/ansible-secrets-management/issues/2399)) ([bdfeaeb](https://github.com/dryvist/ansible-secrets-management/commit/bdfeaeb7f6b8d27fbb793d1756332d01ccf6422d))
* build router key paths from the consumer catalog ([7761562](https://github.com/dryvist/ansible-secrets-management/commit/7761562084a5252475d415541ee562eab506c2fe))
* **ci:** revive the e2e suite with OpenBao-rendered inputs and one matrix job ([#1906](https://github.com/dryvist/ansible-secrets-management/issues/1906)) ([4cd12e6](https://github.com/dryvist/ansible-secrets-management/commit/4cd12e6889383d465f17c298ab92d7db89326c67))
* **cribl_stream:** manage the admin login through the converge ([#1961](https://github.com/dryvist/ansible-secrets-management/issues/1961)) ([ccb2f32](https://github.com/dryvist/ansible-secrets-management/commit/ccb2f326d88fd6dd4626ced229d483becb47ff5e))
* **cribl_stream:** take openbao audit `_time` from the record ([#2516](https://github.com/dryvist/ansible-secrets-management/issues/2516)) ([a748e51](https://github.com/dryvist/ansible-secrets-management/commit/a748e51cd0c0f8dd076e5182f2703a935004f6f1))
* **disclosure:** reword sensitive-category terms in comments and docs ([#2182](https://github.com/dryvist/ansible-secrets-management/issues/2182)) ([0ca9bff](https://github.com/dryvist/ansible-secrets-management/commit/0ca9bffe8c42635aeb4db34b443317643762b170))
* **dns:** front splunk web UI through the shared ingress VIP ([1098d68](https://github.com/dryvist/ansible-secrets-management/commit/1098d68273e949f0d278769414e88c1b5299bdb3))
* **dns:** front splunk web UI through the shared ingress VIP ([8367653](https://github.com/dryvist/ansible-secrets-management/commit/83676539a378ec175f3a63e4eb075adc3c3a3147))
* generate router keys through shared catalog ([#2474](https://github.com/dryvist/ansible-secrets-management/issues/2474)) ([3a109ab](https://github.com/dryvist/ansible-secrets-management/commit/3a109ab4abbdd3124447d0975002fd8249102c4c))
* **homarr:** build the seerr URL from the ingress subdomain; retire the public AppRole ([#1824](https://github.com/dryvist/ansible-secrets-management/issues/1824)) ([7ab7b5b](https://github.com/dryvist/ansible-secrets-management/commit/7ab7b5bd5bfd679594f70c0217ce8edb3df1ad89))
* **inventory:** build fronted service URLs from the ingress zone ([#1666](https://github.com/dryvist/ansible-secrets-management/issues/1666)) ([cb01c45](https://github.com/dryvist/ansible-secrets-management/commit/cb01c453e8ad961bedb66ad19a12c743d30e5a3a))
* **inventory:** preserve tag-selected secret coverage ([90d032c](https://github.com/dryvist/ansible-secrets-management/commit/90d032cca74a2b22b1759b66b810e83d837bb5c8))
* mint flow-lock IDs through approle-issuer ([8efc27d](https://github.com/dryvist/ansible-secrets-management/commit/8efc27d652ee7980e50997a02e3ce996de9fa59b))
* **molecule:** derive expected policy names outside the assert conditional ([#1558](https://github.com/dryvist/ansible-secrets-management/issues/1558)) ([0e81277](https://github.com/dryvist/ansible-secrets-management/commit/0e812779ec32e5315685997ac3bc459f6530ce90))
* **molecule:** give each CI job its own instance names ([#1741](https://github.com/dryvist/ansible-secrets-management/issues/1741)) ([636f5a2](https://github.com/dryvist/ansible-secrets-management/commit/636f5a23dddf1e0f5e429cdafd44a09f8e1acade))
* **ntfy:** single-quote the Zammad topic-group JSON in the subscriber env file ([#2486](https://github.com/dryvist/ansible-secrets-management/issues/2486)) ([55b3418](https://github.com/dryvist/ansible-secrets-management/commit/55b34185f3f9ac9161150a704284ee186a8961ce))
* **openbao_secrets:** decide a failed AppRole login without failing the task ([#2301](https://github.com/dryvist/ansible-secrets-management/issues/2301)) ([ba97921](https://github.com/dryvist/ansible-secrets-management/commit/ba979218bb0713e019c514768c53a6c52554dbcf))
* **openbao_secrets:** declare apps/pve-exporter optional ([#1878](https://github.com/dryvist/ansible-secrets-management/issues/1878)) ([6f31bc3](https://github.com/dryvist/ansible-secrets-management/commit/6f31bc34e2959aef4738c9627baa0254106745fb))
* **openbao_secrets:** declare the local-cloud path optional ([#2293](https://github.com/dryvist/ansible-secrets-management/issues/2293)) ([7bf2124](https://github.com/dryvist/ansible-secrets-management/commit/7bf2124432dda1d1f6e9b47d7d8e647b961a05ae))
* **openbao_secrets:** engine_mount_point AttributeError on ansible-core 2.21 ([#1895](https://github.com/dryvist/ansible-secrets-management/issues/1895)) ([9d3a7a7](https://github.com/dryvist/ansible-secrets-management/commit/9d3a7a74cbdd0308f365143af62373c45299cb15))
* **openbao_secrets:** fail loud on missing or unreadable secrets ([#1691](https://github.com/dryvist/ansible-secrets-management/issues/1691)) ([bffe38b](https://github.com/dryvist/ansible-secrets-management/commit/bffe38b1b323a9cf514ffa886abb91a99562718b))
* **openbao_secrets:** stop the delegated publish escalating on the control node ([#1439](https://github.com/dryvist/ansible-secrets-management/issues/1439)) ([318804a](https://github.com/dryvist/ansible-secrets-management/commit/318804a7708e8bc5811b9a54f155888a9b5b7d0e))
* **openbao_secrets:** take the issuer path only where flow-lock runs ([#2503](https://github.com/dryvist/ansible-secrets-management/issues/2503)) ([75f9f6c](https://github.com/dryvist/ansible-secrets-management/commit/75f9f6c4c98a59dd7969e66a29b4d417607e01a2))
* **openbao:** a denied AppRole existence check is not an absent AppRole ([865b226](https://github.com/dryvist/ansible-secrets-management/commit/865b22641fa451ded785f22a2a9961554de26601))
* **openbao:** admin and write-realm AppRoles accept the workstation ([#1854](https://github.com/dryvist/ansible-secrets-management/issues/1854)) ([8501d94](https://github.com/dryvist/ansible-secrets-management/commit/8501d94bd78e0ea5af2c203d41606ec639b61315))
* **openbao:** ai-admin administers login MFA ([3f59c63](https://github.com/dryvist/ansible-secrets-management/commit/3f59c634f1b6f86f8d13c213270fe0abb1f9b9bf))
* **openbao:** ai-admin administers login MFA ([9016915](https://github.com/dryvist/ansible-secrets-management/commit/9016915c54b9d28163b54926a9238391056f300e))
* **openbao:** alert once per rotator failure streak ([#2515](https://github.com/dryvist/ansible-secrets-management/issues/2515)) ([f7a82d0](https://github.com/dryvist/ansible-secrets-management/commit/f7a82d0cdae13f5585d5b8904483995ef32b67ed))
* **openbao:** bind flow-lock to a machine-or-workstation CIDR class ([#1748](https://github.com/dryvist/ansible-secrets-management/issues/1748)) ([4839da7](https://github.com/dryvist/ansible-secrets-management/commit/4839da72673627d43a0b235e5be587281aa22610))
* **openbao:** bind github-repo-create to the workstation class ([#1869](https://github.com/dryvist/ansible-secrets-management/issues/1869)) ([0dc4133](https://github.com/dryvist/ansible-secrets-management/commit/0dc4133efa6d5c77fd9f7890ea6a907f667456b4))
* **openbao:** bind the ai-sessions-backup AppRole to the workstation class ([81cef7d](https://github.com/dryvist/ansible-secrets-management/commit/81cef7dbd1a28ffef153d40502a0b882f331c797))
* **openbao:** bind the ai-sessions-backup AppRole to the workstation class ([0912923](https://github.com/dryvist/ansible-secrets-management/commit/091292381a6286b1656f2ee913fd5b4cf2eac9c3))
* **openbao:** bind the GitHub write realm to the workstation class ([#1858](https://github.com/dryvist/ansible-secrets-management/issues/1858)) ([a8462b0](https://github.com/dryvist/ansible-secrets-management/commit/a8462b058cc2e08d84922e373f2ba3c3ba2ee63f))
* **openbao:** bound the admin AppRole token to the human unlock window ([#1734](https://github.com/dryvist/ansible-secrets-management/issues/1734)) ([6a172b5](https://github.com/dryvist/ansible-secrets-management/commit/6a172b5e7687de2afad55fc1b8e0c08959fa9ab1))
* **openbao:** build the capability probe's paths without a regex backreference ([04f4b9f](https://github.com/dryvist/ansible-secrets-management/commit/04f4b9f5545efcd1e1c464356f2ac8febd3ad33a))
* **openbao:** classify the platform deploy identity as workstation-held ([#1754](https://github.com/dryvist/ansible-secrets-management/issues/1754)) ([0df097c](https://github.com/dryvist/ansible-secrets-management/commit/0df097c2b8fa212908e4d696ac72c18d4e21497f))
* **openbao:** constrain the one policy path inventory renders verbatim ([d730476](https://github.com/dryvist/ansible-secrets-management/commit/d7304767af65642d4ed9d635ffd882de817a56c9))
* **openbao:** constrain the one policy path inventory renders verbatim ([c826aa3](https://github.com/dryvist/ansible-secrets-management/commit/c826aa37f879ee026bc02ce48915964197ffc6e8))
* **openbao:** converge-domain AppRole secret_ids no longer expire ([#1963](https://github.com/dryvist/ansible-secrets-management/issues/1963)) ([59435cb](https://github.com/dryvist/ansible-secrets-management/commit/59435cb17e172b815048214c13c1428a9c462542))
* **openbao:** create the denylist entry metadata with put when absent ([#2273](https://github.com/dryvist/ansible-secrets-management/issues/2273)) ([40e8589](https://github.com/dryvist/ansible-secrets-management/commit/40e85897f2a737dbdf97691fa922df0152271054))
* **openbao:** curl the snapshot API on an on-box IPv4 ([#1706](https://github.com/dryvist/ansible-secrets-management/issues/1706)) ([3e53f8a](https://github.com/dryvist/ansible-secrets-management/commit/3e53f8a1e8cddcfa70ec8ee82e590ab6c078d285))
* **openbao:** declare the reconcile identity's class as plane-and-workstation ([#1772](https://github.com/dryvist/ansible-secrets-management/issues/1772)) ([15831f2](https://github.com/dryvist/ansible-secrets-management/commit/15831f240ab5eeb21cd6fce286ea5f338e03b226))
* **openbao:** define openbao_write_addr in the exempt-tag test fixture ([#1890](https://github.com/dryvist/ansible-secrets-management/issues/1890)) ([d611f6e](https://github.com/dryvist/ansible-secrets-management/commit/d611f6e2ee0ff2e24e7e32f3d5a3e578ea7b2f35))
* **openbao:** delegate generated secret writes through the CLI host ([e677200](https://github.com/dryvist/ansible-secrets-management/commit/e677200747bfadb1b771d93fb0ea388e9b96e43b))
* **openbao:** delegate the GitHub App check include to localhost ([#2270](https://github.com/dryvist/ansible-secrets-management/issues/2270)) ([65c0388](https://github.com/dryvist/ansible-secrets-management/commit/65c0388b426db360e677254d239dada38385b208))
* **openbao:** delegate the reconcile login to the controller ([f0cd0fe](https://github.com/dryvist/ansible-secrets-management/commit/f0cd0fe844f06632616b7c7fcae700fd84d77ea3))
* **openbao:** deploy the snapshot timer, fix voter-health self-detection, harden audit forwarding ([#1693](https://github.com/dryvist/ansible-secrets-management/issues/1693)) ([6745449](https://github.com/dryvist/ansible-secrets-management/commit/6745449a41f1ff315c481c256287967c83d889be))
* **openbao:** do not declare the Hermes policies without an installation ([#2448](https://github.com/dryvist/ansible-secrets-management/issues/2448)) ([79d7ca8](https://github.com/dryvist/ansible-secrets-management/commit/79d7ca8ad817ef53a728bb0e3bf510977bda799a))
* **openbao:** drop the stale scheduled-mode name load in the rotation play ([#2346](https://github.com/dryvist/ansible-secrets-management/issues/2346)) ([4762c6b](https://github.com/dryvist/ansible-secrets-management/commit/4762c6b4cac13730b1df19553cf924b91add6e55))
* **openbao:** emit the voters count the quorum alert needs, and fail closed ([#1761](https://github.com/dryvist/ansible-secrets-management/issues/1761)) ([e3d5e97](https://github.com/dryvist/ansible-secrets-management/commit/e3d5e97a58a206cbe49c40d1eef2b77f16a45309))
* **openbao:** extend reconcile token session TTL ([626d70a](https://github.com/dryvist/ansible-secrets-management/commit/626d70ae12f6c7dfe6628626963bfc720ee67b1d))
* **openbao:** extend reconcile token session TTL ([86310ca](https://github.com/dryvist/ansible-secrets-management/commit/86310cad5b665cbf24c00230c3d6bf4cc1df549d))
* **openbao:** fail the capability gate on a short probe answer, not only an empty one ([8f1a435](https://github.com/dryvist/ansible-secrets-management/commit/8f1a435ef50fc1db28d627a76b6266af4aeed812))
* **openbao:** fail the converge when no ingress address is trusted for X-Forwarded-For ([#1743](https://github.com/dryvist/ansible-secrets-management/issues/1743)) ([d87fa2f](https://github.com/dryvist/ansible-secrets-management/commit/d87fa2f144cc68e9086855567045a574bc6103f7))
* **openbao:** fail the snapshot leader-gate on local API errors ([#1705](https://github.com/dryvist/ansible-secrets-management/issues/1705)) ([0ed0ddf](https://github.com/dryvist/ansible-secrets-management/commit/0ed0ddf855916114b3107317d8e70491ac50a35c))
* **openbao:** fail with the secrets-engine listing's exit code and stderr ([#1795](https://github.com/dryvist/ansible-secrets-management/issues/1795)) ([8a302e2](https://github.com/dryvist/ansible-secrets-management/commit/8a302e2eea426004f80f5d9f5aa35e3e4e0908ae))
* **openbao:** filter ai-orchestrator GitHub grants by tier ([#1834](https://github.com/dryvist/ansible-secrets-management/issues/1834)) ([fbb8193](https://github.com/dryvist/ansible-secrets-management/commit/fbb81938c09f6b412511b967ba63ea04d95c2e45))
* **openbao:** finish a rotation whose previous secret_id already expired ([#2258](https://github.com/dryvist/ansible-secrets-management/issues/2258)) ([617dfa5](https://github.com/dryvist/ansible-secrets-management/commit/617dfa5449f4a2aec377989b67c6833f4ebbe4a5))
* **openbao:** fold host-cert sign grant into existing signer policies ([#2210](https://github.com/dryvist/ansible-secrets-management/issues/2210)) ([437bbf8](https://github.com/dryvist/ansible-secrets-management/commit/437bbf84d55fe2db396da2066f6795a6b0f742cc))
* **openbao:** gate RBAC reconciliation on real, server-reported capability ([#1641](https://github.com/dryvist/ansible-secrets-management/issues/1641)) ([8903e40](https://github.com/dryvist/ansible-secrets-management/commit/8903e40a95e2d5c8504829b23210b1b91aa21310))
* **openbao:** gate SSH-engine and auth-method bootstrap out of reconcile mode ([#1638](https://github.com/dryvist/ansible-secrets-management/issues/1638)) ([cb81fea](https://github.com/dryvist/ansible-secrets-management/commit/cb81feab2fb96fb6b8c9dcd3e1f561d47e1ba11f))
* **openbao:** gate the KV-mounts init step behind reconcile mode ([#1865](https://github.com/dryvist/ansible-secrets-management/issues/1865)) ([78f5997](https://github.com/dryvist/ansible-secrets-management/commit/78f5997f7560ab7ab0ea5690cc63a1ae03444907))
* **openbao:** gate the rotation-exempt metadata patch on capability; grant it to reconcile ([#1835](https://github.com/dryvist/ansible-secrets-management/issues/1835)) ([ba8efb2](https://github.com/dryvist/ansible-secrets-management/commit/ba8efb2ec9693ba8740c826c45a07539e5fbacd2))
* **openbao:** generate router virtual keys in the format the router accepts ([#1857](https://github.com/dryvist/ansible-secrets-management/issues/1857)) ([79b33f1](https://github.com/dryvist/ansible-secrets-management/commit/79b33f1b00cbc1bc21a5553ea61caad0dceb0fc9))
* **openbao:** generate the monitoring GATUS_EXTERNAL_TOKEN ([#2172](https://github.com/dryvist/ansible-secrets-management/issues/2172)) ([546f0aa](https://github.com/dryvist/ansible-secrets-management/commit/546f0aa55f3fcc2fd350cf50e1eb8ed5405c5641))
* **openbao:** give open-llm the rotated-domain secret_id ttl ([#2518](https://github.com/dryvist/ansible-secrets-management/issues/2518)) ([3697109](https://github.com/dryvist/ansible-secrets-management/commit/36971098c32dff31395db6f8ec16af988519bdd3))
* **openbao:** grant the rotate policy's missing role-id/lookup reads ([#2081](https://github.com/dryvist/ansible-secrets-management/issues/2081)) ([9ffee7f](https://github.com/dryvist/ansible-secrets-management/commit/9ffee7f97276470b9c59f6a40ff4733179ebddff))
* **openbao:** grant tofu-unifi read on the object-storage credential ([#1494](https://github.com/dryvist/ansible-secrets-management/issues/1494)) ([390e297](https://github.com/dryvist/ansible-secrets-management/commit/390e29719b89f51fa72b9d8a1bef18adb68d9133))
* **openbao:** guard secret-age rsyslog drop-in against duplicate imfile load ([#1877](https://github.com/dryvist/ansible-secrets-management/issues/1877)) ([d5bf87e](https://github.com/dryvist/ansible-secrets-management/commit/d5bf87ec0c2ce5ff8a83456131abb93a0b4c33ae))
* **openbao:** install curl and jq on the nodes, and name a missing one ([#1730](https://github.com/dryvist/ansible-secrets-management/issues/1730)) ([73ae403](https://github.com/dryvist/ansible-secrets-management/commit/73ae403b5996f2c8795a5025b469bec617e00973))
* **openbao:** keep finite secret_id bounds on the open-llm AppRole ([7e88bb8](https://github.com/dryvist/ansible-secrets-management/commit/7e88bb81e170050b2f5a5c53811baa454286aa03))
* **openbao:** keep finite secret_id bounds on the open-llm AppRole ([2e9b0de](https://github.com/dryvist/ansible-secrets-management/commit/2e9b0def770e7b8493a37819c46bc8905bc0c915))
* **openbao:** keep finite secret_id bounds on the proxman AppRole ([0822829](https://github.com/dryvist/ansible-secrets-management/commit/082282939702dde6c1fa9ae955f067291cae3ef3))
* **openbao:** keep installation write scope opt-in ([#2336](https://github.com/dryvist/ansible-secrets-management/issues/2336)) ([#2342](https://github.com/dryvist/ansible-secrets-management/issues/2342)) ([c068d9f](https://github.com/dryvist/ansible-secrets-management/commit/c068d9f288dceec4df5183d898b7748a232ed274))
* **openbao:** keep the apps reader's grant on the pve-exporter bucket ([#2328](https://github.com/dryvist/ansible-secrets-management/issues/2328)) ([9eda50e](https://github.com/dryvist/ansible-secrets-management/commit/9eda50ed1922db727a82c0dd26e2cff7114bf358))
* **openbao:** keep the existing static-seal key when none is supplied ([#2102](https://github.com/dryvist/ansible-secrets-management/issues/2102)) ([ca9eda2](https://github.com/dryvist/ansible-secrets-management/commit/ca9eda2050d376b276848cb4d54039e295173a99))
* **openbao:** keep the nodes' seal key id when the environment sets none ([#2244](https://github.com/dryvist/ansible-secrets-management/issues/2244)) ([e8d8d81](https://github.com/dryvist/ansible-secrets-management/commit/e8d8d81ed22501c28812387c7b470276dfddd373))
* **openbao:** load the scheduled identity's name from 05g in the rotation play ([b2add5c](https://github.com/dryvist/ansible-secrets-management/commit/b2add5cefb2b467b3a65d9deae0f51fb3854f652))
* **openbao:** load the scheduled identity's name from 05g in the rotation play ([3e7534c](https://github.com/dryvist/ansible-secrets-management/commit/3e7534c47bdd84fc9d8f0135601715d8e40faffa))
* **openbao:** make the bao CLI routing switch a role default, not a fact ([#1907](https://github.com/dryvist/ansible-secrets-management/issues/1907)) ([9697d2c](https://github.com/dryvist/ansible-secrets-management/commit/9697d2ca4cb665933337395e43911e38107f7ba1))
* **openbao:** make the RBAC policy write actually idempotent ([#1665](https://github.com/dryvist/ansible-secrets-management/issues/1665)) ([6a1bc4d](https://github.com/dryvist/ansible-secrets-management/commit/6a1bc4d146ee91057b96eaf10bb58cbf4586c495))
* **openbao:** mask the role_id read in domain rotation ([#2371](https://github.com/dryvist/ansible-secrets-management/issues/2371)) ([d3af608](https://github.com/dryvist/ansible-secrets-management/commit/d3af608a81667febe7dd4e29a1802827ab5c200d))
* **openbao:** non-expiring class-bound secret_ids for standing identities ([#2509](https://github.com/dryvist/ansible-secrets-management/issues/2509)) ([6d4e47a](https://github.com/dryvist/ansible-secrets-management/commit/6d4e47a646c2db98d7bf0073b6c4ea7990587b8f))
* **openbao:** non-expiring secret_ids for the standing ambient AppRoles ([#1885](https://github.com/dryvist/ansible-secrets-management/issues/1885)) ([6553eb7](https://github.com/dryvist/ansible-secrets-management/commit/6553eb70cdf544990755b03cabe04ee5bf10f702))
* **openbao:** parse the live AppRole list as a bare array ([#2351](https://github.com/dryvist/ansible-secrets-management/issues/2351)) ([15f3246](https://github.com/dryvist/ansible-secrets-management/commit/15f3246f20e1f003b8e3d499d866d2d4b2e77e0d))
* **openbao:** pass item explicitly into nested RBAC policy template renders ([be1a67b](https://github.com/dryvist/ansible-secrets-management/commit/be1a67b7aee6ca91ffe052ebd06259152b6a6da7))
* **openbao:** pass item explicitly into nested RBAC policy template renders ([48116f6](https://github.com/dryvist/ansible-secrets-management/commit/48116f6ef4e0a85bc5b28ec6302233866c2878c8))
* **openbao:** persist the audit imfile read offset ([#2521](https://github.com/dryvist/ansible-secrets-management/issues/2521)) ([a2f5115](https://github.com/dryvist/ansible-secrets-management/commit/a2f5115c7e240703ef4f44dfab898cc1e19f17b8))
* **openbao:** preserve finite write realm bounds ([#2339](https://github.com/dryvist/ansible-secrets-management/issues/2339)) ([1e44f41](https://github.com/dryvist/ansible-secrets-management/commit/1e44f41c3da496ed1413992ab1d7ff6a715fa4a4))
* **openbao:** prove workstation-bound rotated pairs by lookup ([#2149](https://github.com/dryvist/ansible-secrets-management/issues/2149)) ([fe78ec8](https://github.com/dryvist/ansible-secrets-management/commit/fe78ec8778fe89ab5d86b022b0e88e19e220f670))
* **openbao:** read capabilities from both response locations, and separate an empty probe from a denial ([#1653](https://github.com/dryvist/ansible-secrets-management/issues/1653)) ([59bad20](https://github.com/dryvist/ansible-secrets-management/commit/59bad20a14536b6768b3ae6abae5b1d97b817b33))
* **openbao:** read the App install allowlist from the env document ([#2268](https://github.com/dryvist/ansible-secrets-management/issues/2268)) ([0127aad](https://github.com/dryvist/ansible-secrets-management/commit/0127aad84cda0c438ad435f3a25f9756c3ab6ade))
* **openbao:** read the rotator's Doppler target from the platform env doc ([#2127](https://github.com/dryvist/ansible-secrets-management/issues/2127)) ([99c77fd](https://github.com/dryvist/ansible-secrets-management/commit/99c77fd87b0cd79ee1dece1c2ae917f3fdf87830))
* **openbao:** reclassify slack approles for workstation CIDR access ([#1864](https://github.com/dryvist/ansible-secrets-management/issues/1864)) ([8bece7d](https://github.com/dryvist/ansible-secrets-management/commit/8bece7d4defc031f24093d73da03cd0ab119f0ab))
* **openbao:** reconcile AppRole TTL bounds on existing machine roles ([#1704](https://github.com/dryvist/ansible-secrets-management/issues/1704)) ([1e69712](https://github.com/dryvist/ansible-secrets-management/commit/1e697126a6e997d5aa4f0d2be946ac4c01fb8c48))
* **openbao:** reconcile declared RBAC without an operator token ([9417daf](https://github.com/dryvist/ansible-secrets-management/commit/9417daf463f9b434a4f5c61b00508a68febd4bc5))
* **openbao:** reconcile RBAC before tagging rotation-exempt paths ([#1844](https://github.com/dryvist/ansible-secrets-management/issues/1844)) ([1723682](https://github.com/dryvist/ansible-secrets-management/commit/1723682e3cd93dfa2e19225887f81f96b1e96816))
* **openbao:** reconcile through per-call issuer ([#2446](https://github.com/dryvist/ansible-secrets-management/issues/2446)) ([588ac6b](https://github.com/dryvist/ansible-secrets-management/commit/588ac6b1c1a8a9101fb96da2587bd7aa7b0c4105))
* **openbao:** refuse to write an empty rendered RBAC policy ([#1831](https://github.com/dryvist/ansible-secrets-management/issues/1831)) ([5fce97c](https://github.com/dryvist/ansible-secrets-management/commit/5fce97cc5e9103dded139602c8e2f57f8fa4ecc1))
* **openbao:** reload plugin backends on a same-version binary rewrite ([#1997](https://github.com/dryvist/ansible-secrets-management/issues/1997)) ([b0af473](https://github.com/dryvist/ansible-secrets-management/commit/b0af473d11183aa9cbf0de2c90fdd3bcc114224d))
* **openbao:** rename open-llm's promoted vikunja field to VIKUNJA_API_TOKEN ([#2021](https://github.com/dryvist/ansible-secrets-management/issues/2021)) ([f3c430a](https://github.com/dryvist/ansible-secrets-management/commit/f3c430a0b0013c80256654d139fcbfc0f044b435))
* **openbao:** republish rotated workstation AppRole pairs into Doppler ([#2120](https://github.com/dryvist/ansible-secrets-management/issues/2120)) ([15cf20d](https://github.com/dryvist/ansible-secrets-management/commit/15cf20dec40a31f3c72b7737d4ed2c43b58da164))
* **openbao:** resolve the existing TOTP method by the field the API returns ([#1913](https://github.com/dryvist/ansible-secrets-management/issues/1913)) ([cf1d0ed](https://github.com/dryvist/ansible-secrets-management/commit/cf1d0ed696d0bdadabfa2acfebf23b11cec9a896))
* **openbao:** restart notified voters one at a time ([#2519](https://github.com/dryvist/ansible-secrets-management/issues/2519)) ([684e155](https://github.com/dryvist/ansible-secrets-management/commit/684e15596a77058ea3cc7933e1537662e626cbe5))
* **openbao:** restore Cribl Mac rotation catalog ([e43cc9d](https://github.com/dryvist/ansible-secrets-management/commit/e43cc9d587408c4e7f39b297158d0f0f7eb249e3))
* **openbao:** rotate the ai-donna AppRole secret_id with the other agent identities ([#2465](https://github.com/dryvist/ansible-secrets-management/issues/2465)) ([b8ef9b2](https://github.com/dryvist/ansible-secrets-management/commit/b8ef9b2fd575c0b87fbb764ab2b8f18dbdcfcef6))
* **openbao:** run init store calls on the CLI host ([a305c3b](https://github.com/dryvist/ansible-secrets-management/commit/a305c3b7f9996d918ac50fe063a4d7af38df509f))
* **openbao:** run init store calls on the CLI host ([505ae3e](https://github.com/dryvist/ansible-secrets-management/commit/505ae3e03f351c4a44ca41b54ebba47b9145eb32))
* **openbao:** run policy-sync before reconcile-grant consumers ([#2219](https://github.com/dryvist/ansible-secrets-management/issues/2219)) ([a5b30d9](https://github.com/dryvist/ansible-secrets-management/commit/a5b30d9c297bf6246a1731792adca7bb33fef521))
* **openbao:** run policy-sync capability check and write from the controller ([#2221](https://github.com/dryvist/ansible-secrets-management/issues/2221)) ([a461dd0](https://github.com/dryvist/ansible-secrets-management/commit/a461dd002fb6a1e1a2f19f48c6a3c310cd3810cb))
* **openbao:** run the undeclared-live AppRole calls on the CLI host ([#2450](https://github.com/dryvist/ansible-secrets-management/issues/2450)) ([fecf6af](https://github.com/dryvist/ansible-secrets-management/commit/fecf6af8a903a4eee2d6ad2b06f4dc09a4262ad9))
* **openbao:** scheduled AppRole rotation renews itself first and survives a failed domain ([#2510](https://github.com/dryvist/ansible-secrets-management/issues/2510)) ([19d268f](https://github.com/dryvist/ansible-secrets-management/commit/19d268f230b8ce164260def3abe726540d2e4e15))
* **openbao:** scrub environment-specific names from init tasks ([#2259](https://github.com/dryvist/ansible-secrets-management/issues/2259)) ([7b6fa02](https://github.com/dryvist/ansible-secrets-management/commit/7b6fa02e6f7e437a3a027e2798186a6ae54780dc))
* **openbao:** seed the claude-code router key under apps ([2fbe517](https://github.com/dryvist/ansible-secrets-management/commit/2fbe51700123e9183c6683e6fe8e53a093133af6))
* **openbao:** send provisioning writes to the Raft leader ([3c09e54](https://github.com/dryvist/ansible-secrets-management/commit/3c09e540509cf61804af77acab1b92b8fa8d0b00))
* **openbao:** send provisioning writes to the Raft leader ([4f4ada6](https://github.com/dryvist/ansible-secrets-management/commit/4f4ada6d200119b35ea2a34240b24cc13ef2b342))
* **openbao:** send the app-secret promote write from the CLI host ([#2452](https://github.com/dryvist/ansible-secrets-management/issues/2452)) ([7709979](https://github.com/dryvist/ansible-secrets-management/commit/770997926a5b48c8cdb0a8692708aa0e19d9783e))
* **openbao:** set ansible_become false on the delegated App check include ([#2271](https://github.com/dryvist/ansible-secrets-management/issues/2271)) ([1bafa69](https://github.com/dryvist/ansible-secrets-management/commit/1bafa69f1fb7fb35e39db939d7723189e4f6d3fb))
* **openbao:** skip plugin-registering engines in reconcile mode ([#1637](https://github.com/dryvist/ansible-secrets-management/issues/1637)) ([ba28afb](https://github.com/dryvist/ansible-secrets-management/commit/ba28afb20796ff3dec9d06f2e9153955cea7cb5a))
* **openbao:** skip the Doppler sync-token read on a seed run ([#2131](https://github.com/dryvist/ansible-secrets-management/issues/2131)) ([e18fa98](https://github.com/dryvist/ansible-secrets-management/commit/e18fa98311d2e36123ad49140dbd489f26426fb2))
* **openbao:** split rbac-policies to clear the per-file token budget ([28e7981](https://github.com/dryvist/ansible-secrets-management/commit/28e7981beebb67a9d165efd488999f2f73394e28))
* **openbao:** stop the audit trail vanishing for hours at a time ([#1690](https://github.com/dryvist/ansible-secrets-management/issues/1690)) ([509386f](https://github.com/dryvist/ansible-secrets-management/commit/509386fb3be423e1abd4652c9e0e9692b5637e93))
* **openbao:** stop treating a CIDR-refused probe as a dead secret_id ([#2023](https://github.com/dryvist/ansible-secrets-management/issues/2023)) ([24e312f](https://github.com/dryvist/ansible-secrets-management/commit/24e312f27b8acff3eac207a34cc15dd9fed05e25))
* **openbao:** tag and order the per-App GitHub mount phase ([#2514](https://github.com/dryvist/ansible-secrets-management/issues/2514)) ([f0687fa](https://github.com/dryvist/ansible-secrets-management/commit/f0687fa9ddb51a993281272a09fa9e26255be2e8))
* **openbao:** tolerate only a genuine-absence answer before a conditional write ([#1678](https://github.com/dryvist/ansible-secrets-management/issues/1678)) ([ea4e6b7](https://github.com/dryvist/ansible-secrets-management/commit/ea4e6b754de796f2b99866111e0ef836d20435a2))
* **openbao:** trim app-secrets comment under the token-limit gate ([3478e1b](https://github.com/dryvist/ansible-secrets-management/commit/3478e1b27bd1a16ab54205ae6c9a09b69baebd3e))
* **openbao:** trim approle comments under the 4000-token file budget ([c8f3850](https://github.com/dryvist/ansible-secrets-management/commit/c8f38500ad91ae412a83c0152d5dbf8c75312df7))
* **openbao:** tune the approle mount login lockout for shared aliases ([#1872](https://github.com/dryvist/ansible-secrets-management/issues/1872)) ([c70d5ed](https://github.com/dryvist/ansible-secrets-management/commit/c70d5edd169e2e97f27b341c1a35861bc6ac8fea))
* **openbao:** unbound redemption count on the workstation GitHub AppRoles ([#1871](https://github.com/dryvist/ansible-secrets-management/issues/1871)) ([d81c7b2](https://github.com/dryvist/ansible-secrets-management/commit/d81c7b255d4f862f1074e5ae846565e0ce01a2af))
* **openbao:** uppercase open-llm's promoted KV field names ([8bdaf5f](https://github.com/dryvist/ansible-secrets-management/commit/8bdaf5f84472b9d2f077699a9523a1e6bb39cc61))
* **openbao:** validate rsyslog once, after every drop-in writer has run ([#1917](https://github.com/dryvist/ansible-secrets-management/issues/1917)) ([6e0e98f](https://github.com/dryvist/ansible-secrets-management/commit/6e0e98f0e7b194dd6f8adf0bf6724dc0e789097c))
* **openbao:** write KV secret values through the API, never argv ([#2370](https://github.com/dryvist/ansible-secrets-management/issues/2370)) ([a07dced](https://github.com/dryvist/ansible-secrets-management/commit/a07dcedcc1e58b4e7e7a945c7e85b27cb9da7b18))
* **openbao:** write reachable RBAC policies before failing on an ungranted name ([#2213](https://github.com/dryvist/ansible-secrets-management/issues/2213)) ([ad4d62d](https://github.com/dryvist/ansible-secrets-management/commit/ad4d62d488ab96d0fa32a7fd65893679a32f8e87))
* **postgres:** replace removed postgresql_set with postgresql_alter_system ([#1889](https://github.com/dryvist/ansible-secrets-management/issues/1889)) ([208eeca](https://github.com/dryvist/ansible-secrets-management/commit/208eeca6d7125b69255b38d64fb25a94d753c7fb))
* **unpoller:** read the UniFi controller address from OpenBao via the prefetch ([#2227](https://github.com/dryvist/ansible-secrets-management/issues/2227)) ([0749376](https://github.com/dryvist/ansible-secrets-management/commit/07493764074a302a4f9e6aa11a953ffd783641ff))
* **vikunja:** give the donna bridge identity its own OpenBao secret path ([#2087](https://github.com/dryvist/ansible-secrets-management/issues/2087)) ([9b06f81](https://github.com/dryvist/ansible-secrets-management/commit/9b06f81231f74e4bb7de70da45a74c7142e304c2))
* **vikunja:** resolve a stable, persisted login password for each Hermes bridge identity ([#2075](https://github.com/dryvist/ansible-secrets-management/issues/2075)) ([916ba43](https://github.com/dryvist/ansible-secrets-management/commit/916ba436c29e08f12da4476831be35c7d9a5dc75))


### Performance

* **ci:** run the checks a change needs ([#1470](https://github.com/dryvist/ansible-secrets-management/issues/1470)) ([733855b](https://github.com/dryvist/ansible-secrets-management/commit/733855b629ee53b7315a0ccecedb3b309b730f75))
* **converge:** cap wall clock at 20 minutes and run openbao reads on the controller ([#1904](https://github.com/dryvist/ansible-secrets-management/issues/1904)) ([10c0ac6](https://github.com/dryvist/ansible-secrets-management/commit/10c0ac68004ca5625d1363bf4529c0271571420b))
* **openbao:** add openbao_kv_seed tag and controller-side policy reads ([#2193](https://github.com/dryvist/ansible-secrets-management/issues/2193)) ([bf7386c](https://github.com/dryvist/ansible-secrets-management/commit/bf7386c5326efdb04bdd832d05a5cdeec4017c51))
* **openbao:** move remaining read loops to the controller ([5fd9b7d](https://github.com/dryvist/ansible-secrets-management/commit/5fd9b7ded4f7fbf56e024b2577bc9b5ac7bfaf97))
* **openbao:** move remaining read loops to the controller ([91fcbae](https://github.com/dryvist/ansible-secrets-management/commit/91fcbaeffa12bf7f7e494a563e7683229a1b56f8))
* **openbao:** render RBAC policies on the controller, not the target ([#1649](https://github.com/dryvist/ansible-secrets-management/issues/1649)) ([8546179](https://github.com/dryvist/ansible-secrets-management/commit/85461795bc8ba1e4a1b30add87dc28d5eac61784))
* **openbao:** run the AppRole, SSH role and policy writes on openbao_cli_host ([c5f9307](https://github.com/dryvist/ansible-secrets-management/commit/c5f9307dd51c64a517f75361c702f0718659b67d))
* **openbao:** run the AppRole, SSH role and policy writes on openbao_cli_host ([34ef30a](https://github.com/dryvist/ansible-secrets-management/commit/34ef30a79f71b0530aec558b66ee324bc4eb6000))
* **secrets:** scope the OpenBao pre-fetch to domains this run's hosts need ([#2183](https://github.com/dryvist/ansible-secrets-management/issues/2183)) ([bad4da3](https://github.com/dryvist/ansible-secrets-management/commit/bad4da3c46444eab5e117322bd435bd3f1423571))

## Changelog

All notable changes to this project will be documented in this file.

This project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).
Releases are managed automatically by [release-please](https://github.com/googleapis/release-please).
