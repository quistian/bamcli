from click.testing import CliRunner
from bluecat_am.cli import run


VALID_IPS = ['10.128.0.10', '10.128.0.20', '10.128.0.30']
INVALID_IP = '10.20.30.40'
VALID_DOMAIN = 'alex.utoronto.ca'
INVALID_DOMAIN = 'something.some.thing'
NONEXIST_DOMAIN = 'blah.alex.utoronto.ca'


def test_cli_command_group():
    """Test to make sure subcommands show up in """
    print()
    cli = CliRunner()
    cmd = '--help'
    result = cli.invoke(run, cmd)
    print("Ran 'bamcli {}'".format(cmd))
    print("Got:")
    print(result.stdout)


def test_multiple_A_records():
    print()
    cli = CliRunner()
    cmd = 'add {} A {}'.format(VALID_DOMAIN, VALID_IPS[0])
    result = cli.invoke(run, cmd)
    print("Ran 'bamcli {}'".format(cmd))
    print("Got:")
    print(result.stdout)
    cmd = 'add {} A {}'.format(VALID_DOMAIN, VALID_IPS[1])
    result = cli.invoke(run, cmd)
    print("Ran 'bamcli {}'".format(cmd))
    print("Got:")
    print(result.stdout)
    cmd = 'add {} A {}'.format(VALID_DOMAIN, VALID_IPS[2])
    result = cli.invoke(run, cmd)
    print("Ran 'bamcli {}'".format(cmd))
    print("Got:")
    print(result.stdout)
    cmd = 'view alex.utoronto.ca A'
    result = cli.invoke(run, cmd)
    print("Ran 'bamcli {}'".format(cmd))
    print("Got:")
    print(result.stdout)
    cmd = 'find {} A'.format(VALID_DOMAIN)
    result = cli.invoke(run, cmd)
    print("Ran 'bamcli {}'".format(cmd))
    print("Got:")
    print(result.stdout)
    cmd = 'delete {} A {}'.format(VALID_DOMAIN, VALID_IPS[2])
    result = cli.invoke(run, cmd)
    print("Ran 'bamcli {}'".format(cmd))
    print("Got:")
    print(result.stdout)
    cmd = 'delete {} A {}'.format(VALID_DOMAIN, VALID_IPS[1])
    result = cli.invoke(run, cmd)
    print("Ran 'bamcli {}'".format(cmd))
    print("Got:")
    print(result.stdout)
    cmd = 'delete {} A {}'.format(VALID_DOMAIN, VALID_IPS[0])
    result = cli.invoke(run, cmd)
    print("Ran 'bamcli {}'".format(cmd))
    print("Got:")
    print(result.stdout)


def test_add_ip_outside_valid_network():
    print()
    cli = CliRunner()
    cmd = 'add {} A {}'.format(VALID_DOMAIN, INVALID_IP)
    result = cli.invoke(run, cmd)
    print("Ran 'bamcli {}'".format(cmd))
    print("Got:")
    print(result.stdout)


def test_add_fqdn_outside_range():
    print()
    cli = CliRunner()
    cmd = 'add {} A {}'.format(INVALID_DOMAIN, VALID_IPS[0])
    result = cli.invoke(run, cmd)
    print("Ran 'bamcli {}'".format(cmd))
    print("Got:")
    print(result.stdout)


def test_delete_non_existant_FQDN():
    print()
    cli = CliRunner()
    cmd = 'delete {} A {}'.format(NONEXIST_DOMAIN, VALID_IPS[0])
    result = cli.invoke(run, cmd)
    print("Ran 'bamcli {}'".format(cmd))
    print("Got:")
    print(result.stdout)
