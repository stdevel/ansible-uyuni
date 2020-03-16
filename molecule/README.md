# molecule
This folder contains molecule configuration and tests.

## Preparation
Ensure to the following installed:
- [Vagrant](https://vagrantup.com)
- [Oracle VirtualBox](https://virtualbox.org)
- Python modules
  - [`molecule`](https://pypi.org/project/molecule/)
  - [`molecule-vagrant`](https://pypi.org/project/molecule-vagrant/)
  - [`python-vagrant`](https://pypi.org/project/python-vagrant/)

## Environment
The test environment consists of two test scenarios:
- `default` - default scenario with VM running openSUSE Leap 15.1
- `suma` - SUSE Manager 4.x scenario with VM running SUSE Linux Enterprise Server 15 SP1

### SUSE licensing hints
In order to run tests against SUSE Linux Enterprise Server 15 SP1 / SUSE Manager 4.x you will either require a valid subscription or a trial license.
You can request a [60-day trial on the SUSE website.](https://www.suse.com/products/suse-manager/download/)
For this, you will need to create a [SUSE Customer Center](https://scc.suse.com) account - you will **not** be able to request an additional trial for the same release after the 60 days have expired.

When using SLES, alter ``suma/converge.yml`` like this:
```
---
- name: Converge machines
  hosts: all
  roles:
    - role: ansible-uyuni
      scc_reg_code: <insert code here>
      scc_mail: <insert SCC mail here>
...
```

## Usage
In order to create the test environment execute the following command:

```
$ molecule create
```

Run the Ansible role:
```
$ molecule converge
```

Finally, run the tests:
```
$ molecule verify
...
collected 8 items

    tests/test_default.py ........                                           [100%]

    ========================== 8 passed in 14.09 seconds ===========================
Verifier completed successfully.
```

For running tests in the `suma` scenario context, run the commands above with the `-s suma` parameter.