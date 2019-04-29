import re
import click
from bluecat_am import config
from bluecat_am import util

def validate_fqdn(ctx, param, value):
    pattern = '[\w]+(\.[\w]+)+'
    if not re.match(pattern, value):
        raise click.BadParameter('Value must be in the form: hobo.utoronto.ca')
    return value

def validate_value(ctx, param, value):
    return value

@click.command()

@click.option(
        '-s', '--silent', is_flag=True,
        help='Minimize the output from commands. Silence is golden')
@click.option(
        '-v', '--verbose', is_flag=True,
        help='Show what is going on for debugging purposes')
@click.argument('action',
                type=click.Choice(['view', 'add', 'delete', 'modify']),
                required=True)
@click.argument('fqdn', type=click.STRING,
                required=True,
                callback=validate_fqdn)
@click.argument('rr_type',
                type=click.Choice(['A', 'MX', 'CNAME', 'TXT', 'defRR']),
                default='defRR')
@click.argument('value', type=click.STRING, default='defVAL',
                callback=validate_value)
@click.argument('ttl', type=click.STRING, default='86400')


# Main programme

def run(action, fqdn, rr_type, value, ttl, silent, verbose):
    """ Command line interface to BAM DNS System\n
    Usage: bamcli action fqdn rr_type ttl value\n
    E.g.  $ add bozo.uoft.ca A 3600 10.10.10.1 [TTL]
    """

    config.Silent = silent
    config.Debug = verbose

    if verbose:
        click.echo('action: {}'.format(action))
        click.echo('    fqdn: {} rr_type: {} value: {}'.format(fqdn,rr_type,value))
        click.echo()

    util.bam_init()


    if action == 'add':
        if rr_type == 'defRR' or value == 'defVAL':
            print('Not enough RR information given')
            print('Format: bamcli {} fqdn RR_type value [ttl]'.format(action))
        elif rr_type == 'A':
            ips = value.split(',')
            for ip in ips:
                util.add_rr(fqdn, rr_type, ip, ttl)
        else:
                util.add_rr(fqdn, rr_type, value, ttl)
    elif action == 'replace' or action == 'update':
        if rr_type == 'defRR' or value == 'defVAL':
            print('Not enough RR information given')
            print('Format: bamcli {} fqdn RR_type value'.format(action))
        else:
            util.update_rr(fqdn, rr_type, value, ttl)
    elif action == 'delete' or action == 'remove':
        if rr_type == 'defRR':
            print('No RR type information given')
        elif rr_type == 'CNAME':
            util.delete_rr(fqdn, rr_type)
        elif value != 'defVAL':
            if rr_type == 'A':
                for val in value.split(','):
                    util.delete_rr(fqdn, rr_type, val)    
            else:
                util.delete_rr(fqdn, rr_type, value)
        else:
            print('Not enough RR information given')
            print('Format: bamcli {} fqdn RR_type value'.format(action))
    elif action == 'view' or action == 'list':
        if rr_type == 'defRR':
            util.view_rr(fqdn)
        elif value == 'defVAL':
            util.view_rr(fqdn, rr_type)
        else:
            util.view_rr(fqdn, rr_type, value)
    elif action == 'find':
        if rr_type == 'defRR':
            ids = util.find_rr(fqdn)
        elif value == 'defVAL':
            ids = util.find_rr(fqdn, rr_type)
        else:
            ids = util.find_rr(fqdn, rr_type, value)
        print(ids)


if __name__ == '__main__':
    run()
