from bluecat_am import api

import click

@click.command()

@click.argument('action', nargs=1, default='add')
@click.argument('fqdn', nargs=1, default='uoft.ca')
@click.argument('rr_type', nargs=1, default='defRR')
@click.argument('value', nargs=1, default='defVAL')
@click.argument('ttl', nargs=1, default='86400')

@click.option(
        '--debug', default=False,
        help='To show what is going on'
        )

# Main programme

def run(action, fqdn, rr_type, value, ttl, debug):
    '''
    Command line interface to BAM DNS System \n
    Usage: action fqdn rr_type ttl value \n
    E.g.  $ add bozo.uoft.ca A 3600 10.10.10.1 [TTL]
    '''

    api.bam_init(debug)

    if debug:
        click.echo('action: {}'.format(action))
        click.echo('   {}  {}  {} {}'.format(fqdn, ttl, rr_type, value))

    if action == 'add':
        if rr_type == 'defRR' or value == 'defVAL':
            print('Not enough RR information given')
            print('Format: bamcli {} fqdn RR_type value [ttl]'.format(action))
        elif rr_type == 'A':
            ips = value.split(',')
            for ip in ips:
                api.add_rr(fqdn, rr_type, ip, ttl)
        else:
                api.add_rr(fqdn, rr_type, value, ttl)
    elif action == 'replace' or action == 'update':
        if rr_type == 'defRR' or value == 'defVAL':
            print('Not enough RR information given')
            print('Format: bamcli {} fqdn RR_type value'.format(action))
        else:
            api.update_rr(fqdn, rr_type, value, ttl)
    elif action == 'delete' or action == 'remove':
        if rr_type == 'defRR':
            print('No RR type information given')
        elif rr_type == 'CNAME':
            api.delete_rr(fqdn, rr_type)
        elif value != 'defVAL':
            if rr_type == 'A':
                for val in value.split(','):
                    api.delete_rr(fqdn, rr_type, val)    
            else:
                api.delete_rr(fqdn, rr_type, value)
        else:
            print('Not enough RR information given')
            print('Format: bamcli {} fqdn RR_type value'.format(action))
    elif action == 'view' or action == 'list':
        if rr_type == 'defRR':
            api.view_rr(fqdn)
        elif value == 'defVAL':
            api.view_rr(fqdn, rr_type)
        else:
            api.view_rr(fqdn, rr_type, value)
    elif action == 'find':
        if rr_type == 'defRR':
            ids = api.find_rr(fqdn)
        elif value == 'defVAL':
            ids = api.find_rr(fqdn, rr_type)
        else:
            ids = api.find_rr(fqdn, rr_type, value)
        print(ids)


if __name__ == '__main__':
    run()
