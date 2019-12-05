[![Build Status](https://travis-ci.org/stdevel/ansible-uyuni.svg?branch=master)](https://travis-ci.org/stdevel/ansible-uyuni)

ansible-uyuni
=============

This role prepares, installs and configures [Uyuni](https://uyuni-project.org).

Requirements
------------

The system needs access to the internet. Also, you will need an openSUSE Leap 15.1 installation.

Role Variables
--------------

| Variable | Default | Description |
| -------- | ------- | ----------- |
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

Dependencies
------------

No dependencies.

Example Playbook
----------------

Refer to the following example:

```
    - hosts: servers
      roles:
         - stdevel.ansible_uyuni
```

Set variables if required, e.g.:
```
---
- hosts: uyuni.giertz.loc
  remote_user: root
  roles:
    - { role: stdevel.ansible_uyuni, pv_uyuni: '/dev/vdb' }
```

License
-------

Apache 2.0

Author Information
------------------

Christian Stankowic (info@cstan.io)
