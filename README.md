[![Build Status](https://travis-ci.org/stdevel/ansible-uyuni.svg?branch=master)](https://travis-ci.org/stdevel/ansible-uyuni)

# uyuni

This role prepares, installs and configures [Uyuni](https://uyuni-project.org) and [SUSE Manager](https://www.suse.com/products/suse-manager/).

## Requirements

Make sure to install the `jmespath` and `xml` Python modules.

The system needs access to the internet. Also, you will need an openSUSE Leap or SUSE Linux Enterprise Server 15.1+ installation.

## Role Variables

| Variable | Default | Description |
| -------- | ------- | ----------- |
| `uyuni_suma_release` | `4.1` | SUSE Manager release to install (*4.0 or 4.1*) |
| `uyuni_scc_reg_code` | - | [SUSE Customer Center](https://scc.suse.com) registration code (*received after trial registration or purchase*) |
| `uyuni_scc_mail` | - | SUSE Customer Center mail address |
| `uyuni_scc_check_registration` | `true` | Register system if unregistered |
| `uyuni_scc_check_modules` | `true` | Activate required modules if not already enabled |
| `uyuni_sles_modules` | (*Modules required for SUSE Manager 4.x*) | Modules to enable before installation |
| `uyuni_use_lvm` | `true` | Use LVM to create application volumes |
| `uyuni_vg` | `uyuni` | LVM volume group to create for Docker data |
| `uyuni_pv` | `/dev/sdb` | Disk to use for LVM |
| `uyuni_filesystems` | see [defaults/main.yml](defaults) | LVs, filesystems and mount points to create |
| `uyuni_mail` | `root@localhost` | Web server administrator mail |
| `uyuni_db_name` | `uyuni` | Database name |
| `uyuni_db_user` | `uyuni` | Database user |
| `uyuni_db_pass` | `uyuni` | Database password |
| `uyuni_cert_city` | `Berlin` | Certificate city |
| `uyuni_cert_country` | `DE` | Certificate country |
| `uyuni_cert_mail` | `root@localhost` | Certificate mail |
| `uyuni_cert_o` | `Berlin` | Certificate organization |
| `uyuni_cert_ou` | `Berlin` | Certificate organization unit |
| `uyuni_cert_state` | `Berlin` | Certificate state |
| `uyuni_cert_pass` | `uyuni` | Certificate password |
| `uyuni_org_name` | `Demo` | Organization name |
| `uyuni_org_login` | `admin` | Organization administrator username |
| `uyuni_org_password` | `admin` | Organization administrator password |
| `uyuni_org_mail` | `root@localhost` | Organization administrator mail |
| `uyuni_org_first_name`| `Anton` | Organization administrator first name |
| `uyuni_org_last_name`| `Administrator` | Organization administrator last name |
| `uyuni_use_repo` | `true` | Flag whether official Uyuni repository should be added |
| `uyuni_firewall_config` | `true` | Flag whether firewalld should be configured |
| `uyuni_firewall_default_zone` | `internal` | firewalld default zone to set |
| `uyuni_firewall_services` | `["suse-manager-server"]` | Firewall services to enable |
| `uyuni_setup_cefs` | `false` | Flag whether errata for CentOS should be generated via [CEFS](https://cefs.steve-meier.de/) |
| `uyuni_setup_cefs_cronjob` | `false` | Flag whether CEFS cronjob should be generated |
| `uyuni_setup_defs` | `false` | Flag whether errata for Debian should be generated via [DEFS](https://defs.steve-meier.de/) |
| `uyuni_setup_defs_cronjob` | `false` | Flag whether DEFS cronjob should be generated |
| `uyuni_cefs_path` | `/opt/errata-import` | Path to install CEFS and the wrapper script to |
| `uyuni_channels`| *empty* | Common channels to synchronize (*e.g. ``centos7`` and ``epel7``*) |
| `uyuni_sync_channels` | `false` | Flag whether created channels should be synced |
| `uyuni_bootstrap_repos` | `false` | Flag whether Salt bootstrap repositories should be created |

When supplying channels to create in `channels`, ensure passing a list with dicts like this:

```json
[{"name": "centos7", "arch": "x86_64"}, {"name": "centos7-updates", "arch": "x86_64"}]
```

For available channels and architectures, see the `spacewalk-common-channels.ini` installed by the `spacewalk-utils` package. There is also [an online version](https://github.com/spacewalkproject/spacewalk/blob/master/utils/spacewalk-common-channels.ini) on GitHub.

## Dependencies

No dependencies.

## Example Playbook

Refer to the following example:

```yaml
- hosts: servers
  roles:
    - stdevel.uyuni
```

Set variables if required, e.g.:

```yaml
---
- hosts: uyuni.giertz.loc
  remote_user: root
  roles:
    - role: stdevel.uyuni
      uyuni_setup_cefs: true
      uyuni_setup_cefs_cronjob: true
      uyuni_setup_defs: true
      uyuni_setup_defs_cronjob: true
      uyuni_channels:
        - {"name": "centos7", "arch": "x86_64"}
        - {"name": "centos7-updates", "arch": "x86_64"}
```

Don't forget setting SUSE-related variables when deploying SUSE Manager:

```yaml
- hosts: servers
  roles:
    - role: stdevel.uyuni
      uyuni_scc_reg_code: DERP1337LULZ
      uyuni_scc_mail: bla@foo.bar
```

Ensure having all available system updates installed **before** running the playbook!

## Common issues

Error when running the playbook:

```shell
TASK [ansible-uyuni : Add Uyuni repository] ************************************
An exception occurred during task execution. To see the full traceback, use -vvv. The error was: ImportError: No module named xml.dom.minidom
```

Install the missing `python-xml` package.

## License

Apache 2.0

## Author Information

Christian Stankowic (info@cstan.io)
