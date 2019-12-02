"""
Molecule unit tests
"""
import os
import testinfra.utils.ansible_runner

TESTINFRA_HOSTS = testinfra.utils.ansible_runner.AnsibleRunner(
    os.environ['MOLECULE_INVENTORY_FILE']
).get_hosts('all')

def test_packages(host):
    """
    check if packages are installed
    """
    # get variables from file
    ansible_vars = host.ansible("include_vars", "file=main.yml")
    print("***")
    print(ansible_vars)
    # depend + uyuni
    for pkg in ansible_vars["ansible_facts"]["core_packages"] + \
        ansible_vars["ansible_facts"]["uyuni_packages"]:
        assert host.package(pkg).is_installed

def test_setup_complete(host):
    """
    check if installation files exist
    """
    with host.sudo():
        for file in [
                "/root/.MANAGER_SETUP_COMPLETE",
                "/root/.MANAGER_INITIALIZATION_COMPLETE"]:
            assert host.file(file).exists

def test_ports_listen(host):
    """
    check if ports are listening
    """
    for port in [22, 80, 443, 4505, 4506]:
        assert host.socket("tcp://0.0.0.0:%s" % port).is_listening

def test_org(host):
    """
    check if organization is accessible
    """
    # get variables from file
    ansible_vars = host.ansible("include_vars", "file=main.yml")
    # check if organization exists
    cmd_org = host.run(
        "spacecmd -q -u %s -p %s org_list",
        ansible_vars["ansible_facts"]["org_login"],
        ansible_vars["ansible_facts"]["org_password"]
        )
    assert cmd_org.stdout.strip() == ansible_vars["ansible_facts"]["org_name"]
