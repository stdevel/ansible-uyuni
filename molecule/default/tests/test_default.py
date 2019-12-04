"""
Molecule unit tests
"""
import os
import testinfra.utils.ansible_runner

TESTINFRA_HOSTS = testinfra.utils.ansible_runner.AnsibleRunner(
    os.environ['MOLECULE_INVENTORY_FILE']
).get_hosts('all')

def test_lvm(host):
    """
    test if storage was set-up correctly
    """
    # get variables from file
    ansible_vars = host.ansible("include_vars", "file=main.yml")
    if ansible_vars["ansible_facts"]["use_lvm"]:
        # check file systems
        for fs in ansible_vars["ansible_facts"]["filesystems"]:
            assert host.mount_point(fs["mountpoint"]).exists
            assert host.mount_point(fs["mountpoint"]).filesystem == fs["type"]

def test_packages(host):
    """
    check if packages are installed
    """
    # get variables from file
    ansible_vars = host.ansible("include_vars", "file=main.yml")
    # check dependencies and Uyuni packages
    for pkg in ansible_vars["ansible_facts"]["core_packages"] + \
        ansible_vars["ansible_facts"]["uyuni_packages"]:
        assert host.package(pkg).is_installed

def test_setup_complete(host):
    """
    check if installation files exist
    """
    with host.sudo():
        for state_file in [
                "/root/.MANAGER_SETUP_COMPLETE",
                "/root/.MANAGER_INITIALIZATION_COMPLETE"]:
            assert host.file(state_file).exists

def test_ports_listen(host):
    """
    check if ports are listening
    """
    for port in [22, 80, 443, 4505, 4506]:
        assert host.socket("tcp://0.0.0.0:%s" % port).is_listening

def test_firewall(host):
    """
    check if firewall is configured properly
    """
    # get variables from file
    ansible_vars = host.ansible("include_vars", "file=main.yml")
    # check if services are enabled
    with host.sudo():
        cmd_fw = host.run("firewall-cmd --list-services")
        for srv in ansible_vars["ansible_facts"]["firewall_services"]:
            assert srv in cmd_fw.stdout.strip()

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
