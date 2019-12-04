# molecule
This folder contains molecule configuration and tests.

## Preparation
Ensure to the following installed:
- [Vagrant](https://vagrantup.com)
- [Oracle VirtualBox](https://virtualbox.org)
- Molecule pip module

## Usage
In order to create the test environment execute the following command:

```
$ molecule create
```

After that, shutdown the VM and edit it. Add a second disk with **at least 40 GB** to the first controller.
Power-on the VM again.

Run the Ansible role:
```
$ molecule converge
```

Finally, run the tests:
```
$ molecule verify
...
    ===== 5 passed in 24.69 seconds =====
Verifier completed successfully.
```