#!/usr/bin/env python

from click.testing import CliRunner
from bluecat_am.cli import run

VALID_IPS = ['10.128.0.10', '10.128.0.20', '10.128.0.30']
INVALID_IP = '10.20.30.40'
Valid_Domains = ['yes.uoft.ca', 'no.uoft.ca']
INVALID_DOMAINS = ['something.some.thing', 'bozo.uoft.ca']
NONEXIST_DOMAIN = 'blah.alex.utoronto.ca'


def test_cli_command_group():
    """Test to make sure subcommands show up in """
    print()
    cli = CliRunner()
    cmd = '--help'
    result = cli.invoke(run, cmd)
    print('Ran -> bamcli {}'.format(cmd))
    print('Got:')
    print(result.stdout)


def test_view_zones():
    print()
    cli = CliRunner()
    for zone in Valid_Domains:
        cmd = 'view {}'.format(zone)
        result = cli.invoke(run, cmd)
        print('Executed: bamcli {}'.format(cmd))
        print('Output:')
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

def main():
    test_cli_command_group()
    test_view_zones()

if __name__ == '__main__':
    main()
