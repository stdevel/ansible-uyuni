[![Build Status](https://travis-ci.org/stdevel/ansible-uyuni.svg?branch=master)](https://travis-ci.org/stdevel/ansible-uyuni)

# uyuni

This role prepares, installs and configures [Uyuni](https://uyuni-project.org) and [SUSE Manager](https://www.suse.com/products/suse-manager/).

## Requirements

Make sure to install the `jmespath` Python module.

The system needs access to the internet. Also, you will need an openSUSE Leap or SUSE Linux Enterprise Server 15.1 installation.

## Role Variables

| Variable | Default | Description |
| -------- | ------- | ----------- |
| `suma_release` | `4.1` | SUSE Manager release to install (*4.0 or 4.1*) |
| `scc_reg_code` | - | [SUSE Customer Center](https://scc.suse.com) registration code (*received after trial registration or purchase*) |
| `scc_mail` | - | SUSE Customer Center mail address |
| `scc_check_registration` | `true` | Register system if unregistered |
| `scc_check_modules` | `true` | Activate required modules if not already enabled |
| `sles_modules` | (*Modules required for SUSE Manager 4.x*) | Modules to enable before installation |
| `use_lvm` | `true` | Use LVM to create application volumes |
| `vg_uyuni` | `uyuni` | LVM volume group to create for Docker data |
| `pv_uyuni` | `/dev/sdb` | Disk to use for LVM |
| `lv_spacewalk` | `lv_spacewalk` | Logical volume to create for Spacewalk data |
| `size_spacewalk` | `10240` (*10 GB*) | Logical volume size for Spacewalk data |
| `fs_spacewalk` | `xfs` | File system for Spacewalk data |
| `lv_pgsql` | `lv_pgsql` | Logical volume to create for PostgreSQL data |
| `size_pgsql` | `10240` (*10 GB*) | Logical volume size for PostgreSQL data |
| `fs_pgsql` | `xfs` | File system for PostgreSQL data |
| `uyuni_mail` | `root@localhost` | Web server administrator mail |
| `uyuni_db_name` | `uyuni` | Database name |
| `uyuni_db_user` | `uyuni` | Database user |
| `uyuni_db_pass` | `uyuni` | Database password |
| `cert_city` | `Berlin` | Certificate city |
| `cert_country` | `DE` | Certificate country |
| `cert_mail` | `root@localhost` | Certificate mail |
| `cert_o` | `Berlin` | Certificate organization |
| `cert_ou` | `Berlin` | Certificate organization unit |
| `cert_state` | `Berlin` | Certificate state |
| `cert_pass` | `uyuni` | Certificate password |
| `org_name` | `Demo` | Organization name |
| `org_login` | `admin` | Organization administrator username |
| `org_password` | `admin` | Organization administrator password |
| `org_mail` | `root@localhost` | Organization administrator mail |
| `org_first_name`| `Anton` | Organization administrator first name |
| `org_last_name`| `Administrator` | Organization administrator last name |
| `use_uyuni_repo` | `true` | Flag whether official Uyuni repository should be added |
| `config_firewall` | `true` | Flag whether firewalld should be configured |
| `default_zone` | `internal` | firewalld default zone to set |
| `firewall_services` | `["suse-manager-server"]` | Firewall services to enable |
| `setup_cefs` | `false` | Flag whether errata for CentOS should be generated via [CEFS](https://cefs.steve-meier.de/) |
| `setup_cefs_cronjob` | `false` | Flag whether CEFS cronjob should be generated |
| `setup_defs` | `false` | Flag whether errata for Debian should be generated via [DEFS](https://defs.steve-meier.de/) |
| `setup_defs_cronjob` | `false` | Flag whether DEFS cronjob should be generated |
| `cefs_path` | `/opt/errata-import` | Path to install CEFS and the wrapper script to |
| `channels`| *empty* | Common channels to synchronize (*e.g. ``centos7`` and ``epel7``*) |
| `sync_channels` | `false` | Flag whether created channels should be synced |
| `bootstrap_repos` | `false` | Flag whether Salt bootstrap repositories should be created |

When supplying channels to create in `channels`, ensure passing an array with dicts like this:

```json
[{"name": "centos7", "arch": "x86_64"}, {"name": "centos7-updates", "arch": "x86_64"}]
```

For available channels and architectures, see the ``spacewalk-common-channels.ini`` installed by the ``spacewalk-utils`` package. There is also [an online version](https://github.com/spacewalkproject/spacewalk/blob/master/utils/spacewalk-common-channels.ini) on GitHub.

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
      setup_cefs: true
      setup_cefs_cronjob: true
      setup_defs: true
      setup_defs_cronjob: true
      channels:
        - {"name": "centos7", "arch": "x86_64"}
        - {"name": "centos7-updates", "arch": "x86_64"}
```

Don't forget setting SUSE-related variables when deploying SUSE Manager:

```yaml
    - hosts: servers
      roles:
        - role: stdevel.uyuni
          scc_reg_code: DERP1337LULZ
          scc_mail: bla@foo.bar
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
