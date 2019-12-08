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
        for filesys in ansible_vars["ansible_facts"]["filesystems"]:
            assert host.mount_point(filesys["mountpoint"]).exists
            assert host.mount_point(filesys["mountpoint"]).filesystem == filesys["type"]

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

def test_errata(host):
    """
    check if CEFS/DEFS are installed properly
    """
    # get variables from file
    ansible_vars = host.ansible("include_vars", "file=main.yml")
    if ansible_vars["ansible_facts"]["setup_cefs"]:
        # check package dependencies
        for pkg in ansible_vars["ansible_facts"]["cefs_packages"]:
            assert host.package(pkg).is_installed
        # check script
        assert host.file(
            "{}/errata-import.pl" % ansible_vars["ansible_facts"]["cefs_path"]
            ).exists
        # check cronjobs
        if ansible_vars["ansible_facts"]["setup_cefs_cronjob"]:
            assert host.file("/etc/cron.d/errata-cefs").exists
        if ansible_vars["ansible_facts"]["setup_defs_cronjob"]:
            assert host.file("/etc/cron.d/errata-defs").exists

def test_channels(host):
    """
    check if supplied channels were created
    """
    # get variables from file
    ansible_vars = host.ansible("include_vars", "file=main.yml")
    if len(ansible_vars["ansible_facts"]["channels"]) > 0:
        # get all channels
        with host.sudo():
            cmd_channels = host.run(
                "spacewalk-repo-sync -l"
            )
        for channel in ansible_vars["ansible_facts"]["channels"]:
            # check channel
            assert channel in cmd_channels